#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-06-20 20:43
# @Author  : SuperMonkey
# @Site    : 
# @File    : setup.py
# @Software: PyCharm

from setuptools import setup


def readme_data():
    with open('./README.rst', encoding='utf-8') as f:
        data = f.read()

        return data


setup(
    name='ApiTest',
    version='1.0.0',
    author='fyt',
    author_email='fangyt@163.com',
    packages=["ApiTest"],
    install_requires=[
        'PyYAML',
        'requests',
        'jsonpath',
        'DingtalkChatbot',
        'pytest',
        'pytest-parallel'
    ],
    long_description=readme_data(),
    url='https://github.com/fangyt/ApiTest.git'
)