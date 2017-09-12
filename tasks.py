#!/usr/bin/env python
# -*- coding: utf-8 -*-

from invoke import task


@task
def test(ctx):
    """ run flake8 and tests """
    ctx.run('flake8')
    ctx.run('nosetests')


@task
def build_doc(ctx):
    """ build sphinx docs """
    ctx.run('cd docs/ && make html')


@task
def clean_doc(ctx):
    ctx.run('cd docs/ && make clean')


@task
def view_doc(ctx):
    """ open readme of sphinx docs"""
    ctx.run("open -a Google\ Chrome docs/_build/html/index.html")
