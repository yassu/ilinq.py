#!/usr/bin/env python
# -*- coding: utf-8 -*-

from invoke import task


def run_commands(ctx, commands):
    for command in commands:
        print(command)
        ctx.run(command)


@task
def test(ctx, verbose=False):
    """ run flake8 and tests """
    ctx.run('flake8')

    nose_command = 'nosetests --with-coverage --cover-html'
    if verbose:
        nose_command += " --verbose"
    ctx.run(nose_command)


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
def release(ctx):
    from ilinq import __VERSION__
    run_commands(
        ctx,
        [
            'python setup.py sdist bdist_wheel',
            'twine upload dist/*',
            'git tag {}'.format(__VERSION__)
        ])
    deploy_doc(ctx)


@task
def deploy_doc(ctx):
    build_doc(ctx)
    run_commands(
        ctx,
        [
            'git stash',
            'cp -r docs/_build/html/ /tmp/.build',
            'git checkout gh-pages',
            'git clean -fdx',
            'rm -rf *',
            'git rm -rf *',
            'mv /tmp/.build/* .',
            'touch .nojekyll',
            'git add .',
            'git commit --allow-empty -m "update docs"',
            'git push -f origin gh-pages',
            'git checkout master',
            'git stash pop',
        ])

    build_doc(ctx)
