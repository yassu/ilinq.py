#!/usr/bin/env python
# -*- coding: utf-8 -*-

from invoke import task


def run_commands(ctx, commands):
    for command in commands:
        print(command)
        ctx.run(command)


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


@task
def deploy_doc(ctx):
    build_doc(ctx)
    run_commands(
        ctx,
        [
            'cp -r docs/_build/html/ /tmp/.build',
            'git checkout gh-pages',
            'git clean -fdx',
            'git rm -rf *',
            'mv /tmp/.build/* .',
            'touch .nojekyll',
            'git add .',
            'git commit -m "update docs"',
            'git push origin gh-pages',
        ])
    ctx.run('git checkout master')
