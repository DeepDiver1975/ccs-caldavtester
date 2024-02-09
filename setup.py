#!/usr/bin/env python

##
# Copyright (c) 2006-2016 Apple Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

from os.path import dirname, abspath, join as joinpath
from setuptools import setup, find_packages as setuptools_find_packages
import errno
import os
import subprocess

base_version = "0.2"
base_project = "ccs-caldavtester"

#
# Utilities
#


def find_packages():
    modules = []

    for pkg in filter(
        lambda p: os.path.isdir(p) and os.path.isfile(os.path.join(p, "__init__.py")),
        os.listdir(".")
    ):
        modules.extend([pkg, ] + [
            "{}.{}".format(pkg, subpkg)
            for subpkg in setuptools_find_packages(pkg)
        ])
    return modules


def git_info(wc_path):
    """
    Look up info on a GIT working copy.
    """
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.STDOUT,
        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            return None
        raise
    except subprocess.CalledProcessError:
        return None

    branch = branch.decode().strip()

    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "--verify", "HEAD"],
            stderr=subprocess.STDOUT,
        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            return None
        raise
    except subprocess.CalledProcessError:
        return None

    revision = revision.decode().strip()

    try:
        tag = subprocess.check_output(
            ["git", "describe", "--candidates=0", "HEAD"],
            stderr=subprocess.STDOUT,
        )
    except OSError as e:
        if e.errno == errno.ENOENT:
            return None
        raise
    except subprocess.CalledProcessError:
        tag = None
    else:
        tag = tag.decode().strip()

    return dict(
        project=base_project,
        branch=branch,
        revision=revision,
        tag=tag,
    )


#
# Options
#

project_name = "CalDAVTester"

description = "CalDAV/CardDAV protocol test suite"

long_description = open(joinpath(dirname(__file__), "README.md")).read()

url = "https://github.com/apple/ccs-caldavtester"

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2 :: Only",
    "Topic :: Software Development :: Testing",
]

author = "Apple Inc."

author_email = "calendarserver-dev@lists.macosforge.org"

license = "Apache License, Version 2.0"

platforms = ["all"]


#
# Dependencies
#

setup_requirements = []

install_requirements = [
    "pycalendar",
]

extras_requirements = {}


#
# Set up Extension modules that need to be built
#

# from distutils.core import Extension

extensions = []


#
# Run setup
#

def doSetup():
    version_string = "0.2"

    setup(
        name=project_name,
        version=version_string,
        description=description,
        long_description=long_description,
        url=url,
        classifiers=classifiers,
        author=author,
        author_email=author_email,
        license=license,
        platforms=platforms,
        packages=find_packages(),
        package_data={},
        scripts=[],
        data_files=[],
        ext_modules=extensions,
        py_modules=[],
        setup_requires=setup_requirements,
        install_requires=install_requirements,
        extras_require=extras_requirements,
    )


#
# Main
#

if __name__ == "__main__":
    doSetup()
