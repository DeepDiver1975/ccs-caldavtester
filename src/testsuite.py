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

"""
Class that encapsulates a series of tests.
"""

from src.test import test
from src.xmlUtils import getYesNoAttributeValue
import src.xmlDefs


class testsuite(object):
    """
    Maintains a list of tests to run as part of a 'suite'.
    """

    def __init__(self, manager):
        self.manager = manager
        self.name = ""
        self.ignore = False
        self.only = False
        self.changeuid = False
        self.require_features = set()
        self.exclude_features = set()
        self.tests = []

    def aboutToRun(self):
        """
        Typically we need the calendar/contact data for a test file to have a common set
        of UIDs, and for each overall test file to have unique UIDs. Occasionally, within
        a test file we also need test suites to have unique UIDs. The "change-uid" attribute
        can be used to reset the active UIDs for a test suite.
        """
        return self.manager.server_info.newUIDs() if self.changeuid else set()

    def missingFeatures(self):
        return self.require_features - self.manager.server_info.features

    def excludedFeatures(self):
        return self.exclude_features & self.manager.server_info.features

    def parseXML(self, node):
        self.name = node.get(src.xmlDefs.ATTR_NAME, "")
        self.ignore = getYesNoAttributeValue(node, src.xmlDefs.ATTR_IGNORE)
        self.only = getYesNoAttributeValue(node, src.xmlDefs.ATTR_ONLY)
        self.changeuid = getYesNoAttributeValue(node, src.xmlDefs.ATTR_CHANGE_UID)

        for child in node:
            if child.tag == src.xmlDefs.ELEMENT_REQUIRE_FEATURE:
                self.parseFeatures(child, require=True)
            elif child.tag == src.xmlDefs.ELEMENT_EXCLUDE_FEATURE:
                self.parseFeatures(child, require=False)
            elif child.tag == src.xmlDefs.ELEMENT_TEST:
                t = test(self.manager)
                t.parseXML(child)
                self.tests.append(t)

    def parseFeatures(self, node, require=True):
        for child in node:
            if child.tag == src.xmlDefs.ELEMENT_FEATURE:
                (self.require_features if require else self.exclude_features).add(child.text)

    def dump(self):
        print("\nTest Suite:")
        print("    name: %s" % self.name)
        for iter in self.tests:
            iter.dump()
