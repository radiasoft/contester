# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

def test_env_parser():
    from contester.pkcli.run import _env_parser

    env_str = 'a=b,c=d,e=f'

    env = _env_parser(env_str)

    assert env == {'a':'b', 'c':'d', 'e':'f'}
