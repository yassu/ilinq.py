#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _get_short_version(full_version):
    return '.'.join(full_version.split('.')[:2])


__VERSION__ = '0.3.1'
__SHORT_VERSION__ = _get_short_version(__VERSION__)
