# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from pykern import pkjinja
from pykern.pkdebug import pkdc, pkdexc, pkdp
from sh import docker
import contester.templates
import os
import shutil
import tempfile

def _process_output(line):
    pkdc(line)

class TestContainer(object):
    def __init__(self, src_location, build_script, repo_name, repo_commit, repo_branch):
        self.repo_branch = repo_branch
        self.repo_commit = repo_commit
        self.repo_name = repo_name
        self.script = build_script
        self.src = src_location

    def prepare(self):
        self._pull_base()
        self._prepare_test_image()

    def _pull_base(self):
        assert docker.pull(self.script.base_container, _out=_process_output).exit_code == 0

    def _prepare_test_image(self):
        with tempfile.TemporaryDirectory() as build_dir_path:
            if self.script.files is not None:
                for filename in self.script.files:
                    assert not os.path.isabs(filename), 'Only relative paths allowed'
                    full_src = os.path.join(self.src, filename)
                    full_dst = os.path.join(build_dir_path, filename)

                    pkdc('Copy: {0} -> {1}', full_src, full_dst)

                    shutil.copyfile(full_src, full_dst)

            dockerfile = os.path.join(build_dir_path, 'Dockerfile')

            pkjinja.render_file(
                    filename=contester.templates.DOCKERFILE,
                    output=dockerfile,
                    values={
                        'script': self.script,
                    },
            )

            pkdc(open(dockerfile).read())

            container_tag = 'contester/{0.repo_name}_{0.repo_branch}:{0.repo_commit}'.format(self)

            docker.build('-t', container_tag, build_dir_path, _out=_process_output)
