# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='ltmjsvis',
    version='0.1',
    description="BIGIP LTM Status Visualizer",
    author='Tim Freund',
    author_email='tim@freunds.net',
    license='GPLv2+',
    url='http://github.com/timfreund/ltmjsvis',
    install_requires=[
        'flask',
        'pycontrolshed',
    ],
    packages=['ltmjsvis'],
    test_suite='nose.collector',
    include_package_data=True,
    entry_points="""
    [console_scripts]
    ltmjsvis = ltmjsvis.cli:run_server
    """,
)
