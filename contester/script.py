# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from pykern.pkdebug import pkdc, pkdexc, pkdp

class BuildScript(object):
    def __init__(self, container, test, files=None, prepare_script=None, packages=None):
        self.base_container = container
        self.files = files
        self.packages = packages
        self.prepare_script = prepare_script
        self.test = test
