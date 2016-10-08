# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from future.standard_library import install_aliases
install_aliases()

from pykern import pkyaml
from pykern.pkdebug import pkdc, pkdexc, pkdp
import contester.docker
import contester.script
import os
import urllib.parse

TEST_SCRIPT_NAME = '.radia_tests.yml'

class Runner(object):
    def __init__(self, repo, env):
        self.location = None
        self.script = None
        self.test_container = None
        self.repo_url = urllib.parse.urlparse(repo)
        self.repo_type = None

    @property
    def script_filename(self):
        return os.path.join(self.location, TEST_SCRIPT_NAME)

    def run(self):
        self._prepare_repo()
        self._read_run_script()
        self._prepare_container()

    def _prepare_repo(self):
        {
            '': self._prepare_local_repo
        }[self.repo_url.scheme]()

    def _prepare_local_repo(self):
        if os.path.isabs(self.repo_url.path):
            self.location = self.repo_url.path
        else:
            self.location = os.path.realpath(os.path.join(os.getcwd(), self.repo_url.path))
        pkdc('LOCAL repo: {}', self.location)

    def _read_run_script(self):
        self.script = contester.script.BuildScript(**pkyaml.load_file(self.script_filename))

    def _prepare_container(self):
        self.test_container = contester.docker.TestContainer(build_script=self.script,
                                                             src_location=self.location)
        self.test_container.prepare()
