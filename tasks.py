#!/usr/bin/env python
# -*- coding: utf-8 -*-

from invoke import task


@task
def test(ctx):
    """ run flake8 and tests """
    ctx.run('flake8')
    ctx.run('nosetests')
