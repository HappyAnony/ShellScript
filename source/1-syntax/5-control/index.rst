控制流程语句
=================

和其它编程语言一样，shell的控制流程语句大体上也分为三种

- \ `顺序执行语句 <#orderstate>`_\ 
- \ `条件执行语句 <#conditionstate>`_\ 

	- \ `if条件语句 <#ifconditon>`_\ 
	- \ `case条件语句 <#casecondition>`_\ 
	- \ `select条件语句 <#selectcondition>`_\ 
	- \ `条件测试表达式 <#conteststate>`_\ 

		- \ `整数测试表达式 <#intergtest>`_\ 
		- \ `字符测试表达式 <#chartest>`_\ 
		- \ `文件测试表达式 <#filetest>`_\ 
- \ `循环执行语句 <#loopstate>`_\ 
	- \ `for循环语句 <#forloop>`_\ 
	- \ `while循环语句 <#whileloop>`_\ 
	- \ `until循环语句 <#untilloop>`_\ 
	- \ `循环退出命令 <#loopexit>`_\ 

.. _orderstate:

0x00 顺序执行语句
~~~~~~~~~~~~~~~~~~~~

顺序执行语句是默认法则，即按照自上而下、自左往右的顺序逐条执行各命令，每执行一次就会得到对应的结果，然后退出该次执行操作

.. _conditionstate:

0x01 条件执行语句
~~~~~~~~~~~~~~~~~~~~

条件执行语句会根据判断条件选择符合条件的分支执行对应的\ ``cmd_list``\ 命令列表，执行完命令后就会退出该分支；条件执行语句有以下几种

- \ `if条件语句 <#ifconditon>`_\ 
- \ `case条件语句 <#casecondition>`_\ 
- \ `select条件语句 <#selectcondition>`_\ 

.. _ifconditon:

0x0100 if条件语句
^^^^^^^^^^^^^^^^^^

\ ``if条件语句``\ 的语法结构如下(使用\ ``help if``\ 命令可以查看)

.. code-block:: sh

	if TEST_COMMANDS; then
		COMMANDS_LIST;
	[elif TEST_COMMANDS; then
		COMMANDS_LIST;]
	...
	[else
		COMMANDS_LIST;]
	fi

其执行逻辑是

- \ **1.**\  先执行\ ``if``\ 分支下的\ ``TEST_COMMANDS``\ 条件测试命令，如果执行完的状态返回值为\ ``非0``\ ，则执行第2步；如果执行完的状态返回值为\ ``0``\ ，即\ ``TEST_COMMANDS``\ 条件测试命令执行成功，则执行该分支下的\ ``COMMANDS_LIST``\ 命令列表，执行完后就直接退出，此时整个if语句结构体的状态返回值取决于\ ``COMMANDS_LIST``\ 命令列表中最后一个命令的状态返回值
- \ **2.**\ 如果存在\ ``elif``\ 分支，则按照第一步的流程依次执行\ ``elif``\ 分支下的\ ``TEST_COMMANDS``\ 条件测试命令，如果没有一个\ ``elif``\ 分支的状态返回值为\ ``0``\ ，则执行第3步；如果存在一个\ ``elif``\ 分支的状态返回值为\ ``0``\ ，即该分支下的\ ``TEST_COMMANDS``\ 条件测试命令执行成功，则执行该分支下的\ ``COMMANDS_LIST``\ 命令列表，执行完后就直接退出，此时整个if语句结构体的状态返回值取决于\ ``COMMANDS_LIST``\ 命令列表中最后一个命令的状态返回值
- \ **3.**\ 如果\ ``else``\ 分支不存在，那么整个if语句结构体的状态返回值为\ ``0``\ ；如果存在\ ``else``\ 分支，则执行该分支下的\ ``COMMANDS_LIST``\ 命令列表，执行完后就直接退出，此时整个if语句结构体的状态返回值取决于\ ``COMMANDS_LIST``\ 命令列表中最后一个命令的状态返回值

在整个if语句结构体中有两个地方需要注意

- \ ``COMMANDS_LIST``\ ：表示待执行的命令列表，即一系列shell命令的集合，类型格式多种多样，在一系列示例代码中可见一斑

	- 注意：在命令列表中不能使用\ ``()``\ 操作符改变优先级，它的作用是让括号内的语句成为命令列表进入子shell中执行，它的具体作用可参考：\ `括号操作符 <../4-operator/index.html#parenthesel>`_\ 
- \ ``TEST_COMMANDS``\ ：表示条件测试命令，即通过引用条件测试命令的执行状态返回值是否为\ ``0``\ 来判断是否执行上述\ ``COMMANDS_LIST``\ 命令列表；\ **这里需要特别注意的是，和其它语言不通，shell的条件测试命令只有以下三种类型**\ 

	- \ ``命令执行``\ ：命令本身执行后就会产生对应的执行状态返回值，所以可以直接用来做条件判断

		- 此时不能使用\ **``**\ 操作符来引用命令，因为该操作引用的是命令的执行结果，而不是命令的执行状态返回值
		- 通常是直接使用命令，然后在命令后面添加\ ``s&> /dev/null``\ ，表示将命令的执行结果重定向至\ ``/dev/null``\ ，只引用其状态返回值；例如：\ ``if grep "^root" /etc/passwd &> /dev/null; then``\ 
	- \ ``执行条件测试表达式``\ ：在shell中，条件测试表达式是由条件测试操作符以及对应的操作数组成，详细介绍可参考下列：\ `条件测试表达式 <#conteststate>`_\ ，执行条件测试表达式有以下三种格式

		- \ ``test Test_Expression``\ ：通过\ ``test``\ 命令执行
		- \ ``[ Test_Expression ]``\ ：通过\ ``[]``\ 操作符执行，注意\ ``Test_Expression`` 前后有空格
		- \ ``[[ Test_Expression ]]``\ ：通过\ ``[[]]``\ 操作符执行，注意\ ``Test_Expression`` 前后有空格
	- \ ``组合条件测试``\ ：即对多个\ ``命令执行状态返回值``\ 或者\ ``执行条件测试表达式状态返回值``\ 做逻辑运算，组合条件测试有以下三种格式

		- 逻辑与操作：只有当\ ``&&``\ 操作符两边执行结果都为真(状态值为0)，最后组合条件测试结果才为真(状态值为0)

			- \ ``[ Test_Expression1 ] && [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND &> /dev/null && [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND1 &> /dev/null && COMMAND2 &> /dev/null &&``\ 
			- \ ``[ Test_Expression1 -a Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``[[ Test_Expression1 && Test_Expression2 ]]``\ ：此处只能使用\ ``[[]]``\ 操作符，因为\ ``&&``\ 运算符不允许用于\ ``[]``\ 操作符中
		- 逻辑或操作：只要\ ``||``\ 操作符两边执行结果有一个为真(状态值为0)，最后组合条件测试结果就为真(状态值为0)

			- \ ``[ Test_Expression1 ] || [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND &> /dev/null || [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND1 &> /dev/null || COMMAND2 &> /dev/null &&``\ 
			- \ ``[ Test_Expression1 -0 Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``[[ Test_Expression1 || Test_Expression2 ]]``\ ：此处只能使用\ ``[[]]``\ 操作符，因为\ ``||``\ 运算符不允许用于\ ``[]``\ 操作符中
		- 逻辑非操作：对\ ``!``\ 右侧执行结果取反

			- \ ``! [ Test_Expression ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``! COMMAND1 &> /dev/null``\ 
			- \ ``! ([ Test_Expression1 ] || [ Test_Expression2 ])``\ ：此处相当于\ ``! [ Test_Expression1 ] && ! [ Test_Expression2 ]``\ 
			- \ ``! ([ Test_Expression1 ] && [ Test_Expression2 ])``\ ：此处相当于\ ``! [ Test_Expression1 ] || ! [ Test_Expression2 ]``\ 
		- 注意：\ **非的优先级大于与，与的优先级大于或**\ 

示例代码如下

- 输出两个传入参数中的最大值

.. code-block:: sh

	#!/bin/bash
	if [ $# -lt 2 ]; then
	        echo "`basename $0` arg1 arg2"
	        exit 1
	fi
	if [ $1 -gt $2 ]; then
	        echo "the max num is $1"
	else
	        echo "the max num is $2"
	fi

- 计算1~200之间偶数之和

.. code-block:: sh

	#!/bin/bash

	declare -i sum=0
	for i in {1..200};do
	        if [ $[$i%2] -eq 0 ]; then
	                let sum+=$i
	        fi
	done

	echo "the sum is : $sum"


- 让用户输入一个用户名，先判断该用户是否存在，不存在，则以7为退出码；如果存在，判断用户的shell是否为\ ``/bin/bash``\ ，如果是，则显示为\ ``Bash User``\ ，退出码为0，否则显示为\ ``Not Bash User``\ ，退出码为1

.. code-block:: sh


	#!/bin/bash

	read -p "please input username: " username

	echo $username
	if ! grep "^$username\>" /etc/passwd &> /dev/null; then
	        echo "User not exist"
	        exit 7
	elif [[ `grep "^$username\>" /etc/passwd | cut -d: -f7` =~ /bin/bash ]];then
	        echo "Bash User"
	        exit 0
	else
	        echo "Not Bash User"
	        exit 1
	fi

- 统计输入文件的空白行数

.. code-block:: sh

	#!/bin/bash

	read -p "Enter a file path: " filename

	if grep "^$" $filename &> /dev/dull; then
	        linesCount=`grep "^$" $filename | wc -l`
	        echo "$filename has $linesCount space lines"
	else
	        echo "$filename has no space linse"
	fi

.. _casecondition:

0x0101 case条件语句
^^^^^^^^^^^^^^^^^^^^^^

\ ``case条件语句``\ 的语法结构如下(使用\ ``help case``\ 命令可以查看)

.. code-block:: sh

	case WORD in 
		PATTERN1) 
			COMMANDS_LIST
			;;
		PATTERN2)
			COMMANDS_LIST
			;;
		PATTERN3)
			COMMANDS_LIST
			;;
		... 
	esac

其执行逻辑是：\ ``WORD``\ 依次匹配\ ``PATTERN1``\ 、\ ``PATTERN2``\ 、\ ``PATTERN3``\ ......；如果所有模式都没有匹配上，则直接退出\ ``case``\ 语句，此时执行状态返回值为\ ``0``\ ；如果匹配上任意一个\ ``PATTERN``\ 就执行该分支下面的\ ``COMMANDS_LIST``\ 命令列表，执行完后就直接退出，此时整个case语句结构体的状态返回值取决于\ ``COMMANDS_LIST``\ 命令列表中最后一个命令的状态返回值；模式的匹配优先级是\ ``PATTERN1``\ > \ ``PATTERN2``\ > \ ``PATTERN3``\ > \ ``......``\ 

在以上结构中，有以下几点需要注意

- case中的每个小分支都以双分号\ ``;;``\ 结尾，表示执行完该分支后直接退出\ ``case``\ 语句；但最后一个小分句的双分号可以省略。实际上，小分句除了使用\ ``;;``\ 结尾，还可以使用\ ``;&``\ 和\ ``;;&``\ 结尾，只不过意义不同，如下

	- \ ``;;``\ 符号表示小分支执行完成后立即退出case语句
	- \ ``;&``\ 符号表示继续执行下一个小分支中的\ ``COMMANDS_LIST``\ 部分，而无需进行匹配动作，并由此小分支的结尾符号来决定是否继续操作下一个小分句
	- \ ``;;&``\ 符号表示继续向后(不止是下一个，而是一直向后)匹配小分支，如果匹配成功，则执行对应小分支中的\ ``COMMANDS_LIST``\ 部分，并由此小分支的结尾符号来决定是否继续向后匹配
- 每个小分支中的\ ``PATTERN``\ 部分都使用括号\ ``()``\ 包围，只不过左括号\ ``(``\ 不是必须的
- 一般最后一个小分支使用的\ ``PATTERN``\ 是\ ``*``\ ，表示无法匹配前面所有小分支时，将匹配该小分支；用来避免case语句无法匹配的情况，在shell脚本中，此小分支一般用于提示用户脚本的使用方法，即给出脚本的\ ``Usage``\ 

这里也需要说明下以下两个关键组成成分

- \ ``WORD``\ ：一般是字符串类型
- \ ``PATTERN``\ ：该模式支持\ `通配符机制 <../../../../5-Wildcard/1-FileWildcard.html>`_\ (注意不是正则表达式)

	- \ ``*``\ ：匹配任意长度的任意字符
	- \ ``?``\ : 匹配单个任意字符
	- \ ``[]``\ : 匹配指定字符范围内的任意单个字符，不区分大小写

	    - \ ``[a-z]``\ ：不区分大小写，可以匹配大写字母
	    - \ ``[A-Z]``\ ：不区分大小写，可以匹配小写字母
	    - \ ``[0-9]``\ ：匹配0到9任意单个数字
	    - \ ``[a-z0-9]``\ ：匹配单个字母或数字
	    - \ ``[[:upper:]]``\ ：匹配单个大写字母
	    - \ ``[[:lower:]]``\ ：匹配单个小写字母
	    - \ ``[[:alpha:]]``\ ：匹配单个大写或小写字母
	    - \ ``[[:digit:]]``\ ：匹配单个数字
	    - \ ``[[:alnum:]]``\ ：匹配单个字母或数字
	    - \ ``[[:space:]]``\ ：匹配单个空格字符
	    - \ ``[[:punct:]]``\ ：匹配单个标点符号

	- \ ``[^]``\ : 匹配指定字符范围外的任意单个字符

	    - \ ``[^a-z]``\ ：匹配字母之外的单个字符
	    - \ ``[^A-Z]``\ ：匹配字母之外的单个字符
	    - \ ``[^0-9]``\ ：匹配数字之外的单个字符
	    - \ ``[^a-z0-9]``\ ：匹配字母和数字之外的单个字符
	    - \ ``[^[:upper:]]``\ ：匹配大写字母之外的单个字符
	    - \ ``[^[:lower:]]``\ ：匹配小写字母之外的单个字符
	    - \ ``[^[:alpha:]]``\ ：匹配字母之外的单个字符
	    - \ ``[^[:digit:]]``\ ：匹配数字之外的单个字符
	    - \ ``[^[:alnum:]]``\ ：匹配字母和数字之外的单个字符
	    - \ ``[^[:space:]]``\ ：匹配空格字符之外的单个字符
	    - \ ``[^[:punct:]]``\ ：匹配标点符号之外的单个字符
	- \ ``|``\ ：用来分隔上述\ ``*``\  、\ ``?``\ 、\ ``[]``\ 、\ ``[^]``\ 通配元字符；例如\ ``([yY] | [yY][eE][sS]])``\ 表示即可以输入单个字母的\ ``y或Y``\ ，还可以输入\ ``yes三个字母的任意大小写格式``\ 

示例代码如下

.. code-block:: sh

	#!/bin/bash
	set -- y

	case "$1" in
	    ([yY]|[yY][eE][sS])
	        echo yes;&
	    ([nN]|[nN][oO])
	        echo no;;
	    (*)
	        echo wrong;;
	esac

	# 执行结果如下
	# yes
	# no

其中\ ``set -- string_list``\ 的作用是将\ ``string_list``\ 按照\ ``IFS``\ 分隔后分别赋值给位置变量\ ``$1、$2、$3...``\ ，因此此处是为\ ``$1``\ 赋值字符\ ``y``\ 

在此示例中，\ ``$1``\ 能匹配第一个小分支，但第一个小分支的结尾符号为\ ``;&``\ ，所以无需判断地直接执行第二个小分支的\ ``echo no``\ ，但第二个小分支的结尾符号为\ ``;;``\ ，于是直接退出case语句。因此，即使\ ``$1``\ 无法匹配第二个小分句，case语句的结果中也输出了\ ``yes``\ 和\ ``no``\ 

.. code-block:: sh

	#!/bin/bash
	set -- y

	case "$1" in
	    ([yY]|[yY][eE][sS])
	        echo yes;;&
	    ([nN]|[nN][oO])
	        echo no;;
	    (*)
	        echo wrong;;
	esac

	# 执行结果如下
	# yes
	# wrong

在此示例中，\ ``$1``\ 能匹配第一个小分支，但第一个小分支的结尾符号为\ ``;;&``\ ，所以继续向下匹配，第二个小分支未匹配成功，直到第三个小分支才被匹配上，于是执行第三个小分支中的\ ``echo wrong``\ ，但第三个小分支的结尾符号为\ ``;;``\ ，于是直接退出case语句。所以，结果中输出了\ ``yes``\ 和\ ``wrong``\ 




.. _selectcondition:

0x0102 select条件语句
^^^^^^^^^^^^^^^^^^^^^^^

\ ``select条件语句``\ 是一种可以提供菜单选择的条件判断语句，其语法结构如下(使用\ ``help select``\ 命令可以查看)

.. code-block:: sh

	select NAME [in WORDS ... ;] do 
		COMMANDS_LIST
	done

其执行逻辑是

- \ **1.**\ 如果\ ``in WORDS``\ 部分存在，则会将\ ``WORDS``\ 部分根据环境变量\ ``IFS``\ 进行分割，对分割后的每一项依次进行编号作为菜单项输出；如果\ ``in WORDS``\ 部分不存在，则使用\ ``in $@``\ 代替，即将位置变量的内容进行编号作为菜单项输出
- \ **2.**\ 当输入内容能够匹配输出菜单序号时，该序号将会保存到变量\ ``NAME``\ 中，该序号对应的内容将会保存到特殊变量\ ``REPLY``\ 中；当输入内容不能匹配输出菜单序号时，比如随便几个字符，变量\ ``NAME``\ 将会被置空，特殊变量\ ``REPLY``\ 将会保存所有输入内容
- \ **3.**\ 每次输入选择保存\ ``NAME``\ 和\ ``REPLY``\ 变量后，就会直接执行\ ``COMMANDS_LIST``\ 部分；如果没有\ ``break``\ 命令，则会跳回第一步，循环重复执行，直到遇到\ ``break``\ 命令或者\ ``ctrl+c``\ 退出\ ``select``\ 语句


示例代码如下

.. code-block:: sh

	#!/bin/bash

	select fname in cat dog sheep mouse;do
	        echo your choice: \"$REPLY\) $fname\"
	done

	# 执行结果如下
	[root@localhost ~]# ./test.sh 
	1) cat
	2) dog
	3) sheep
	4) mouse
	#? 1                      # 输入序号1
	your choice: "1) cat"
	#? 2                      # 输入序号2
	your choice: "2) dog"
	#? 3                      # 输入序号3
	your choice: "3) sheep"
	#? 4                      # 输入序号4
	your choice: "4) mouse"
	#? 5                      # 输入序号5，没有该序号值，所有fname变量置空
	your choice: "5) "
	#? anony                  # 输入anony，不是序号值，所以fname变量置空
	your choice: "anony) "
	#? ^C                     # select语句中没有break命令，通过ctrl+c退出select语句


.. _conteststate:

0x0103 条件测试表达式
^^^^^^^^^^^^^^^^^^^^^^^^^^^

条件测试表达式有以下几种类型

- \ `整数测试表达式 <#intergtest>`_\ 
- \ `字符测试表达式 <#chartest>`_\ 
- \ `文件测试表达式 <#filetest>`_\ 

.. _intergtest:

整数测试表达式的格式为：\ ``NUM1 操作符 NUM2``\ 

- \ ``NUM1``\ 和\ ``NUM2``\ 是整数，可以直接是整数值(例如：\ ``2``\ )，可以是变量引用(例如：\ ``$#``\ )，也可以是算术运算得到的值(参考\ `算术运算 <../2-datatype/index.html#arithmeticl>`_\ )
- 整数测试操作符有

	- \ ``-eq``\ ：等于
	- \ ``-ne``\ ：不等于
	- \ ``-le``\ ：小于等于
	- \ ``-ge``\ ：大于等于 
	- \ ``-lt``\ ：小于
	- \ ``-gt``\ :大于

.. _chartest:

字符测试表达式的格式有两种格式

- 双目测试格式：\ ``STR1 双目操作符 STR2``\ 
	
	- \ ``STR1``\ 和\ ``STR2``\ 是字符串，shell中默认数据类型是字符串，即不带\ ``""``\ 默认都会被当做字符串类型；但是在此处，必须使用\ ``""``\ (除非是模式匹配中的模式字符串，才不用引号)
	- 双目测试操作符有

		- \ ``>``\ ：表示左边的字符串大于右边的字符串
		- \ ``<``\ ：表示左边的字符串小于右边的字符串
		- \ ``==``\ ：表示左边的字符串等于右边的字符串
		- \ ``!=``\ 、\ ``<>``\ ：表示左右两边的字符串完全不相等
		- \ ``=~``\ ：左侧是普通字符串，右侧是一个模式字符串，用来判断左侧的字符串能否被右侧的模式所匹配：但是必须在\ ``[[]]``\ 中才能执行模式匹配；模式中可以使用行首、行尾锚定符，但是\ **模式不要加引号**\ ，有时候可能不需要转义，具体模式书写格式可参考\ `正则表达式 <../../../../5-Wildcard/2-Regular/1-syntax/index.html>`_\ 
- 单目测试格式：\ ``单目操作符 STR``\ 

	- \ ``STR``\ 是字符串，shell中默认数据类型是字符串，即不带\ ``""``\ 默认都会被当做字符串类型；但是在此处，必须使用\ ``""``\ 
	- 单目测试操作符有

		- \ ``-n``\ : 判断字符串是否不空，不空为真，空则为假
		- \ ``-z``\ ：判断字符串是否为空，空则为真，不空则假

.. _filetest:

文件测试表达式的格式也有两种

- 单目测试格式：\ ``单目操作符 FILE``\ 

	- \ ``FILE``\ 是文件名，一般使用绝对路径
	- 单目操作符有

		- \ ``-e FILE``\ ：测试文件是否存在
		- \ ``-a FILE``\ ：测试文件是否存在
		- \ ``-f FILE``\ ：测试是否为普通文件
		- \ ``-d FILE``\ ： 测试是否为目录文件
		- \ ``-b FILE``\ ：测试文件是否存在并且是否为一个块设备文件
		- \ ``-c FILE``\ ：测试文件是否存在并且是否为一个字符设备文件
		- \ ``-h|-L FILE``\ ：测试文件是否存在并且是否为符号链接文件
		- \ ``-p FILE``\ ：测试文件是否存在并且是否为管道文件：
		- \ ``-S FILE``\ ：测试文件是否存在并且是否为套接字文件：
		- \ ``-r FILE``\ ：测试其有效用户是否对此文件有读取权限
		- \ ``-w FILE``\ ：测试其有效用户是否对此文件有写权限
		- \ ``-x FILE``\ ：测试其有效用户是否对此文件有执行权限
		- \ ``-s FILE``\ ：测试文件是否存在并且不空
- 双目测试格式：\ ``FILE1 双目操作符 FILE2``\ 

	- \ ``FILE1``\ 和\ ``FILE2``\ 是文件名，一般使用绝对路径
	- 双目操作符有

		- \ ``FILE1 -nt FILE2``\ ：测试FILE1是否比FILE2更new一些
		- \ ``FILE1 -ot FILE2``\ ：测试FILE1是否比FILE2更old一些


.. _loopstate:

0x02 循环执行语句
~~~~~~~~~~~~~~~~~~~

循环执行语句会根据判断条件循环多次执行对应的循环体\ ``cmd_list``\ 命令列表，当判断条件不满足时就会退出该循环体，需要注意的是：\ **循环必须有退出条件，否则将陷入死循环**\ ；循环执行语句有以下几种

- \ `for循环语句 <#forloop>`_\ 
- \ `while循环语句 <#whileloop>`_\ 
- \ `until循环语句 <#untilloop>`_\ 

.. _forloop:

0x0200 for循环语句
~~~~~~~~~~~~~~~~~~~~

\ ``for循环语句``\ 在shell脚本中应用及其广泛，它有两种语法结构(使用\ ``help for``\ 命令可以查看)

.. code-block:: sh

	# 结构一
	for NAME [in WORDS ... ] ; do 
		COMMANDS_LIST
	done


	# 结构二
	for (( exp1; exp2; exp3 )); do 
		COMMANDS_LIST
	done

语法结构一的执行逻辑是

-  \ **1.**\ 如果\ ``in WORDS``\ 部分存在，则会将\ ``WORDS``\ 部分根据环境变量\ ``IFS``\ 进行分割，依次赋值给变量\ ``NAME``\ (\ **如果WORD中使用引用包围了某些单词，则将引号包围的内容分隔为一个单词**\ )；如果\ ``in WORDS``\ 部分不存在，则默认使用\ ``in $@``\ 代替，即将位置变量依次赋值给变量\ ``NAME``\ 
- \ **2.**\ \ ``NAME``\ 变量每被赋值一次，就会执行一次循环体\ ``COMMANDS_LIST``\ ，直到第一步中所有分隔部分给\ ``NAME``\ 变量赋值完毕，才会结束循环
- \ **3.**\ 如果在循环体中遇到\ ``continue``\ 命令，则退出当前for循环，直接进行下一for循环；如果遇到\ ``break``\ 命令，则直接退出for循环结构体
- \ **4.**\ 整个for语句结构体的状态返回值取决于退出整个for循环结构体时最后一个命令的执行状态返回值

语法结构二的执行逻辑是

- \ **1.**\ 首先执行算术表达式\ ``exp1``\ 
- \ **2.**\ 然后判定算术表达式\ ``exp2``\ 的状态返回值是否为\ ``0``\ ，如果为\ ``0``\ 则执行循环体\ ``COMMANDS_LIST``\ ，执行完之后，执行算术表达式\ ``exp3``\ ，然后再次判定算术表达式\ ``exp2``\ 的状态返回值是否为\ ``0``\ ；直到其状态返回值为\ ``非0``\ 才退出整个for循环结构体，否则就会循环执行第2步，此时整个for循环的状态返回值为退出整个for循环结构体时最后一个算术表达式\ ``exp2``\ 的状态返回值
- \ **3.**\ 如果在循环体中遇到\ ``continue``\ 命令，则退出当前for循环，直接进行下一for循环(即直接执行上述第二步)，此时整个for循环的状态返回值为退出整个for循环结构体时最后一个算术表达式\ ``exp2``\ 的状态返回值；如果遇到\ ``break``\ 命令，则直接退出整个for循环结构体，此时整个for语句结构体的状态返回值取决于退出整个for循环结构体时最后一个命令的执行状态返回值

\ ``for循环``\ 语句的循环退出机制有：

- \ ``continue``\ ：跳出当前循环进入下一循环
- \ ``break[n]``\ ：默认跳出整个循环；n可以指定跳出几层循环
- \ ``列表遍历``\ ：使用一个变量去遍历给定\ `列表 <../2-datatype/index.html#listsl>`_\ 中的每个元素(以环境变量\ ``IFS``\ 为分隔符)，在每次变量赋值时执行一次循环体，直至赋值完成所有元素退出循环
- \ ``算术执行``\ ：引用算术表达式的执行状态返回值来判断是否退出整个循环

for循环语句适用于已知循环次数的场景

语法结构一中的\ ``WORDS``\ 有多种表现形式

-  \ `列表变量 <../2-datatype/index.html#listsl>`_\ 

	- 数字列表：\ `数字列表示例代码 <../2-datatype/index.html#forlistl>`_\ 

		- \ ``{start..end}``\ 
		- \ ```seq start step end```\ 
	- 其它列表：\ `其它列表示例代码 <../2-datatype/index.html#forlistll>`_\ 

		- \ ``使用空白分隔符直接给出列表``\ 
		- \ ``使用文件名通配机制生成列表``\ 
		- \ ``使用命令生成列表``\ 
- \ `数组变量 <../2-datatype/index.html#arraysl>`_\ 

	- 普通数组：\ `普通数组示例代码 <../2-datatype/index.html#forlooppl>`_\ 
	- 关联数组：\ `关联数组示例代码 <../2-datatype/index.html#forloopgl>`_\ 

语法结构二种的\ ``exp``\ 只支持数学计算和比较，因为它被包含在执行算术运算的\ ``(())``\ 操作符之内

- \ ``exp1``\ ：一般是赋值表达式，例如\ ``for ((i=1,j=3;i<=3 && j>=2;++i,--j));do echo $i $j;done``\ 
- \ ``exp2``\ ：一般是比较表达式，例如\ ``for ((i=1,j=3;i<=3 && j>=2;++i,--j));do echo $i $j;done``\ ，比较表达式可参考\ `数值类型比较运算for循环部分 <../2-datatype/index.html#logiclforl>`_\ 
- \ ``exp3``\ ：一般是计算表达式，例如\ ``for ((i=1,j=3;i<=3 && j>=2;++i,--j));do echo $i $j;done``\ ，计算表达式可参考\ `数值类型算术运算 <../2-datatype/index.html#arithmeticl>`_\ 


示例代码如下

- 计算当前系统所有用户ID之和

.. code-block:: sh

	#!/bin/bash

	declare -i uidSum=0

	for i in `cut -d: -f3 /etc/passwd`; do
	        uidSum=$[$uidSum+$i]
	done

	echo "the UIDSum is: $uidSum"

- 新建用户tmpuser1-tmpuser10，并计算它们的id之和

.. code-block:: sh

	#!/bin/bash

	declare -i uidSum=0

	for i in {1..10}; do
	        useradd tmpuser$i
	        let uidSum+=`id -u tmpuser$i`
	done

	echo "the UIDSum is: $uidSum"

- 输出1-10之间的所有偶数

.. code-block:: sh

	#!/bin/bash

	for ((i=1;i<=10;i++));do
	        let tmp=i%2
	        if [ $tmp -eq 0 ]; then
	                echo $i
	        fi
	done



.. _whileloop:

0x0201 while循环语句
~~~~~~~~~~~~~~~~~~~~~~~

\ ``while循环语句``\ 的语法结构如下(使用\ ``help while``\ 命令可以查看)

.. code-block:: sh

	while TEST_COMMANDS_LIST; do 
		COMMANDS_LIST
	done

其执行逻辑是

- \ **1.**\ 先执行\ ``TEST_COMMANDS_LIST``\ 条件测试命令，如果其最后一个命令的执行状态返回值为\ ``0``\ ，则执行循环体\ ``COMMANDS_LIST``\ ，执行完后，再次执行\ ``TEST_COMMANDS_LIST``\ 条件测试命令，直到其最后一个名的状态返回值为\ ``非0``\ 才会退出整个while循环体，否则将一直循环执行该步，此时整个while循环的状态返回值为退出循环结构体时最后一个\ ``TEST_COMMANDS_LIST``\ 条件测试命令的最后一个命令的状态返回值
- \ **2.**\ 如果在循环体中遇到\ ``continue``\ 命令，则退出当前while循环，直接进行下一while循环(即直接执行上述第一步)，此时整个while循环的状态返回值为退出循环结构体时最后一个\ ``TEST_COMMANDS_LIST``\ 条件测试命令的最后一个命令的状态返回值；如果遇到\ ``break``\ 命令，则直接退出整个while循环结构体，此时整个while语句结构体的状态返回值取决于退出整个循环结构体时最后一个命令的执行状态返回值

在上述\ ``while循环语句``\ 结构中需要注意的是

- \ ``COMMANDS_LIST``\ ：表示待执行的命令列表(也称为while循环体)，即一系列shell命令的集合，类型格式多种多样，在一系列示例代码中可见一斑

	- 注意：在命令列表中不能使用\ ``()``\ 操作符改变优先级，它的作用是让括号内的语句成为命令列表进入子shell中执行，它的具体作用可参考：\ `括号操作符 <../4-operator/index.html#parenthesel>`_\ 
- \ ``TEST_COMMANDS_LIST``\ ：表示条件测试命令，即通过引用条件测试命令的执行状态返回值是否为\ ``0``\ 来判断是否执行上述\ ``COMMANDS_LIST``\ 循环体；\ **这里需要特别注意的是，和其它语言不通，shell的条件测试命令只有以下三种类型**\ 

	- \ ``命令执行``\ ：命令本身执行后就会产生对应的执行状态返回值，所以可以直接用来做条件判断

		- 此时不能使用\ **``**\ 操作符来引用命令，因为该操作引用的是命令的执行结果，而不是命令的执行状态返回值
		- 通常是直接使用命令，然后在命令后面添加\ ``s&> /dev/null``\ ，表示将命令的执行结果重定向至\ ``/dev/null``\ ，只引用其状态返回值；例如：\ ``if grep "^root" /etc/passwd &> /dev/null; then``\ 
	- \ ``执行条件测试表达式``\ ：在shell中，条件测试表达式是由条件测试操作符以及对应的操作数组成，详细介绍可参考下列：\ `条件测试表达式 <#conteststate>`_\ ，执行条件测试表达式有以下三种格式

		- \ ``test Test_Expression``\ ：通过\ ``test``\ 命令执行
		- \ ``[ Test_Expression ]``\ ：通过\ ``[]``\ 操作符执行，注意\ ``Test_Expression`` 前后有空格
		- \ ``[[ Test_Expression ]]``\ ：通过\ ``[[]]``\ 操作符执行，注意\ ``Test_Expression`` 前后有空格
	- \ ``组合条件测试``\ ：即对多个\ ``命令执行状态返回值``\ 或者\ ``执行条件测试表达式状态返回值``\ 做逻辑运算，组合条件测试有以下三种格式

		- 逻辑与操作：只有当\ ``&&``\ 操作符两边执行结果都为真(状态值为0)，最后组合条件测试结果才为真(状态值为0)

			- \ ``[ Test_Expression1 ] && [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND &> /dev/null && [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND1 &> /dev/null && COMMAND2 &> /dev/null &&``\ 
			- \ ``[ Test_Expression1 -a Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``[[ Test_Expression1 && Test_Expression2 ]]``\ ：此处只能使用\ ``[[]]``\ 操作符，因为\ ``&&``\ 运算符不允许用于\ ``[]``\ 操作符中
		- 逻辑或操作：只要\ ``||``\ 操作符两边执行结果有一个为真(状态值为0)，最后组合条件测试结果就为真(状态值为0)

			- \ ``[ Test_Expression1 ] || [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND &> /dev/null || [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND1 &> /dev/null || COMMAND2 &> /dev/null &&``\ 
			- \ ``[ Test_Expression1 -0 Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``[[ Test_Expression1 || Test_Expression2 ]]``\ ：此处只能使用\ ``[[]]``\ 操作符，因为\ ``||``\ 运算符不允许用于\ ``[]``\ 操作符中
		- 逻辑非操作：对\ ``!``\ 右侧执行结果取反

			- \ ``! [ Test_Expression ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``! COMMAND1 &> /dev/null``\ 
			- \ ``! ([ Test_Expression1 ] || [ Test_Expression2 ])``\ ：此处相当于\ ``! [ Test_Expression1 ] && ! [ Test_Expression2 ]``\ 
			- \ ``! ([ Test_Expression1 ] && [ Test_Expression2 ])``\ ：此处相当于\ ``! [ Test_Expression1 ] || ! [ Test_Expression2 ]``\ 
		- 注意：\ **非的优先级大于与，与的优先级大于或**\ 

while循环语句的循环退出机制有：

- \ ``continue``\ ：跳出当前循环进入下一循环
- \ ``break[n]``\ ：默认跳出整个循环；n可以指定跳出几层循环
- \ ``条件测试``\ ：此时为了避免死循环，\ ``TEST_COMMANDS_LIST``\ 条件测试里必须有控制循环次数的变量；\ ``COMMANDS_LIST``\ 循环体里必须有改变条件测试中用于控制循环次数变量的值操作

\ ``while循环``\ 语句适用于循环次数未知的场景，示例代码如下

.. code-block:: sh

	#!/bin/bash

	let i=1,sum=0

	# 此处TEST_COMMANDS_LIST有多个命令
	# 需要注意的是[ $i -le 10 ]才是判定是否退出循环的命令
	# 而echo $i命令的执行状态返回结果跟退出循环无关
	while echo $i;[ $i -le 10 ]; do
	        let sum=sum+i;
	        let ++i
	done

	echo $sum


对于\ ``while循环``\ ，有另外两种常见的用法

- 实现无限死循环

.. code-block:: sh

	# 格式一：TEST_COMMANDS_LIST部分使用:
	while :; do
		COMMANDS_LIST
	done

	# 格式二：TEST_COMMANDS_LIST部分使用true
	while true; do
		COMMANDS_LIST
	done

- 实现read命令从标准输入中按行读取值，然后保存到变量line中(既然是read命令，就可以保存到多个变量中)，读取一行就是一个循环

.. code-block:: sh

	##############################方法一#####################################
	# 标准输入来自于管道
	# 每读取一行内容就会进入一次while循环，此处有两行内容所以进行两次while循环
	# 此处通过-e选项实现多行输入
	# 读取的每行内容将会按照IFS分隔，并赋值给两个变量
	declare -i linenum=0
	echo -e "abc xyz\n2abc 2xyz" | while read field1 field2; do
		echo $field1
		echo $field2
		linenum+=1
	done
	echo "there are $linenum lines"
	# 此处使用的是管道符号，这样使得while语句在子shell中执行，这也意味着while语句内部设置的变量、数组、函数等在while循环外部都不再生效
	# 执行结果如下
	# abc
	# xyz
	# 2abc
	# 2xyz
	# there are 0 lines


	##############################方法二#####################################
	# 标准输入来自于重定向
	# 每读取一行内容就会进入一次while循环，此处有两行内容所以进行两次while循环
	# 此处通过EOF标志实现多行输入
	# 读取的每行内容将会按照IFS分隔，并赋值给两个变量
	declare -i linenum=0
	while read field1 field2; do
		echo $field1
		echo $field2
		linenum+=1
	done << EOF
	abc xyz
	2abc 2xyz
	EOF
	echo "there are $linenum lines"
	# 此处while语句内部设置的变量、数组、函数等在while循环外部依然生效
	# 执行结果如下
	# abc
	# xyz
	# 2abc
	# 2xyz
	# there are 2 lines


	##############################方法三#####################################
	# 标准输入来自于重定向
	# 常用来重定向文件输入，读取文件内容
	# 每读取文件一行内容，就会进入一次while循环，直到读完文件尾部退出循环
	while read line; do
		echo $line
	done < /etc/passwd


	##############################方法四#####################################
	# 读取文件的另一种写法
	exec </etc/passwd;while read line; do
        echo $line
	done

关于read命令从标准输入中按行读取值的几种while循环的写法，还有一点需要注意

- 方法一传递数据的源是一个单独的进程，它传递的数据只要被while循环读取一次，所有剩余的数据就会被丢弃
- 方法二、三、四是以实体文件作为重定向传递的数据，while循环读取一次之后并不会丢弃剩余数据，直到数据完全读取完毕

也就是说当标准输入是非实体文件时(如管道传递、独立进程产生的)只供一次读取；当标准输入是直接重定向实体文件时，可供多次读取，但只要某一次读取了该文件的全部内容就无法再提供读取

回到IO重定向上，无论什么数据资源，只要被读取完毕或者主动丢弃，那么该资源就不可再得

- 对于独立进程传递的数据(管道左侧进程产生的数据、进程替换产生的数据)，它们都是虚拟数据，要不被一次读取完毕，要不读一部分剩余的丢弃，这是真正的一次性资源；其实这也是进程间通信时数据传递的现象
- 实体文件重定向传递的数据，只要不是一次性被全部读取，它就是可再得资源，直到该文件数据全部读取结束，这是伪一次性资源

大多数情况下，独立进程传递的数据和文件直接传递的数据并没有什么区别，但有些命令可以标记当前读取到哪个位置，使得下次该命令的读取动作可以从标记位置处恢复并继续读取，特别是这些命令用在循环中时。这样的命令有\ ``head -n N``\ 和\ ``grep -m``\ ，经测试，\ ``tail``\ 并没有位置标记的功能，因为\ ``tail``\ 读取的是后几行，所以它必然要读取到最后一行并计算要输出的行，所以\ ``tail``\ 的性能比\ ``head``\ 要差


- 示例一：通过管道将实体文件的内容传递给head

.. code-block:: sh

	#!/bin/bash
	declare -i i=0

	cat /etc/passwd | while head -n 2; [[ $i -le 3 ]]; do
	        echo $i
	        let ++i
	done

	# 执行结果如下
	# root:x:0:0:root:/root:/bin/bash
	# bin:x:1:1:bin:/bin:/sbin/nologin
	# 0
	# 1
	# 2
	# 3


- 示例二：将实体文件重定向传递给head

.. code-block:: sh

	#!/bin/bash
	declare -i i=0

	while head -n 2; [[ $i -le 3 ]]; do
	        echo $i
	        let ++i
	done < /etc/passwd

	# 执行结果如下
	# root:x:0:0:root:/root:/bin/bash
	# bin:x:1:1:bin:/bin:/sbin/nologin
	# 0
	# daemon:x:2:2:daemon:/sbin:/sbin/nologin
	# adm:x:3:4:adm:/var/adm:/sbin/nologin
	# 1
	# lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
	# sync:x:5:0:sync:/sbin:/bin/sync
	# 2
	# shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
	# halt:x:7:0:halt:/sbin:/sbin/halt
	# 3
	# mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
	# operator:x:11:0:operator:/root:/sbin/nologin

分析上述结果可以看到

- 示例一中：本该head应该每次读取2行，但实际执行结果中显示总共就只读取了2行
- 示例二中：head每次读取2行，而且每次读取的两行是不同的，后一次读取的两行是从前一次读取结束的地方开始的，这是因为head有\ ``读取到指定行数后做上位置标记``\ 的功能

要想确定命令、工具是否具有做位置标记的能力，只需像下面例子一样做个简单的测试。以\ ``head``\ 和\ ``sed``\ 为例，即使\ ``sed``\ 的\ ``q``\ 命令能让\ ``sed``\ 匹配到内容就退出，但却不做位置标记，而且数据资源使用一次就丢弃

.. figure:: images/1.png

其实在实际应用过程中，这根本就不是个问题，因为搜索和处理文本数据的工具虽然不少，但绝大多数都是用一次文本就丢一次，几乎不可能因此而产生问题。之所以说这么多废话，主要是想说上面的read读取数据while写法中，管道传递数据是使用最广泛的写法，但其实也是最烂的一种

.. _untilloop:

0x0202 until循环语句
~~~~~~~~~~~~~~~~~~~~~

\ ``until循环语句``\ 的语法结构如下(使用\ ``help until``\ 命令可以查看)

.. code-block:: sh

	until TEST_COMMANDS_LIST; do
		COMMANDS_LIST
	done

\ ``until循环``\ 和\ ``while循环``\ 的执行思路大致相同，只不过效果相反

- \ **1.**\ 先执行\ ``TEST_COMMANDS_LIST``\ 条件测试命令，如果其最后一个命令的执行状态返回值为\ ``非0``\ ，则执行循环体\ ``COMMANDS_LIST``\ ，执行完后，再次执行\ ``TEST_COMMANDS_LIST``\ 条件测试命令，直到其最后一个命令的状态返回值为\ ``0``\ 才会退出整个until循环体，否则将一直循环执行该步，此时整个until循环的状态返回值为退出循环结构体时最后一个\ ``TEST_COMMANDS_LIST``\ 条件测试命令的最后一个命令的状态返回值
- \ **2.**\ 如果在循环体中遇到\ ``continue``\ 命令，则退出当前until循环，直接进行下一until循环(即直接执行上述第一步)，此时整个until循环的状态返回值为退出循环结构体时最后一个\ ``TEST_COMMANDS_LIST``\ 条件测试命令的最后一个命令的状态返回值；如果遇到\ ``break``\ 命令，则直接退出整个until循环结构体，此时整个until语句结构体的状态返回值取决于退出整个循环结构体时最后一个命令的执行状态返回值

在上述\ ``until循环语句``\ 结构中需要注意的是

- \ ``COMMANDS_LIST``\ ：表示待执行的命令列表(也称为until循环体)，即一系列shell命令的集合，类型格式多种多样，在一系列示例代码中可见一斑

	- 注意：在命令列表中不能使用\ ``()``\ 操作符改变优先级，它的作用是让括号内的语句成为命令列表进入子shell中执行，它的具体作用可参考：\ `括号操作符 <../4-operator/index.html#parenthesel>`_\ 
- \ ``TEST_COMMANDS_LIST``\ ：表示条件测试命令，即通过引用条件测试命令的执行状态返回值是否为\ ``0``\ 来判断是否执行上述\ ``COMMANDS_LIST``\ 循环体；\ **这里需要特别注意的是，和其它语言不通，shell的条件测试命令只有以下三种类型**\ 

	- \ ``命令执行``\ ：命令本身执行后就会产生对应的执行状态返回值，所以可以直接用来做条件判断

		- 此时不能使用\ **``**\ 操作符来引用命令，因为该操作引用的是命令的执行结果，而不是命令的执行状态返回值
		- 通常是直接使用命令，然后在命令后面添加\ ``s&> /dev/null``\ ，表示将命令的执行结果重定向至\ ``/dev/null``\ ，只引用其状态返回值；例如：\ ``if grep "^root" /etc/passwd &> /dev/null; then``\ 
	- \ ``执行条件测试表达式``\ ：在shell中，条件测试表达式是由条件测试操作符以及对应的操作数组成，详细介绍可参考下列：\ `条件测试表达式 <#conteststate>`_\ ，执行条件测试表达式有以下三种格式

		- \ ``test Test_Expression``\ ：通过\ ``test``\ 命令执行
		- \ ``[ Test_Expression ]``\ ：通过\ ``[]``\ 操作符执行，注意\ ``Test_Expression`` 前后有空格
		- \ ``[[ Test_Expression ]]``\ ：通过\ ``[[]]``\ 操作符执行，注意\ ``Test_Expression`` 前后有空格
	- \ ``组合条件测试``\ ：即对多个\ ``命令执行状态返回值``\ 或者\ ``执行条件测试表达式状态返回值``\ 做逻辑运算，组合条件测试有以下三种格式

		- 逻辑与操作：只有当\ ``&&``\ 操作符两边执行结果都为真(状态值为0)，最后组合条件测试结果才为真(状态值为0)

			- \ ``[ Test_Expression1 ] && [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND &> /dev/null && [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND1 &> /dev/null && COMMAND2 &> /dev/null &&``\ 
			- \ ``[ Test_Expression1 -a Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``[[ Test_Expression1 && Test_Expression2 ]]``\ ：此处只能使用\ ``[[]]``\ 操作符，因为\ ``&&``\ 运算符不允许用于\ ``[]``\ 操作符中
		- 逻辑或操作：只要\ ``||``\ 操作符两边执行结果有一个为真(状态值为0)，最后组合条件测试结果就为真(状态值为0)

			- \ ``[ Test_Expression1 ] || [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND &> /dev/null || [ Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``COMMAND1 &> /dev/null || COMMAND2 &> /dev/null &&``\ 
			- \ ``[ Test_Expression1 -0 Test_Expression2 ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``[[ Test_Expression1 || Test_Expression2 ]]``\ ：此处只能使用\ ``[[]]``\ 操作符，因为\ ``||``\ 运算符不允许用于\ ``[]``\ 操作符中
		- 逻辑非操作：对\ ``!``\ 右侧执行结果取反

			- \ ``! [ Test_Expression ]``\ ：此处使用\ ``[]``\ 或\ ``[[]]``\ 都行
			- \ ``! COMMAND1 &> /dev/null``\ 
			- \ ``! ([ Test_Expression1 ] || [ Test_Expression2 ])``\ ：此处相当于\ ``! [ Test_Expression1 ] && ! [ Test_Expression2 ]``\ 
			- \ ``! ([ Test_Expression1 ] && [ Test_Expression2 ])``\ ：此处相当于\ ``! [ Test_Expression1 ] || ! [ Test_Expression2 ]``\ 
		- 注意：\ **非的优先级大于与，与的优先级大于或**\ 

\ ``until循环``\ 语句的循环退出机制有：

- \ ``continue``\ ：跳出当前循环进入下一循环
- \ ``break[n]``\ ：默认跳出整个循环；n可以指定跳出几层循环
- \ ``条件测试``\ ：此时为了避免死循环，\ ``TEST_COMMANDS_LIST``\ 条件测试里必须有控制循环次数的变量；\ ``COMMANDS_LIST``\ 循环体里必须有改变条件测试中用于控制循环次数变量的值操作

until循环语句也是适用于循环次数未知的场景，示例代码如下

.. code-block:: sh

	#!/bin/bash

	declare -i i=5

	until echo hello;[ "$i" -eq 1 ]; do
	        let --i
	        echo $i
	done

	# 执行结果如下
	# hello
	# 4
	# hello
	# 3
	#hello+
	# 2
	# hello
	# 1
	# hello

.. _loopexit:

0x0203 循环退出命令
~~~~~~~~~~~~~~~~~~~~~

循环退出命令有

- \ ``continue [n]``\ ：表示退出当前循环进入下一次循环，适用于\ ``for、while、until、select``\ 语句；n表示退出的循环的次数，默认n=1
- \ ``break [n]``\ ：表示退出整个循环，适用于\ ``for、while、until、select``\ 语句；n表示退出的循环层数，默认n=1
- \ ``return [n]``\ ：表示退出整个函数，适用于函数体内的\ ``for、while、until、select``\ 语句，同样也适用于函数体内的\ ``if、case``\ 语句；数值n表示函数的退出状态码，如果没有定义退出状态码，则函数的状态退出码为函数的最后一条命令的执行状态返回值
- \ ``exit [n]``\ ：表示退出当前shell，适用于脚本的任何地方，表示退出整个脚本；数值n表示脚本的退出状态码，如果没有定义退出状态码，则脚本的状态退出码为脚本的最后一条命令的执行状态返回值