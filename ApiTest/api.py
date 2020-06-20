#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-06-20 15:37
# @Author  : SuperMonkey
# @Site    : 
# @File    : api.py
# @Software: PyCharm

from ApiTest.apiAssert import ApiAssert
from ApiTest.apiData import ParsingData

def assert_body_eq_assert_value(interface_name, assert_name, host_key=None):
	'''
	断言数据是否相等
	:param interface_name:
	:param assert_name:
	:param host_key:
	:return:
	'''
	ApiAssert().assert_eq(interface_name=interface_name,
	                             assert_name=assert_name,
	                             host_key=host_key)


def update_interface_request_data(interface_name, assert_name, new_request_data: dict):
	'''
	更新接口请求数据
	:param interface_name:
	:param assert_name:
	:param new_request_data:
	:return:
	'''
	ParsingData().update_interface_request_data(interface_name=interface_name,
	                                                   assert_name=assert_name,
	                                                   new_request_data=new_request_data)


def update_interface_json_path(interface_name, assert_name, new_value: dict = None):
	'''
	更多断言值jsonpath表达式
	:param interface_name:
	:param assert_name:
	:param new_value:
	:return:
	'''
	ParsingData().update_interface_json_path(interface_name=interface_name,
	                                                assert_name=assert_name,
	                                                new_value=new_value)