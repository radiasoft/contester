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
import contester.git
import contester.script
import os

TEST_SCRIPT_NAME = '.radia_tests.yml'

class Runner(object):
    def __init__(self, repo, env):
        self.script = None
        self.test_container = None
        self.repo = contester.git.GitRepo(repo)

    @property
    def script_filename(self):
        return os.path.join(self.repo.location, TEST_SCRIPT_NAME)

    def run(self):
        self._prepare_repo()
        self._read_run_script()
        self._prepare_container()
        self._run_test()

    def _prepare_repo(self):
        self.repo.ensure()
        print('Running on Git repo located at {}'.format(self.repo.location))

    def _read_run_script(self):
        self.script = contester.script.BuildScript(**pkyaml.load_file(self.script_filename))

    def _prepare_container(self):
        self.test_container = contester.docker.TestContainer(build_script=self.script,
                                                             src_location=self.repo.location,
                                                             repo=self.repo,
                                                            )
        self.test_container.prepare()

    def _run_test(self):
        self.test_container.run()
