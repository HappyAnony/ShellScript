变量
=================

变量是一种逻辑概念，变量有三要素(也可称为三种属性)

- 数据类型：变量存储数据的类型；用来确定该变量存储数据的内存大小以及存储数据所能支持的运算操作(解释器执行解释)
- 变量类型：变量名的类型；用来确定该变量的作用域以及生命周期(关键字修饰决定)
- 变量名：访问变量存储的数据；用来访问一段可读可写的连续内存空间(自定义命名)

其中数据类型属性将在\ `数据类型 <../2-datatype/index.html>`_\ 一章内容介绍

在本章内容中主要介绍

- \ `变量名 <#varnamel>`_\ 
- \ `变量类型 <#vartypel>`_\ 

	- \ `本地变量 <#locall>`_\ 
	- \ `局部变量 <#sidel>`_\ 
	- \ `环境变量 <#envl>`_\ 
	- \ `位置变量 <#positionl>`_\ 
	- \ `特殊变量 <#speciall>`_\ 
	- \ `变量属性 <#propertyl>`_\ 
	- \ `变量赋值 <#varassignl>`_\ 

.. _varnamel:

0x00 变量名
~~~~~~~~~~~~

变量是通过变量名进行声明、定义、赋值和引用；变量存在于内存中，对于shell变量而言，设置或修改变量属性以及变量值时，不需要带\ ``$``\ ，只有引用变量的值时才使用\ ``$``\ 

变量名的本质是：一段可读可写的连续内存空间的别名

通过对变量名的引用就可以读写访问连续的内存空间

变量名的命名须遵循如下规则：

- 命名只能使用英文字母，数字和下划线，首个字符不能以数字开头
- 中间不能有空格，可以使用下划线\ ``_``\ 
- 不能使用标点符号
- 不能使用\ ``bash``\ 内嵌的关键字(可用\ ``help``\ 命令查看保留关键字)
- 不能使用\ `shell命令 <http://codetoolchains.readthedocs.io/en/latest/4-Linux/2-shellcmd/index.html>`_\ 

.. _vartypel:

0x01 变量类型
~~~~~~~~~~~~~~~

shell脚本是弱类型解释型的语言，变量类型由不同关键字声明决定；根据变量类型可将变量分为：(变量类型即变量名的类型，它决定变量的作用域以及定义引用的方式)

	- 本地变量
	- 局部变量
	- 环境变量
	- 位置变量
	- 特殊变量
	- 变量属性


.. _locall:

0x0100 本地变量
^^^^^^^^^^^^^^^^^

本地变量可以理解为全局变量，它的作用域为：只对当前shell进程有效，对其子shell以及其他shell都无效

该类型变量的声明定义方式为：\ ``[set]Var_Name=Value``\ 

- \ ``set``\ 关键字可以省略
- 等号左右没有空格；如果有空格就是进行比较运算符的比较运算
- 该变量可以声明定义在脚本的任何地方
- 变量Var_Name可以是任意数据类型

该类型变量的引用方式(获取变量的值)为：\ ``$Var_Name``\ 或\ ``${Var_Name}``\ 

- 可以在脚本的任意地方引用

该类型变量的赋值方式(修改变量的值)为：\ ``Var_Name=Value``\ 

- 在脚本中任意地方的赋值都会覆盖之前的变量值

该类型变量的撤销释放方式为：\ ``unset Var_Name``\ 

- 变量名前不加前缀\ ``$``\ 
- 撤销该变量后，引用该变量就会为空

需要注意的是：

- 如果使用\ ``readonly``\ 关键字修饰变量\ ``Var_Name``\ ，即\ ``readonly Var_Name[=Value]``\ ，此时将无法修改变量值也无法unset变量
- 不接收任何参数的\ ``set``\ 或者\ ``declare``\ 关键字命令，将会输出当前所有有效的本地变量、局部变量和环境变量

示例程序如下

.. code-block:: sh

	#!/bin/bash

	test_str="hello world"
	readonly ro_str="test"
	test_one(){
	        echo "test_str in test_one is $test_str"
	        test_str="happy"
	        test_name="anony"
	        unset test_set    # 撤销变量test_set，之后引用该变量就会为空
	        echo "test_set in test_one is $test_set"
	        ro_str="tset"     # 该变量被readonly修饰，不能修改其变量值，将会出现语法错误，直接退出函数，不执行下列命令
	        echo "ro_str"     # 上述直接退出函数，该命令不会执行
	}

	test_two()
	{
	        echo "test_str in test_two is $test_str"
	        echo "test_name in test_two is $test_name"
	        echo "test_set in test_two is $test_set"

	}

	test_one
	test_two

	# 执行结果如下
	# test_str in test_one is hello world
	# test_set in test_one is               # echo显示为空
	# ./demo.sh: line 9: ro_str: readonly variable
	# test_str in test_two is happy
	# test_name in test_two is anony
	# test_set in test_two is               # echo显示为空


.. _sidel:

0x0101 局部变量
^^^^^^^^^^^^^^^^^

局部变量的作用域为：只对变量声明定义所在函数内有效

该类型变量的声明定义方式为：\ ``loca Var_Name=Value``\ 

- \ ``local``\ 关键字不能省略，否则就是本地全局变量
- 等号左右没有空格；如果有空格就是进行比较运算符的比较运算
- 该变量只能声明定义在函数体内，否则会语法报错
- 变量Var_Name可以是任意数据类型

该类型变量的引用方式(获取变量的值)为：\ ``$Var_Name``\ 或\ ``${Var_Name}``\ 

- 只能在声明定义的函数体内引用，其它地方引用将为空

该类型变量的赋值方式(修改变量的值)为：\ ``Var_Name=Value``\ 

该类型变量的撤销释放方式为：\ ``unset Var_Name``\ 

- 变量名前不加前缀\ ``$``\ 
- 撤销该变量后，引用该变量就会为空

需要注意的是：

- 如果使用\ ``readonly``\ 关键字修饰变量\ ``Var_Name``\ ，即\ ``readonly Var_Name[=Value]``\ ，此时将无法修改变量值也无法unset变量
- 不接收任何参数的\ ``set``\ 或者\ ``declare``\ 关键字命令，将会输出当前所有有效的本地变量、局部变量和环境变量

示例程序如下

.. code-block:: sh

	#!/bin/bash

	test_str="anony"
	test_one(){
	        local test_str="happy"   # 局部变量test_str会覆盖全局变量test_str
	        local test_local="test"
	        echo "test_str in test_one is $test_str"
	        echo "test_local in test_one is $test_local"
	        unset test_str          # 只会撤销局部变量test_str，不会撤销全局变量test_str
	}

	test_two()
	{
	        echo "test_str in test_two is $test_str"      # unset没有撤销全局变量test_str
	        echo "test_local in test_two is $test_local"  # test_local是定义在test_one函数中的局部变量，该处引用将会为空

	}

	test_one
	test_two

	# 执行结果如下
	# test_str in test_one is happy
	# test_local in test_one is test
	# test_str in test_two is anony
	# test_local in test_two is 


.. _envl:

0x0102 环境变量
^^^^^^^^^^^^^^^^^

环境变量可以用来

- 定义bash的工作特性
- 保存当前会话的属性信息

关于环境变量的生命周期和作用域可以参考：\ `bash环境配置 <../../../1-shellenv/1-shellsoft/index.html>`_\

shell环境变量有两种来源

- 系统环境变量

	- 该环境变量已经由bash定义初始化，不用重新声明定义，只要引用就可以

		- 使用\ ``env``\ 、\ ``export``\ 、\ ``set``\ 、\ ``declare``\ 或\ ``printenv``\ 可以查看当前用户的环境变量(包括系统环境变量和自定义环境变量)，以下列出部分bash默认系统环境变量(\ ``set``\ 和\ ``declare``\ 可以查看所有环境变量，其它三个命令只能查看部分环境变量)

			- \ ``$BASH``\ ：bash二进制程序文件的路径
			- \ ``$BASH_SUBSHELL``\ ：子shell的层次说明，说明用户在哪一个层次中
			- \ ``$BASH_VERSION``\ ：bash的版本
			- \ ``$EDITOR``\ ：指定默认编辑器
			- \ ``$EUID``\ ：有效的用户ID
			- \ ``$UID``\ ：当前用户的ID号
			- \ ``$USER``\ ：当前用户名
			- \ ``$PATH``\ ：自动搜索路径
			- \ ``$LANG``\ ：系统使用语系
			- \ ``LOGNAME``\ ：当前登录的用户
			- \ ``$FUNCNAME``\ ：当前函数的名称，在函数中引用想判断自己是什么函数
			- \ ``$GROUPS``\ ：当前用户所属的组
			- \ ``$HOME``\ ：当前用户的家目录
			- \ ``$HOSTTYPE``\ ：主机架构类型，用来识别系统硬件平台
			- \ ``$MACHTYPE``\ ：平台类型，系统平台依赖的编译平台
			- \ ``$OSTYPE``\ ：OS系统类型
			- \ ``$IFS``\ ：输入数据时的默认字段分隔符，默认是空白符(空格、制表符、换行符)
			- \ ``$OLDPWD``\ ：上次使用的目录
			- \ ``$PWD``\ ：当前目录
			- \ ``$PPID``\ ：父进程
			- \ ``$PS1``\ ：主提示符，即bash命令窗口提示符
			- \ ``$PS2``\ ：第二提示符，主要用于补充完全命令输入时的提示符
			- \ ``$PS3``\ ：第三提示符，用于select命令中
			- \ ``$PS4``\ ：第四提示符，当使用-X选项调用脚本时，显示的提示符，默认为+号
			- \ ``$SECONDS``\ ：当前脚本已经运行的时长，单位为秒
			- \ ``$SHLVL``\ ：shell的级别，bash被嵌入的深度
		- 系统环境变量常用大写字母表示
	- 系统环境变量作用域

		- 执行脚本前，原始系统环境变量对当前用户所有shell进程(包含不同终端bash进程以及其子shell进程)都有效
		- 执行脚本时，系统环境变量对当前shell进程以及子shell进程都有效
		- 执行脚本后

			- 如果使用source命令执行脚本，修改后的系统环境变量会覆盖之前的系统环境变量，但是修改后的变量值只对当前终端bash进程以及其子shell进程才有效；原始变量值依然对当前用户所有shell进程(包含不同终端bash进程以及其子shell进程)都有效
			- 如果使用\ ``./demo.sh``\ 和\ ``bash demo.sh``\ 执行脚本，修改后的系统环境变量不会覆盖之前的系统环境变量，即所以系统环境变量依然保持原值，依然对当前用户所有shell进程(包含不同终端bash进程以及其子shell进程)都有效
- 自定义环境变量

	- 该环境变量是使用\ ``export``\ 命令将全局变量或局部变量导出成环境变量，需要手动声明定义

		- 方式一：\ ``export Var_Name=Value``\ 
		- 方式二：\ ``Var_Name=Value``\ 、\ ``export Var_Name``\ 
		- 自定义环境变量名尽量避免与系统环境变量名冲突；等号左右没有空格；如果有空格就是进行比较运算符的比较运算
		- 变量\ ``Var_Name``\ 可以是全局变量或局部变量，也可以是任意数据类型
	- 自定义环境变量作用域

		- 执行脚本时，自定义环境变量才被声明定义，同时继承全局变量或局部变量的作用域
		- 执行脚本后

			- 如果使用\ ``./demo.sh``\ 和\ ``bash demo.sh``\ 执行脚本，自定义环境变量不会导出成系统环境变量，即脚本执行完胡，该类环境变量会自动撤销
			- 如果使用\ ``source demo.sh``\ 执行脚本，只有全局环境变量才能导出成bash环境变量，局部环境变量会自动被撤销；但是导出后的全局环境变量只对当前终端bash进程以及其子shell进程才有效

不管是系统环境变量还是自定义环境变量都可以通过以下方式进行引用(获取环境变量的值)：\ ``$Var_Name``\ 或\ ``${Var_Name}``\ 

- 在环境变量的作用域之内引用
- 变量名\ ``Var_Name``\ 可以是系统环境变量名，又可以是自定义环境变量名

不管是系统环境变量还是自定义环境变量都可以通过以下方式进行赋值(修改环境变量的值)：对当前shell进程来说通过该方式赋值修改的环境变量继承之前的作用域

- 方式一：\ ``export Var_Name=Value``\ 
- 方式二：\ ``Var_Name=Value``\ 、\ ``export Var_Name``\ 


不管是系统环境变量还是自定义环境变量都可以通过下列方式进行撤销释放：\ ``unset Var_Name``\ 

- 变量名前不加前缀\ ``$``\ 
- 撤销该变量后，引用该变量就会为空

需要注意的是：

- 如果使用\ ``readonly``\ 关键字修饰变量\ ``Var_Name``\ ，即\ ``readonly Var_Name[=Value]``\ ，此时将无法修改变量值也无法unset变量
- 不接收任何参数的\ ``set``\ 或者\ ``declare``\ 关键字命令，将会输出当前所有有效的本地变量、局部变量和环境变量


示例程序如下

.. code-block:: sh

	#!/bin/bash

	test_one(){
	        PATH=./:$PATH            # 修改系统环境变量的值
	        export PATH              # 导出系统环境变量使其生效
	        export MYNAME="anony"    # 将全局变量导出成环境变量
	        local MYSEX="man"        # 定义局部变量
	        export MYSEX             # 将局部变量导出成环境变量
	        export MYBLOG="blog"
	        export MYAGE="22"
	        echo "PATH in test_one is $PATH"      # 上述所有定义的环境变量都有效
	        echo "MYNAME in test_one is $MYNAME"
	        echo "MYSEX in test_one is $MYSEX"
	        echo "MYBLOG in test_one is $MYBLOG"
	        echo "MYAGE in test_one is $MYAGE"
	        unset MYBLOG             # 撤销全局变量导出成的环境变量
	        readonly MYAGE           # 将全局变量导出成的环境变量修改为只读变量
	        MYAGE="23"               # 对只读变量进行赋值修改会造成语法错误
	}

	test_two()
	{
	        echo "PATH in test_two is $PATH"          # 系统变量的作用域
	        echo "MYNAME in test_two is $MYNAME"      # 全局环境变量的作用域
	        echo "MYSEX in test_two is $MYSEX"        # 局部环境变量的作用域
	        echo "MYBLOG in test_two is $MYBLOG"      # 全局环境变量已经撤销
	        echo "MYAGE in test_two is $MYAGE"        # 全局环境变量只读
	}

	test_one
	test_two


	# 执行结果如下
	# PATH in test_one is ./:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
	# MYNAME in test_one is anony
	# MYSEX in test_one is man
	# MYBLOG in test_one is blog
	# MYAGE in test_one is 22
	# ./demo.sh: line 20: MYAGE: readonly variable
	# PATH in test_two is ./:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
	# MYNAME in test_two is anony
	# MYSEX in test_two is 
	# MYBLOG in test_two is 
	# MYAGE in test_two is 22


.. _positionl:

0x0103 位置变量
^^^^^^^^^^^^^^^^^

位置变量无需声明定义，直接引用即可；该变量也不能被赋值修改，甚至不能被unset撤销

位置变量是用来实现

- 在函数体外直接引用脚本的传入参数，它引用方式如下

	- \ ``$0``\ ：引用脚本名
	- \ ``$1``\ ：引用脚本的第1个传入参数
	- \ ``$n``\ ：引用脚本的第n个传入参数
- 在函数体内直接引用函数的传入参数，它引用方式如下

	- \ ``$0``\ ：引用脚本名
	- \ ``$1``\ ：引用函数的第1个传入参数
	- \ ``$n``\ ：引用函数的第n个传入参数

示例程序如下

.. code-block:: sh

	#!/bin/bash
	echo "script name is $0"

	echo "the script first arg is $1"  # 引用脚本的第一个传入参数
	test(){
	        echo "script name is $0"
	        echo "the func first arg in test is $1" # 引用函数的第一个传入参数，不是脚本的第一个参数
	}
	test 26

	# 执行结果如下：./test.sh 12
	# script name is ./test.sh
	# the script first arg is 12
	# script name is ./test.sh
	# the func first arg in test is 26


.. _speciall:

0x0104 特殊变量
^^^^^^^^^^^^^^^^^

特殊变量也无需声明定义，直接引用即可；该变量也不能被赋值修改，甚至不能被unset撤销

特殊变量的引用方式如下

- \ ``$?``\ ：引用上一条命令的执行状态返回值，状态用数字表示：0-255

	- \ ``0``\ ：表示成功
	- \ ``1-255``\ ：表示失败；需要注意的是\ ``1/2/127/255``\ 是系统预留的，自己写脚本时要避开与这些值重复
- \ ``$$``\ ：引用当前shell的PID。除了执行bash命令和shell脚本时，$$不会继承父shell的值，其他类型的子shell都继承
- \ ``$BASHPID``\ ：引用当前shell的PID，这和\ ``$$``\ 是不同的，因为每个shell的$BASHPID是独立的，而\ ``$$``\ 有时候会继承父shell的值
- \ ``$!``\ ：引用最近一次执行的后台进程PID，即运行于后台的最后一个作业的PID
- \ ``$#``\ ：引用所有位置参数的个数
- \ ``$*``\ ：引用所有位置参数的整体，即所有参数被当做一个字符串
- \ ``$@``\ ：引用所有单个位置参数，即每个参数都是一个独立的字符串
- \ ``$_``\ ：引用上一条命令的最后一个参数的值
- \ ``$-``\ ：引用传递给脚本的标记

示例程序如下

.. code-block:: sh

	#!/bin/bash

	echo '$# is:'$#
	echo '$* is:'$*
	echo '$@ is:'$@
	echo '$! is:'$!
	echo '$$ is:'$$
	echo '$BASHPID is:'$BASHPID
	echo '$? is:'$?
	test(){
	        echo '$# in func is:'$#
	        echo '$* in func is:'$*
	        echo '$@ in func is:'$@
	        echo '$! in func is:'$!
	        echo '$$ in func is:'$$
	        echo '$BASHPID in func is:'$BASHPID
	        echo '$? in func is:'$?
	}
	test 26 23 47

	# 执行结果如下：[root@localhost ~]# ./test.sh 1 3 4 5 6 7
	# $# is:6
	# $* is:1 3 4 5 6 7
	# $@ is:1 3 4 5 6 7
	# $! is:
	# $$ is:4002
	# $BASHPID is:4002
	# $? is:0
	# $# in func is:3
	# $* in func is:26 23 47
	# $@ in func is:26 23 47
	# $! in func is:
	# $$ in func is:4002
	# $BASHPID in func is:4002
	# $? in func is:0


.. _propertyl:

0x0105 变量属性
^^^^^^^^^^^^^^^^^

此处的变量属性是指\ ``数据类型``\ 和\ ``变量类型``\ ，这两个属性可以通过相关命令关键字进行修改，例如：

\ ``Var_Name=Value``\ 语句中声明定义的变量\ ``Var_Name``\ 默认的数据类型是\ ``字符串类型``\ ，变量类型是\ ``本地全局变量``\ 

- \ ``local Var_Name``\ 声明该变量为局部变量
- \ ``export Var_Name``\ 声明该变量为环境变量
- \ ``declare -x Var_Name``\ 声明该变量为环境变量
- \ ``declare +x Var_Name``\ 取消该变量的环境变量属性
- \ ``declare -i Var_Name``\ 声明该变量为整型变量
- \ ``declare +i Var_Name``\ 取消该变量的整型变量属性
- \ ``declare -p Var_Name``\ 显式指定变量被声明的类型
- \ ``declare -r Var_Name``\ 声明该变量为只读变量，不能撤销，不能修改，相当于readonly，只有当前进程终止才消失
- \ ``declare +r Var_Name``\ 取消该变量的只读变量属性

可以使用\ ``man declare``\ 查看\ ``declare``\ 命令的详细使用方法


.. _varassignl:

0x0106 变量赋值
^^^^^^^^^^^^^^^^^^

除了上述介绍的\ ``Var_Name=Value``\ 赋值方式，还有以下变量赋值的方式，以下赋值方式常用来给变量赋默认值

- \ ``${var:-default}``\ ：如果var没有声明或者声明了为空，则返回default代表的值；如果var声明了不为空，则返回var代表的值
- \ ``${var-default}``\ ：如果var没有声明，则返回default代表的值；如果var声明了但是为空，则返回null；如果var声明了不为空，则返回var代表的值
- \ ``${var:+default}``\ ：如果var没有声明或者声明了为空，不做任何操作，返回空；如果var声明了不为空，则返回default代表的值
- \ ``${var:=default}``\ ：如果var没有声明或者声明了为空，则返回default代表的值，并将default的值赋值给var；如果var声明了不为空，则返回var代表的值
- \ ``${var:?default}``\ ：如果var没有声明或者声明了为空，则以default为错误信息返回；如果var声明了不为空，则返回var代表的值