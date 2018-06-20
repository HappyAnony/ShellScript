脚本结构
=================

我们在学习每一种编程语言时，都会先学习写一个\ ``hello world``\ 的demo程序，下面我们将从这个小demo程序来窥探一下我们\ ``shell脚本``\ 的程序结构

.. code-block:: sh

	#!/bin/bash

	# 注释信息

	echo_str="hello world"

	test(){
	        echo $echo_str
	}

	test echo_str

首先我们可以通过\ `文本编辑器 <http://codetoolchains.readthedocs.io/en/latest/1-TextEdit/index.html>`_\ (在这里我们使用linux自带\ `文本编辑神器vim <http://codetoolchains.readthedocs.io/en/latest/1-TextEdit/2-vim/index.html>`_\ )，新建一个文件\ ``demo.sh``\ ，文件扩展名\ ``sh``\ 代表\ ``shell``\ ，表明该文件是一个\ ``shell脚本文件``\ ，并不影响脚本的执行，然后将上述代码片段写入文件中，保存退出

然后使用\ ``bash -n demo.sh``\ 命令可以检测刚才脚本文件的语法是否错误，如果没有回显结果就代表脚本文件没有语法错误


关于上述脚本文件中的代码语法，这里我们简单说明下，详细说明介绍将在下述文档中一一展开

- 脚本都以\ ``#!/bin/bash``\ 开头，\ ``#``\ 称为\ ``sharp``\ ，\ ``!``\ 在unix行话里称为\ ``bang``\ ，合起来简称就是常见的\ ``shabang``\ 。\ ``#!/bin/bash`` 指定了shell脚本解释器bash的路径，即使用\ ``bash``\ 程序作为该脚本文件的解释器，当然也可以使用其它的解释器\ ``/bin/sh``\ 等，根据具体环境进行相应选择
- \ ``echo_str``\ 是字符串变量，通过\ ``$``\ 进行引用变量的值，
- \ ``test``\ 是自定义函数名，通过\ ``函数名 传入参数``\ 格式进行函数的调用
- \ ``echo``\ 是shell命令，相对于c中的\ ``printf``\ 
- \ ``#``\ 字符用来注释shell脚本的

最后可以使用下列两种方式执行上述脚本

- 将脚本作为bash解释器的参数执行：此时首行的\ ``#!/bin/bash``\ shabang可以不用写

	- \ ``bash demo.sh``\ ：直接将脚本文件作为bash命令的参数
	- \ ``bash -x demo.sh``\ ：使用\ ``-x``\ 参数可以查看脚本的详细执行过程
- 将脚本作为独立的可执行文件执行：此时首行的\ ``#!/bin/bash``\ shabang必须写，用来指定shell解释器路径；同时脚本必须可执行权限

	- \ ``chmod +x demo.sh``\ ：给脚本添加执行权限
	- \ ``./demo.sh``\ ：执行脚本文件，在这里需要使用\ ``./demo.sh``\ 表明当前目录下脚本，因为\ ``PATH``\ 环境变量中没有当前目录，写成\ ``demo.sh``\ 系统会去\ ``/sbin、/sbin``\ 等目录下查找该脚本，无法找到该脚本文件执行，造成报错


