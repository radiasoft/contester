# -*- coding: utf-8 -*-

"""
:copyright: Copyright (c) 2016 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""

from __future__ import print_function
import contextlib
import shutil
import sys
import tempfile

if sys.version_info < (3,):
    _print = print
    def print(*a, **kw):
        flush = kw.pop('flush', False)
        _print(*a, **kw)
        if flush:
            kw.get('file', sys.stdout).flush()

    @contextlib.contextmanager
    def TemporaryDirectory(suffix='', prefix='tmp', dir=None):
        tempdir = tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
        yield tempdir
        shutil.rmtree(tempdir)


else:
    TemporaryDirectory = tempfile.TemporaryDirectory
