项目介绍
==========================
此扩展包通过读取yaml文件配置接口请求参数
通过GET、POST方法获取接口返回值并断言

安装和使用
============

| 安装命令如下：

::

    pip install ApiTest

| 支持功能如下：

-  支持 yaml文件内请求参数或断言数据使用JOSNPATH语法获取接口返回值
-  支持 断言接口返回值所有字段是否与断言值相等
-  支持 断言失败发送对应错误接口信息到钉钉群
-  支持 用例前置、后置操作
-  支持 对用例指定用户做请求。


使用：
============

- 使用扩展包项目根目录下必须新建.yaml文件管理测试用例数据
- .yaml文件必须遵循以下格式并包含以下关键字

demo
=====

::

    DING_TALK_URL: <钉钉机器人URL>
    OBJECT_HOST: <项目host>
      MONKEY_HOST: <项目host1>
      PHONE_LOGIN_HOST: <项目host2>


    cms_host_login:
      url: <接口URL，必须配置>
      CMS_HOST:
        des: <用例说明，可选配置>

        headers: <用例请求头信息，可选配置>
          <key>: <value>

        req_data: <用例请求参数，必须配置>
          <key>: <value>

        ast_data: <用例断言参数，必须配置>
          <key>: <value>

        json_expr: <用例json_path_expr,可选配置>
          <key>: <value>

        setup: <用例前置请求>
          -
            interface_name:
            assert_name:
            host_key:

          -
            interface_name:
            assert_name:
            host_key:

        tearDown: <用例后置请求>
          -
            interface_name:
            assert_name:
            host_key:

          -
            interface_name:
            assert_name:
            host_key:





方法说明及使用示例
======================

.. code:: python

    #执行相等断言方法
    import ytApiTest
    assert_body_eq_assert_value(interface_name, assert_name, host_key=None)
    #参数说明：interface_name(.yaml你接口名称),assert_key(.yaml文件内与接口对应的assert_key值)
