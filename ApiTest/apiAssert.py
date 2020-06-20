#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Time   : 2020-03-18 23:40
# Author : fyt
# File   : apiAssert.py


from ApiTest.apiData import ParsingData
from ApiTest.apiRequest import InterFaceReq
import operator


class ApiAssert():
	
	def __init__(self):
		
		self.parsing_data = ParsingData()
		self.interface_req = InterFaceReq()
	
	def format_interface_info(self, **kwargs):
		
		title = kwargs.get('title')
		interface_name = kwargs.get('interface_name')
		assert_name = kwargs.get('assert_name')
		response = kwargs.get('response')
		
		des = self.parsing_data.get_interface_des(interface_name=interface_name,
		                                          assert_name=assert_name)
		interface_url = response.url
		json_expr = self.parsing_data.update_interface_json_path(interface_name=interface_name,
		                                                         assert_name=assert_name)
		response_json = response.json()
		assert_value = kwargs.get('assert_value')
		find_value = kwargs.get('find_value')
		params = response.request.body
		headers = response.request.headers
		info_dic = {'title': title,
		            'case_des': des,
		            'url': interface_url,
		            'json_expr': json_expr,
		            'response': response_json,
		            'assert': assert_value,
		            'find_value': find_value,
		            'params': params,
		            'headers': headers}
		
		info = '\n TITLE      =   {title}' \
		       '\n\n DES        =   {case_des}' \
		       '\n\n URL        =   {url}' \
		       '\n\n PARAMS     =   {params}' \
		       '\n\n JONS_EXPR  =   {json_expr}' \
		       '\n\n HEADERS    =   {headers}' \
		       '\n\n RESPONSE   =   {response}' \
		       '\n\n FIND_VALUE  =   {find_value}' \
		       '\n\n ASSERT_VALUE     =   {assert}'.format_map(info_dic)
		
		self.interface_req.send_case_error_info(error_info=info)
		
		return info
	
	def assert_eq(self, interface_name, assert_name, host_key=None):
		
		interface_rep = self.interface_req.post(interface_name=interface_name,
		                                        assert_name=assert_name,
		                                        host_key=host_key)
		
		interface_data = self.parsing_data.parse_response_data(response_data=interface_rep)
		
		assert_value = self.parsing_data.get_interface_assert_value(interface_name=interface_name,
		                                                            assert_name=assert_name)
		
		self.compare_json_eq(response_data=interface_data,
		                     case_assert_data=assert_value,
		                     interface_name=interface_name,
		                     assert_name=assert_name,
		                     response=interface_rep)
	
	def compare_json_eq(self, response_data, case_assert_data, **kwargs):
		'''
		比较json
		:return:
		'''
		
		if isinstance(case_assert_data, dict):
			
			for key, dic_value in case_assert_data.items():
				
				if operator.ne(dic_value, dict) and operator.ne(dic_value, list):
					assert operator.eq(dic_value, response_data[key]), \
						self.format_interface_info(title='字典比较错误',
						                           interface_name=kwargs.get('interface_name'),
						                           assert_name=kwargs.get('assert_name'),
						                           response=kwargs.get('response'),
						                           assert_value={key: dic_value},
						                           find_value={key: response_data[key]})
				
				self.compare_json_eq(response_data=response_data[key],
				                     case_assert_data=dic_value)
		
		elif isinstance(case_assert_data, list):
			
			for index, list_value in enumerate(case_assert_data):
				
				if operator.ne(list_value, dict) and operator.ne(list_value, dict):
					assert operator.eq(list_value, response_data[index]), self.format_interface_info(title='列表比较错误',
						                           interface_name=kwargs.get('interface_name'),
						                           assert_name=kwargs.get('assert_name'),
						                           response=kwargs.get('response'),
						                           assert_value=list_value,
						                           find_value=response_data[index])
				
				self.compare_json_eq(response_data=response_data[index],
				                     case_assert_data=list_value)


if __name__ == '__main__':
	ApiAssert().compare_json_eq({"data":0},{"data":None})
