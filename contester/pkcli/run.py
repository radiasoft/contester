# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

import os
import contester.runner

def _env_parser(envstr):
    env = {}
    if envstr is not None:
        for kv in envstr.split(','):
            key, value = kv.split('=')
            env[key] = value
    return env


def default_command(repo=None, env=None):
    env = _env_parser(env)
    if repo is None:
        repo = os.getcwd()

    contester.runner.Runner(repo, env).run()
