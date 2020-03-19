#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Time   : 2020-03-18 23:40
# Author : fyt
# File   : apiData.py

import ytApiTest
import os,yaml,operator

class YAML_CONFIG_KEY():

    OBJECT_HOST = 'OBJECT_HOST'
    INTERFACE_URL = 'url'
    INTERFACE_REQUEST_DATA = 'req_data'
    INTERFACE_ASSERT_DATA = 'ast_data'
    INTERFACE_CASE_DES = 'des'
    DING_TALK_URL = 'DING_TALK_URL'



class FindFile():

    def get_yaml_path(self):

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

        assert yaml_file_path ,AssertionError('未找到yaml数据文件')

        with open(yaml_file_path, encoding='UTF-8') as f:
            dic = yaml.load(f, Loader=yaml.FullLoader)
            return dic

    def update_response_data(self,response:dict):
        '''
        更新接口返回数据
        '''
        self.res_data.update(response)

class ParsingData():

    def __init__(self):

        self.yaml_data = YamlSingleton().yaml_data


    def get_object_host(self,host_key:str = None):
        '''
        获取项目host ，默认返回第一个HOST
        :param host_key:
        :return:
        '''
        if operator.eq(host_key,None):

            return iter(self.yaml_data[YAML_CONFIG_KEY.OBJECT_HOST].values()).__next__()

        else:

            if self.yaml_data[YAML_CONFIG_KEY.OBJECT_HOST].__contains__(host_key):

                return self.yaml_data[YAML_CONFIG_KEY.OBJECT_HOST][host_key]

    def get_interface_url(self,interface_name:str,host_key:str = None):
        '''
        获取接口URL路径
        :param interface_name: 接口名称
        :param host_key: 项目host_key
        :return:
        '''
        if self.yaml_data.__contains__(interface_name):

            url = self.yaml_data[interface_name]

            if url.find('http') != -1:

                return url

            else:

                return self.get_object_host(host_key=host_key) + url

    def get_interface_request_data(self,interface_name,assert_name):
        '''
        获取接口请求数据
        :param interface_name: 接口名称
        :param assert_name: 断言名称
        :return:
        '''

        if self.yaml_data.__contains__(interface_name) and self.yaml_data.__contains__(assert_name):

            if self.yaml_data.__contains__(YAML_CONFIG_KEY.INTERFACE_ASSERT_DATA):

                return self.yaml_data[interface_name][assert_name][YAML_CONFIG_KEY.INTERFACE_ASSERT_DATA]

    

if __name__ == '__main__':

    p = ParsingData()
    print(p.get_object_host(host_key='CMS'))

