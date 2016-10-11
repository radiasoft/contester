# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from __future__ import print_function
from pykern import pkjinja
from pykern.pkdebug import pkdc, pkdexc, pkdp
from sh import docker
import contester.templates
import os
import shutil
import sys

if sys.version_info < (3,):
    from contester.py2py3 import TemporaryDirectory, print
else:
    from tempfile import TemporaryDirectory

class TestContainer(object):
    def __init__(self, src_location, build_script, repo):
        self.repo = repo
        self.script = build_script
        self.src = src_location
        self.tag = None

    def prepare(self):
        self._pull_base()
        self._prepare_test_image()

    def _pull_base(self):
        print('Pulling base image: {0}...'.format(self.script.base_container), end='', flush=True)
        docker.pull(self.script.base_container, _out=pkdc)
        print('done', flush=True)

    def _prepare_test_image(self):
        print('Preparing test image...', end='', flush=True)
        with TemporaryDirectory() as build_dir_path:
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
                        'git_branch': self.repo.branch,
                        'git_commit': self.repo.commit,
                        'git_dirty': self.repo.dirty,
                        'git_name': self.repo.repo_name,
                        'script': self.script,
                    },
            )

            pkdc(open(dockerfile).read())

            container_name = 'contester/{0.repo.repo_name}_{0.repo.branch}'.format(self)
            self.tag = ':'.join([container_name, self.repo.commit])


            docker.build('-t', ':'.join([container_name, 'latest']),
                         '-t', self.tag,
                         build_dir_path, _out=pkdc)
        print('done.', flush=True)
        print('Test image built as {0}.'.format(self.tag), flush=True)

    def run(self):
        # TODO(@elventear) I would like to mount the repo as 'ro', but pykern fails, it seems to
        # try to write in the same location as the test.
        docker.run(
            '-v', '{0.repo.location}:/{0.repo.repo_name}:rw'.format(self),
            '-w', '/{0.repo.repo_name}'.format(self),
            '-u', '1000',
            '--rm', '-i', self.tag,
            '/bin/bash', '-l', '-c', self.script.test,
            _out=print,
        )
