# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from future import standard_library
standard_library.install_aliases()

import contester.git
import pytest

# git status --porcelain
STATUS_OUT = \
"""
M  .radia_tests.yml
M  contester/docker.py
M  contester/git.py
M  contester/templates/Dockerfile.j2
M  requirements.txt
RM tests/runner_test.py -> tests/git_test.py
M  tests/pkcli/run_test.py
?? contester/git.py.bak
"""

class GitSideEffect(object):
    def __init__(self, mocker, branch, commit, dirty):
        self.commit = commit
        self.branch = branch

        if dirty:
            self.status = STATUS_OUT
        else:
            self.status = ''

        self.mock = mocker.patch('contester.git.git', autospec=True)
        self.mock.bake.side_effect = self.bake_side_effect

        self.git_call = mocker.MagicMock()
        self.git_call.side_effect = self.git_call_side_effect

    def bake_side_effect(self, *a, **kw):
        git_dir = kw['git_dir']
        assert git_dir.endswith('.git')
        return self.git_call

    def git_call_side_effect(self, *a):
        return {
            ('symbolic-ref', '--short', '-q', 'HEAD'): self.branch,
            ('rev-parse', '--short', 'HEAD'): self.commit,
            ('status', '--porcelain'): self.status
        }[a]

@pytest.mark.parametrize("dirty", [
    True, False
])
def test_local_repo_absolute(mocker, dirty):
    repo_path = '/some'
    branch = 'master'
    commit = 'abcde'

    side_effects = GitSideEffect(mocker, branch, commit, dirty)

    git = contester.git.GitRepo(repo_path)
    git.ensure()

    assert git.location == repo_path
    assert git.branch == branch
    assert git.commit == commit
    assert git.dirty == dirty

@pytest.mark.parametrize("dirty", [
    True, False
])
def test_local_repo_relative(mocker, dirty):
    repo_path = '/some'
    branch = 'master'
    commit = 'abcde'

    getcwd = mocker.patch('os.getcwd')
    getcwd.return_value = '/some/path'

    side_effects = GitSideEffect(mocker, branch, commit, dirty)

    git = contester.git.GitRepo('..')
    git.ensure()

    assert git.location == repo_path
    assert git.branch == branch
    assert git.commit == commit
    assert git.dirty == dirty
