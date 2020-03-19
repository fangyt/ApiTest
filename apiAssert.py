#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
# Time   : 2020-03-18 23:40
# Author : fyt
# File   : apiAssert.py



class AssertException(AssertionError):

    def __init__(self, errorInfo):
        self.errorInfo = str(errorInfo)

    def __str__(self):
        return self.errorInfo


def send_error_info(error_info):

    return error_info

if __name__ == '__main__':


    assert 1 == 2,AssertionError('1 != 2')