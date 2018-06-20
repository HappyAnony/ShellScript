知识碎片
=================

shell脚本是一种纯面向过程的脚本编程语言

在编写shell脚本时，需要注意以下几点

- 标准输出：在编写shell脚本的时候，要考虑下该命令语句是否存在标准输出

	- 如果有，是否需要输出到标准输出设备上
	- 如果不需要，那就输出重定向至\ ``/dev/null``\ 
- 常见逻辑错误

	- 用户输入是否为空问题
	- 用户输入字符串大小写问题
	- 用户输入是否存在问题
- 编程思想

	- 明确脚本的输入、输出是什么
	- 根据输入考虑可能存在逻辑错误的地方
	- 根据输出判断使用什么控制流程
	- 在保证功能实现的前提下进行优化精简代码


在编写shell脚本时，常用到的一些命令语句

- 判断用户是否存在

	- \ ``grep "^$userName\>" /etc/passwd &> /dev/null``\ 
	- \ ``id $userName``\ 
- 获取用户的相关信息(用户名，UID，GID或者默认shell)

	- 对\ ``/etc/passwd``\ 文件进行处理
	- 使用\ ``id``\ 命令

- 脚本文件中导入调用其它脚本文件

    - \ ``source config_file``\ 
    - \ ``. config_file``\ 

.. code-block:: sh

	#!/bin/bash
	# configurefile: /tmp/script/myscript.conf

	# 先判断对导入文件是否有读权限，然后尝试导入
	[ -r /tmp/script/myscript.conf ] && . /tmp/script/myscript.conf
	# 如果导入文件没有成功或者导入文件中对引用变量没有相关定义时，需定义默认值，防止出错
	userName=${userName:-testuser} 

	echo $userName

- 读取文件内容

.. code-block:: sh

	while read line; do
		CMD_LIST
	done < /path/to/somefile

- 下载文件

.. code-block:: sh

	#!/bin/bash

	url="http::/mirrors.aliyun.com/centos/centos6.5.repo"

	which wget &> /dev/null || exit 5 # 如果wget命令不存在就退出

	downloader=`which wget`  # 获取wget命令的二进制文件路径

	[ -x $downloader ] || exit 6 # 如果二进制文件没有执行权限就退出

	$downloader $url

- 创建临时文件或目录

.. code-block:: sh

	mktemp [-d] /tmp/file.XX   # X指定越多，随机生成的后缀就越长，其中-d表示创建临时目录
