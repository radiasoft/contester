# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from pykern.pkdebug import pkdc, pkdexc, pkdp
from sh import git
import os
import urllib.parse

class GitRepo(object):
    def __init__(self, repo_url):
        self._commit = None
        self.branch = None
        self.dirty = False
        self.git = None
        self.location = None
        self.repo_name = None
        self.repo_url = urllib.parse.urlparse(repo_url)

    def ensure(self):
        {
            '': self._process_local_repo
        }[self.repo_url.scheme]()

        self.git = git.bake(git_dir=os.path.join(self.location, '.git'))
        self._read_repo_state()
        pkdc('Git Repo: {0} {1}@{2}', self.location, self.branch, self.commit)

    def _process_local_repo(self):
        if os.path.isabs(self.repo_url.path):
            self.location = self.repo_url.path
        else:
            self.location = os.path.realpath(os.path.join(os.getcwd(), self.repo_url.path))

    @property
    def commit(self):
        if self.dirty:
            return '.'.join([self._commit, 'dirty'])
        return self._commit

    def _read_repo_state(self):
        self._commit = str(self.git('rev-parse', '--short', 'HEAD')).strip()
        self.branch = str(self.git('symbolic-ref', '--short', '-q', 'HEAD')).strip()
        self.dirty = len(str(self.git('status', '--porcelain')).strip()) > 0
        self.repo_name = os.path.basename(self.location)
