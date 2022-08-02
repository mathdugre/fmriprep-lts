#!/bin/python3 env
import json
import os
import subprocess
import sys

import datalad.api as api


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


with open("fmriprep-cmd.json") as fin:
    metadata = json.load(fin)

for dataset, subjects in metadata.items():
    try:
        api.clone(f"///openneuro/{dataset}")
    except:
        api.siblings(dataset=dataset)
        api.clone(f"///openneuro/{dataset}")

    for subject in subjects.keys():
        api.get(path=os.path.join(dataset, subject), dataset=dataset, recursive=True)

TEMPLATEFLOW_HOME=os.path.join(os.path.expanduser("~"), ".cache", "templateflow")
api.clone("///templateflow", path=TEMPLATEFLOW_HOME)
api.get(path=TEMPLATEFLOW_HOME, dataset=TEMPLATEFLOW_HOME, recursive=True)

