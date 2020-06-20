#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Time   : 2020-03-18 23:40
# Author : fyt
# File   : apiData.py

import os, yaml, operator, jsonpath, copy, ytApiTest, json, warnings
from urllib.parse import urlparse


class YAML_CONFIG_KEY():
	OBJECT_HOST = 'OBJECT_HOST'
	DING_TALK_URL = 'DING_TALK_URL'
	INTERFACE_URL = 'url'
	CASE_REQUEST_DATA = 'req_data'
	CASE_ASSERT_DATA = 'ast_data'
	CASE_DES = 'des'
	CASE_JSON_EXPR = 'json_expr'
	CASE_SETUP = 'setup'
	CASE_TEARDOWN = 'teardown'
	INTERFACE_REQUEST_HEADERS = 'headers'

class FindFile():
	
	def get_yaml_path(self):
		'''
		查找用例数据文件
		:return:
		'''
		for dirpath, dirnames, filenames in os.walk('./'):
			
			if len(filenames):
				
				for index, file_name in enumerate(filenames):
					
					if bool(os.path.splitext(file_name).count('.yaml')):
						return os.path.join(dirpath, file_name)

class YamlSingleton():
	_obj = None
	_init_flag = True
	yaml_data = None
	res_data = dict()
	
	def __new__(cls, *args, **kwargs):
		
		if YamlSingleton._obj == None:
			YamlSingleton._obj = object.__new__(cls)
		
		return cls._obj
	
	def __init__(self):
		
		if YamlSingleton._init_flag:
			YamlSingleton._init_flag = False
			YamlSingleton.yaml_data = self.get_yaml_data()
			YamlSingleton.res_data = self.res_data
	
	def get_yaml_data(self):
		'''
		获取yaml测试数据
		:return:
		'''
		
		yaml_file_path = FindFile().get_yaml_path()
		
		assert yaml_file_path, AssertionError('未找到yaml数据文件')
		temp_dic = {}
		with open(yaml_file_path, encoding='UTF-8') as f:
			all_dic = yaml.load_all(f, Loader=yaml.FullLoader)
			
			for dic in all_dic:
				temp_dic.update(dic)
		
		return temp_dic
	
	def update_response_data(self, response: dict):
		'''
		更新接口返回数据
		'''
		self.res_data.update(response)

class ParsingData():
	
	def __init__(self):
		
		self.yaml_data = YamlSingleton().yaml_data
		self.response_data = YamlSingleton().res_data
	
	def get_interface_data(self,  interface_name, assert_name, yaml_config_key,yaml_data= None):
		
		'''
		获取接口数据
		:param interface_name: 接口名称
		:param assert_name: 接口对应断言名称
		:param yaml_config_key: yaml配置key
		:return:
		'''
		
		if yaml_data is None: yaml_data = self.yaml_data
		
		if yaml_data.__contains__(interface_name) and yaml_data[interface_name].__contains__(assert_name) and \
				yaml_data[interface_name][assert_name].__contains__(yaml_config_key):
			return yaml_data[interface_name][assert_name][yaml_config_key]
	
	def get_object_host(self, host_key: str = None):
		'''
		获取项目host ，默认返回第一个HOST
		:param host_key:
		:return:
		'''
		
		dict_host = self.yaml_data.get(YAML_CONFIG_KEY.OBJECT_HOST)
		
		if host_key is None:
			return iter(dict_host.values()).__next__()
		
		return dict_host.get(host_key)
	
	def get_interface_url(self, interface_name: str, host_key: str = None):
		'''
		获取接口URL路径
		:param interface_name: 接口名称
		:param host_key: 项目host_key
		:return:
		'''
		if self.yaml_data.__contains__(interface_name):
			
			url = self.yaml_data[interface_name][YAML_CONFIG_KEY.INTERFACE_URL]
			
			if url.find('http') != -1:
				return url
			
			return self.get_object_host(host_key=host_key) + url
	
	def get_interface_request_data(self, interface_name, assert_name):
		'''
		获取接口请求数据
		:param interface_name: 接口名称
		:param assert_name: 断言名称
		:return:
		'''
		
		old_yaml_data = copy.deepcopy(self.yaml_data)
		
		old_request_data = self.get_interface_data(yaml_data=old_yaml_data,
		                                           interface_name=interface_name,
		                                           assert_name=assert_name,
		                                           yaml_config_key=YAML_CONFIG_KEY.CASE_REQUEST_DATA)
		
		if operator.ne(old_request_data, None):
			
			new_request_data = json.dumps(old_request_data)
			
			if new_request_data.find('$') == -1:
				return new_request_data
			
			self.recursive_replace_json_expr(replace_value=old_request_data)
		
		return json.dumps(old_request_data)
	
	def get_interface_assert_value(self, interface_name, assert_name):
		
		'''
		获取接口断言数据
		:param interface_name: 接口名称
		:param assert_name:  接口对应断言名称
		:return:
		'''
		
		assert_value = self.get_interface_data(interface_name=interface_name,
		                                       assert_name=assert_name,
		                                       yaml_config_key=YAML_CONFIG_KEY.CASE_ASSERT_DATA)
		
		if assert_value is None:
			
			return assert_value
		
		if json.dumps(assert_value).find('$') != -1:
		
			self.recursive_replace_json_expr(assert_value)
		
		return assert_value
	
	def get_interface_des(self, interface_name, assert_name):
		
		'''
		获取用例说明
		:param interface_name: 接口名称
		:param assert_name: 接口对应断言名称
		:return:
		'''
		
		return self.get_interface_data(interface_name=interface_name,
		                               assert_name=assert_name,
		                               yaml_config_key=YAML_CONFIG_KEY.CASE_DES)
	
	def get_interface_json_path(self, interface_name, assert_name):
		
		'''
		获取用例jsonpath
		:param interface_name: 接口名称
		:param assert_name: 接口对应断言名
		:return:
		'''
		
		return self.get_interface_data(interface_name=interface_name,
		                               assert_name=assert_name,
		                               yaml_config_key=YAML_CONFIG_KEY.CASE_JSON_EXPR)
	
	def get_interface_url_host_key(self, url: str):
		
		'''
		获取URL对应HOST key值
		:param url: url
		:return:
		'''
		
		object_host_dict = self.yaml_data[YAML_CONFIG_KEY.OBJECT_HOST]
		url_netloc = urlparse(url).netloc
		for key, value in object_host_dict.items():
			
			if operator.eq(urlparse(value).netloc, url_netloc):
				return key
	
	def get_interface_url_interface_name(self, host_key: str):
		'''
		通过hostkey获取接口名称
		:param host_key:
		:return:
		'''
		
		for interface_name, value in self.yaml_data.items():
			if value.__contains__(host_key) and operator.ne(interface_name, YAML_CONFIG_KEY.OBJECT_HOST):
				return interface_name
	
	def get_interface_response_data(self):
		'''
		获取接口返回值
		:return:
		'''
		return self.response_data
	
	def get_send_error_info_url(self):
		'''
		获取项目配置钉钉机器人URL
		:return:
		'''
		return self.yaml_data[YAML_CONFIG_KEY.DING_TALK_URL]
	
	def get_interface_assert_name(self, assert_value: dict):
		'''
		获取接口断言key
		:param assert_value: 断言值
		:return:
		'''
	
	def get_interface_setup_list(self, interface_name, assert_name):
		'''
		获取用例前置操作
		:param interface_name:
		:param assert_name:
		:return:
		'''
		return self.get_interface_data(interface_name=interface_name,
		                               assert_name=assert_name,
		                               yaml_config_key=YAML_CONFIG_KEY.CASE_SETUP)
	
	def get_interface_teardown_list(self, interface_name, assert_name):
		'''
		用例后置操作
		:return:
		'''
		
		return self.get_interface_data(interface_name=interface_name,
		                               assert_name=assert_name,
		                               yaml_config_key=YAML_CONFIG_KEY.CASE_TEARDOWN)
	
	def get_interface_request_header(self, interface_name, assert_name):
		
		'''
		获取接口请求header
		:param interface_name: 接口名称
		:param assert_name:
		:return:
		'''
		
		return self.get_interface_data(interface_name=interface_name,
		                               assert_name=assert_name,
		                               yaml_config_key=YAML_CONFIG_KEY.INTERFACE_REQUEST_HEADERS)
	
	def update_interface_json_path(self, interface_name, assert_name, new_value: dict = None):
		'''
		修改json_path 路径
		:param interface_name: 接口名称
		:param assert_name: 断言名称
		:param new_value: 修改值，以字典传入
		:return:
		'''
		old_json_path = self.get_interface_json_path(interface_name=interface_name,
		                                             assert_name=assert_name)
		if new_value is None:return old_json_path
		old_json_path.format(**new_value)
		
		return old_json_path
	
	def update_interface_request_data(self, interface_name, assert_name, new_request_data: dict):
		'''
		修改接口请求参数
		:param interface_name: 接口名称
		:param assert_name: 断言名称
		:param new_request_data: 新接口请求值
		'''
		
		old_interface_request_data = self.get_interface_request_data(interface_name=interface_name,
		                                                             assert_name=assert_name)
		
		if old_interface_request_data != None:
			old_interface_request_data.update(new_request_data)
	
	def save_response_data(self,response):
	    '''
	    保存接口返回值
	    :param dic:
	    :return:
	    '''
	
	    if isinstance(response, dict):
		
		    json_value = response
	
	    else:
		
		    name_list = urlparse(response.request.url).path.split('/')
		    name_list = name_list[len(name_list) - 2:]
		    name_list[-1] = name_list[-1].replace('.', '-')
		    json_key = '-'.join(name_list)
		    json_value = {json_key: self.parse_response_data(response_data=response)}
		    
	    YamlSingleton().update_response_data(response=json_value)

	def parse_response_data(self,response_data):
	    '''
	    解析接口返回对象为json
	    :param response_data:
	    :return:
	    '''
	    if isinstance(response_data,dict):

	        return response_data
	    
	    return response_data.json()
	
	def recursive_replace_json_expr(self, replace_value):
		'''
		递归替换请求数据内json_expr
		:param replace_value:
		:return:
		'''
		if isinstance(replace_value, dict):
			
			for key, value in replace_value.items():
				if type(value) != dict or type(value) != list:
					if isinstance(value, str) and value.find('$') != -1:
						replace_value[key] = self.find_json_expr_value(value)
				
				self.recursive_replace_json_expr(value)
		
		elif isinstance(replace_value, list):
			
			for index, list_value in enumerate(replace_value):
				if type(list_value) != dict or type(list_value) != list:
					if isinstance(list_value, str) and list_value.find('$') != -1:
						replace_value[index] = self.find_json_expr_value(list_value)
				
				self.recursive_replace_json_expr(list_value)
	
	def find_json_expr_value(self, json_expr):
		'''
		查找json_expr 返回值
		:param json_expr:
		:return:
		'''
		index = None
		temp_json_expr = json_expr
		if json_expr.find('/') != -1:
			index = int(json_expr.split('/')[-1])
			json_expr = json_expr.split('/')[0]
		
		if jsonpath.jsonpath(self.get_interface_response_data(), json_expr):
			
			json_value = jsonpath.jsonpath(self.response_data, json_expr)
		
		elif jsonpath.jsonpath(self.yaml_data, json_expr):
			
			json_value = jsonpath.jsonpath(self.yaml_data, json_expr)
		
		else:
			
			warnings.warn('未查找到json_expr值{json_expr}'.format(json_expr=json_expr))
			
			return json_expr
		
		if temp_json_expr.find('/') != -1:
			return json_value[index]
		
		return json_value
	
	def find_compare_data(self,response_data,json_expr):
		
		if json_expr is None:return
		
		if json_expr.find('/') != -1:
			json_expr_list = json_expr.split('/')
			json_expr_index = json_expr_list[-1]
			json_expr = json_expr_list[0]
			
		response_json = self.parse_response_data(response_data=response_data)
		
		find_expr_value = jsonpath.jsonpath(response_json,json_expr)
		
		if json_expr_index is None:
			return find_expr_value
			
		return find_expr_value[json_expr_index]
	


if __name__ == '__main__':
	data = ParsingData()
	
	print(data.get_interface_request_data(interface_name='getInitInfo',
	                                      assert_name='assert_user_info'))
