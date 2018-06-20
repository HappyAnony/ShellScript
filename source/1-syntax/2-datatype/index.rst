数据类型
=================

数据类型的本质：固定内存大小的别名

数据类型的作用：

- 确定对应变量分配的内存大小
- 确定对应变量所能支持的运算或操作

shell脚本是弱类型解释型的语言，在脚本运行时由解释器进行解释变量在什么时候是什么数据类型

在bash中，变量默认都是字符串类型，都是以字符串方式存储，所以在本章主要是介绍各数据类型变量所支持的运算或操作

虽说变量默认都是字符串类型，但是按照其使用场景可将数据类型分为以下几种类型：

- \ `数值型 <#valuesl>`_\ 
- \ `字符串型 <#stringsl>`_\ 
- \ `数组型 <#arraysl>`_\ 
- \ `列表型 <#listsl>`_\ 

.. _valuesl:

0x00 数值型
~~~~~~~~~~~~

首先我们来声明定义一个数值型变量：\ ``declare -i Var_Name``\ 

- 虽说声明是一个数值型变量，但是存储依然是按照字符串的形式进行存储
- 该种方式声明，变量默认是本地全局变量，可以通过\ ``local Var_Name``\ 关键字将变量修改为局部变量，可以通过\ ``export Var_Name``\ 关键字将变量导出为环境变量
- 除了使用\ ``declare -i``\ 显式声明变量数据类型为数值型，还可以像\ ``Var_Name=1``\ 由解释器动态执行隐式声明该变量数据类型为数值型

数值型变量一般支持以下运算操作

- \ `算术运算 <#arithmeticl>`_\ 
- \ `比较运算 <#logicl>`_\ 
- \ `数组索引 <#arrayindex>`_\ 

.. _arithmeticl:

0x0000 算术运算
~~~~~~~~~~~~~~~~~

算术运算代码示例如下

.. code-block:: sh

	#!/bin/bash

	declare -i val=5   # 显式声明数值变量
	num=2              # 隐式声明数值变量

	# 使用[]运算符执行算术表达式$val+$num
	# 使用$引用表达式执行结果
	echo "val+num=$[$val+$num]"
	echo "val++: $[val++]"  # 这里不需要加$，不是引用变量的值，而是修改变量的值
	echo "val--: $[val--]"  # 这里不需要加$，不是引用变量的值，而是修改变量的值
	echo "++val: $[++val]"  # 这里不需要加$，不是引用变量的值，而是修改变量的值
	echo "--val: $[--val]"  # 这里不需要加$，不是引用变量的值，而是修改变量的值

	# 使用(())运算符执行算术表达式
	# 使用$引用表达式执行结果
	echo "val-num=$(($val-$num))"
	echo "val%num=$(($val%$num))"

	# 使用let关键字执行算术表达式$val*$num
	# 使用=运算符将执行结果赋值给变量
	let ret=$val*$num
	echo "var*num=$ret"

	# 使用expr命令执行算术表达式$val/$num但是$val / $num之间需要用空格隔开
	# 此时该表达式中的各个部分将作为参数传递给expr命令，最后使用``运算符引用命令的执行结果
	# 使用=运算符将命令引用结果赋值给变量
	ret=`expr $val / $num`
	echo "val/num=$ret"

	# 使用let关键字执行算术表达式+=、-=、*=、/=、%=
	let val+=$num
	echo "var+=num:$val"
	let val-=$num
	echo "var-=num:$val"
	let val*=$num
	echo "val*=num:$val"
	let val/=$sum         # 貌似let不支持/=运算符
	echo "val/=num:$val"
	let val%=$num
	echo "val%=num:$val"

	# 执行结果如下
	# val+num=7
	# val++: 5
	# val--: 6
	# ++val: 6
	# --val: 5
	# val-num=3
	# val%num=1
	# var*num=10
	# val/num=2
	# var+=num:7
	# var-=num:5
	# val*=num:10
	# ./test.sh: line 19: let: val/=: syntax error: operand expected (error token is "/=")
	# val/=num:10
	# val%=num:0


由上述示例可知：数值类型变量支持的算术运算以及对应的算术运算符如下

- \ ``加``\ ：\ ``+``\ 、\ ``+=``\ 、\ ``++``\ 
- \ ``减``\ ：\ ``-``\ 、\ ``-=``\ 、\ ``--``\ 
- \ ``乘``\ ：\ ``*``\ 、\ ``*=``\
- \ ``除``\ ：\ ``/``\ 
- \ ``取余``\  ：\ ``%``\ 、\ ``%=``\

.. _logicl:

0x0001 比较运算
~~~~~~~~~~~~~~~~~

比较运算有以下几种类型

- \ `用于条件测试 <#logicltestl>`_\ 
- \ `用于for循环 <#logiclforl>`_\ 

.. _logicltestl:

用于条件测试的示例代码如下

.. code-block:: sh

	#!/bin/bash

	declare -i val=5   # 显式声明数值变量
	num=2              # 隐式声明数值变量

	# -eq：判断val变量的值是否等于5
	# []运算符用来执行条件测试表达式，其执行结果要么为真，要么为假
	# []运算符和条件测试表达式之间前后有空格
	if [ $val -eq 5 ]; then
	        echo "the value of val variable is 5"
	fi

	# -ne：判断num变量的值是否不等于5
	# [[]]运算符用来执行条件测试表达式，其执行结果要么为真，要么为假
	# [[]]运算符和条件测试表达式之间前后有空格
	if [[ $num -ne 5 ]];then
	        echo "the value of num variable is not 5"
	fi

	# -le：判断num变量的值是否小于或等于val变量的值
	# test命令关键字用来执行条件测试表达式，其执行结果要么为真，要么为假
	if test $num -le $val ;then
	        echo "the value of num variable is lower or equal than val variable"
	fi

	# -ge：判断val变量的值是否大于或等于num变量的值
	# [[]]运算符用来执行条件测试表达式，其执行结果要么为真，要么为假
	# [[]]运算符和条件测试表达式之间前后有空格
	if [[ $val -ge $num ]];then
	        echo "the value of val variable is growth or equal than num variable"
	fi

	# -gt：判断val变量的值是否大于5
	# []运算符用来执行条件测试表达式，其执行结果要么为真，要么为假
	# []运算符和条件测试表达式之间前后有空格
	if [ $val -gt 2 ];then
	        echo "the value of val variable is growth than 2"
	fi

	# -lt：判断num变量的值是否小于5
	# [[]]运算符用来执行条件测试表达式，其执行结果要么为真，要么为假
	# [[]]运算符和条件测试表达式之间前后有空格
	if [[ $num -lt 5 ]];then
	        echo "the value of num variable is lower than 5"
	fi

	# 执行结果如下
	# the value of val variable is 5
	# the value of num variable is not 5
	# the value of num variable is lower or equal than val variable
	# the value of val variable is growth or equal than num variable
	# the value of val variable is growth than 2
	# the value of num variable is lower than 5


由上述示例可知：数值类型变量用于条件测试时支持的比较运算以及对应的运算符如下

- \ ``等于``\ ：\ ``-eq``\ 
- \ ``不等于``\ ：\ ``-ne``\ 
- \ ``小于等于``\ ：\ ``-le``\ 
- \ ``大于等于``\ ：\ ``-ge``\ 
- \ ``大于``\ ：\ ``-gt``\ 
- \ ``小于``\ ：\ ``-lt``\ 
- \ ``逻辑与``\ ：\ ``&&``\ 
- \ ``逻辑非``\ ：\ ``!``\ 
- \ ``逻辑或``\ ：\ ``||``\ 


.. _logiclforl:

用于用于for循环的示例代码如下

.. code-block:: sh

	#!/bin/bash

	# ==判断变量i的值是否等于1
	for ((i=1; i==1; i++));do
	        echo $i
	done

	# !=判断变量i的值是否不等于3
	for ((i=1; i!=3; i++)); do
	        echo $i
	done

	# <=判断变量i的值是否小于等于4
	for ((i=1; i<=4; i++)); do
	        echo $i
	done

	# >=判断变量i的值是否大于等于1
	for ((i=5; i>=1; i--));do
	        echo $i
	done

	# <判断变量i的值是否小于7
	# >判断变量i的值是否大于0
	# &&表示逻辑与
	# ||表示逻辑或
	# !表示逻辑非
	# 非的优先级大于与，与的优先级大于或
	for ((i=1; i>0 && i<7; i++)); do
	        echo $i
	done


由上述示例可知：数值类型变量用于for循环时支持的比较运算以及对应的运算符如下

- \ ``等于``\ ：\ ``==``\ 
- \ ``不等于``\ ：\ ``!=``\ 
- \ ``小于等于``\ ：\ ``<=``\ 
- \ ``大于等于``\ ：\ ``>=``\ 
- \ ``大于``\ ：\ ``>``\ 
- \ ``小于``\ ：\ ``<``\ 
- \ ``逻辑与``\ ：\ ``&&``\ 
- \ ``逻辑非``\ ：\ ``!``\ 
- \ ``逻辑或``\ ：\ ``||``\ 

.. _arrayindex:

0x0002 数组索引
~~~~~~~~~~~~~~~~

数组类型变量当做数组索引可参考\ `数组型变量 <#arraysl>`_\ 一节


.. _stringsl:

0x01 字符串型
~~~~~~~~~~~~~~

首先我们来声明定义一个字符串型变量：\ ``Var_Name="anony"``\ 

- 在bash中，变量默认都是字符串类型，也都是以字符串方式存储，所以字符串可以不需要使用\ ``""``\ ，除非特殊声明，否则都会解释成字符串
- 该种方式声明，变量默认是本地全局变量，可以通过\ ``local Var_Name``\ 关键字将变量修改为局部变量，可以通过\ ``export Var_Name``\ 关键字将变量导出为环境变量
- 该种声明定义方式是由shell解释器动态执行隐式声明该变量数据类型为字符串型

字符串型变量一般支持以下运算操作

- 返回字符串长度：\ ``${#Var_Name}``\ (长度包括空白字符)
- 字符串消除

	- \ ``${var#*word}``\ ：查找\ ``var``\ 中自左而右第一个被\ ``word``\ 匹配到的串，并将此串及向左的所有内容都删除；此处为非贪婪匹配
	- \ ``${var##*word}``\ ：查找\ ``var``\ 中自左而右最后一个被\ ``word``\ 匹配到的串，并将此串及向左的所有内容都删除；此处为贪婪匹配
	- \ ``${var%word*}``\ ：查找\ ``var``\ 中自右而左第一个被\ ``word``\ 匹配到的串，并将此串及向右的所有内容都删除；此处为非贪婪匹配
	- \ ``${var%%word*}``\ ：查找\ ``var``\ 中自右而左最后一个被\ ``word``\ 匹配到的串，并将此串及向右的所有内容都删除；此处为贪婪匹配
- 字符串提取

	- \ ``${var:offset}``\ ：自左向右偏移\ ``offset``\ 个字符，取余下的字串；例如：\ ``name=jerry，${name:2}结果为rry``\ 
	- \ ``${var:offset:length}``\ ：自左向右偏移\ ``offset``\ 个字符，取余下的\ ``length``\ 个字符长度的字串。例如：\``name='hello world' ${name:2:5}结果为llo w``\ 
- 字符串替换

	- \ ``${var/Pattern/Replaceplacement}``\ ：以\ ``Pattern``\ 为模式匹配\ ``var``\ 中的字串，将第一次匹配到的替换为\ ``Replaceplacement``\ ；此处为非贪婪匹配，\ ``Pattern``\ 模式可参考\ `正则表达式 <../../../../5-Wildcard/2-Regular/1-syntax/index.html>`_\ 
	- \ ``${var//Pattern/Replaceplacement}``\ ：以\ ``Pattern``\ 为模式匹配\ ``var``\ 中的字串，将全部匹配到的替换为\ ``Replaceplacement``\ ；此处为贪婪匹配，\ ``Pattern``\ 模式可参考\ `正则表达式 <../../../../5-Wildcard/2-Regular/1-syntax/index.html>`_\ 


代码示例如下：

.. code-block:: sh

	#!/bin/bash
	echo "PATH variable is $PATH"
	echo "the length of PATH variable is ${#PATH}"

	file_name="linux.test.md"
	echo "${file_name%%.*}"
	echo "${file_name%.*}"
	echo "${file_name##*.}"
	echo "${file_name#*.}"
	echo "${file_name:0:5}"
	echo "${file_name:2}"

	test_str="/usr/bin:/root/bin:/usr/local/apache/bin:/usr/local/mysql:/usr/local/apache/bin"
	echo "${test_str/:\/usr\/local\/apache\/bin/}"   # 此处需要使用\对/进行转义，替换值为空表示删除前面匹配到的内容
	echo "${test_str//:\/usr\/local\/apache\/bin/}"  # 此处需要使用\对/进行转义，替换值为空表示删除前面匹配到的内容

	# 执行结果如下
	# PATH variable is /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
	# the length of PATH variable is 59
	# linux
	# linux.test
	# md
	# test.md
	# linux
	# nux.test.md
	# /usr/bin:/root/bin:/usr/local/mysql:/usr/local/apache/bin
	# /usr/bin:/root/bin:/usr/local/mysql


.. _arraysl:

0x02 数组型
~~~~~~~~~~~~~~

数组是一种数据结构，也可以叫做数据序列，它是一段连续的内容空间，保存了连续的多个数据(数据类型可以不相同)，可以使用数组index索引来访问操作数组元素

根据数组index索引的不同可将数组分为

- \ `普通数组 <#regulararray>`_\ ：数组index索引为整型数
- \ `关联数组 <#associaearray>`_\ ：数组index索引为字符串

.. _regulararray:

0x0200 普通数组
^^^^^^^^^^^^^^^^^^

普通数组也可以称为整型索引数组，它的声明定义方式有以下几种

.. code-block:: sh

	#!/bin/bash

	# 使用declare -a显式声明变量数据类型为整型索引数组型
	# 数组中各元素间使用空白字符分隔
	# 字符串类型的元素使用引号
	declare -a array1=(1 'b' 3 'a')
	# 依次引用数组的第一、二、三、四个元素
	# 不加下标时默认引用第一个元素
	# 引用时必须加上{}，否则$array1[0]的值为1[0]
	echo "the first element of array1 is ${array1[0]}"
	echo "the second element of array1 is ${array1[1]}"
	echo "the third element of array1 is ${array1[2]}"
	echo "the fourth element of array1 is ${array1[3]}"
	# 查看数组所有元素
	echo "all elements of array1 is ${array1[*]}"
	echo "all elements of array1 is ${array1[@]}"


	# 由解释器动态解释变量数据类型为整型索引数组型
	# 如果数组中各元素间使用逗号，则它们将作为一个整体，也就是数组索引0的值
	array2=(1,'b',3,'a')
	echo "the first element of array2 is ${array2[0]}"


	# 由解释器动态解释变量数据类型为整型索引数组型
	# 数组元素使用自定义下标赋值
	# 以下数组定义中，第一个元素是1，第二个元素是'b'，第3个元素为空，第4个元素为'a'
	array3=(1 'b' [3]='a')
	# 依次引用数组的第一、二、三、四个元素
	# 不加下标时默认引用第一个元素
	echo "the first element of array3 is ${array3[0]}"
	echo "the second element of array3 is ${array3[1]}"
	echo "the third element of array3 is ${array3[2]}"
	echo "the fourth element of array3 is ${array3[3]}"
	# 查看数组中所有有效元素(不为空)的整型索引号
	echo "the index of effective element is ${!array3[*]}"
	echo "the index of effective element is ${!array3[@]}"
	# 查看数组中的有效元素个数(只统计值不为空的元素)
	echo "the num of array3 is ${#array3[*]}"
	echo "the num of array3 is ${#array3[@]}"


	# 由解释器动态解释变量数据类型为整型索引数组型
	# 数组中每个元素被逐渐赋值
	array4[0]=1
	array4[1]='bc'
	array4[2]=3
	array4[3]='a'
	# 依次引用数组的第一、二、三、四个元素
	# 不加下标时默认引用第一个元素
	echo "the first element of array4 is ${array4[0]}"
	echo "the second element of array4 is ${array4[1]}"
	echo "the third element of array4 is ${array4[2]}"
	echo "the fourth element of array4 is ${array4[3]}"
	# 查看第二个元素的字符长度
	echo "the length of second element is ${#array4[1]}"


	# 执行结果如下
	# the first element of array1 is 1
	# the second element of array1 is b
	# the third element of array1 is 3
	# the fourth element of array1 is a
	# all elements of array1 is 1 b 3 a
	# all elements of array1 is 1 b 3 a
	# the first element of array2 is 1,b,3,a
	# the first element of array3 is 1
	# the second element of array3 is b
	# the third element of array3 is 
	# the fourth element of array3 is a
	# the index of effective element is 0 1 3
	# the index of effective element is 0 1 3
	# the num of array3 is 3
	# the num of array3 is 3
	# the first element of array4 is 1
	# the second element of array4 is bc
	# the third element of array4 is 3
	# the fourth element of array4 is a
	# the length of second element is 2

另外普通数组还支持以下运算操作

- 返回数组长度(即有效元素的个数，不包括空元素)

	- \ ``${#Array_Name[*]}``\ 
	- \ ``${#Array_Name[@]}``\ 
- 数组元素消除，该操作不会修改原数组元素，操作执行结果用数组来接收

	- \ ``Array_Name1=${Array_Name[*]#*word}``\ ：功能同下
	- \ ``Array_Name1=${Array_Name[*]##*word}``\ ：自左而右查找\ ``Array_Name``\ 数组中所有被匹配到的\ ``word``\ 匹配到的元素，并将所有匹配到的元素删除(并不会删除原数组中的元素)，最后返回剩余的数组元素
	- \ ``Array_Name1=${Array_Name[*]%word*}``\ ：功能同下
	- \ ``Array_Name1=${Array_Name[*]%%word*}``\ ：自右而左查找\ ``Array_Name``\ 数组中所有被匹配到的\ ``word``\ 匹配到的元素，并将所有匹配到的元素删除(并不会删除原数组中的元素)，最后返回剩余的数组元素
- 数组元素提取，该操作不会修改原数组元素，操作执行结果用数组来接收

	- \ ``Array_Name1=${Array_Name[*]:offset}``\ ：返回\ ``Array_Name``\ 数组中索引为\ ``offset``\ 的数组元素以及后面所有元素；其中\ ``offset``\ 为整型数
	- \ ``Array_Name1=${Array_Name[*]:offset:length}``\ ：返回\ ``Array_Name``\ 数组中索引为\ ``offset``\ 的数值元素以及后面\ ``length-1``\ 个元素；其中\ ``offset``\ 和\ ``length``\ 都为整型数
- 数组元素替换，该操作不会修改原数组元素，操作执行结果用数组来接收

	- \ ``Array_Name1=${Array_Name[*]/Pattern/Replaceplacement}``\ ：功能同下
	- \ ``Array_Name1=${Array_Name[*]//Pattern/Replaceplacement}``\ ：以\ ``Pattern``\ 为模式匹配\ ``Array_Name``\ 数组中的元素，将全部匹配到的替换为\ ``Replaceplacement``\ (不会修改原数组中的元素)，并返回全部数组元素；\ ``Pattern``\ 模式可参考\ `正则表达式 <../../../../5-Wildcard/2-Regular/1-syntax/index.html>`_\ 


代码示例如下

.. code-block:: sh

	#!/bin/bash

	array_test=(/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin)

	# 返回数组长度(即有效元素的个数，不包括空元素)
	echo "the length of array_test is ${#array_test[*]}"
	echo "the length of array_test is ${#array_test[@]}"

	# 数组元素消除，该操作不会修改原数组元素，操作执行结果用数组来接收
	array_test1=${array_test[*]#*/usr/apache/bin}
	echo "array_test:${array_test[*]}"
	echo "array_test1:${array_test1[@]}"
	array_test2=${array_test[*]##*/usr/apache/bin}
	echo "array_test:${array_test[*]}"
	echo "array_test2:${array_test2[@]}"
	array_test3=${array_test[*]%/usr/apache/bin*}
	echo "array_test:${array_test[*]}"
	echo "array_test3:${array_test3[@]}"
	array_test4=${array_test[*]%%/usr/apache/bin*}
	echo "array_test:${array_test[*]}"
	echo "array_test4:${array_test4[@]}"

	# 数组元素提取，该操作不会修改原数组元素，操作执行结果用数组来接收
	array_test5=${array_test[*]:2}
	echo "array_test:${array_test[*]}"
	echo "array_test5:${array_test5[@]}"
	array_test6=${array_test[*]:2:2}
	echo "array_test:${array_test[*]}"
	echo "array_test6:${array_test6[@]}"

	# 数组元素替换，该操作不会修改原数组元素，操作执行结果用数组来接收
	array_test7=${array_test[*]/\/usr\/apache\/bin/}   # 需要用\对/进行转义，替换值为空表示删除前面匹配到的
	echo "array_test:${array_test[*]}"
	echo "array_test7:${array_test7[@]}"
	array_test8=${array_test[*]//\/usr\/apache\/bin/}  # 需要用\对/进行转义，替换值为空表示删除前面匹配到的
	echo "array_test:${array_test[*]}"
	echo "array_test8:${array_test8[@]}"

	# 执行结果如下
	# the length of array_test is 5
	# the length of array_test is 5
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test1:/usr/bin /root/bin /usr/mysql
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test2:/usr/bin /root/bin /usr/mysql
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test3:/usr/bin /root/bin /usr/mysql
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test4:/usr/bin /root/bin /usr/mysql
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test5:/usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# varray_test6:/usr/apache/bin /usr/mysql
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test7:/usr/bin /root/bin /usr/mysql
	# array_test:/usr/bin /root/bin /usr/apache/bin /usr/mysql /usr/apache/bin
	# array_test8:/usr/bin /root/bin /usr/mysql


.. _forlooppl:

同时普通数组也可用于for循环遍历

代码示例如下

.. code-block:: sh

	#!/bin/bash

	# 获取家目录下文件列表，转换成普通数组
	array_test=(`ls ~`)
	echo ${array_test[@]}
	echo "----------------"

	# 以数组元素值的方式直接遍历数组
	for i in ${array_test[*]};do
	        echo $i
	done
	echo "----------------"

	# 以数组index索引的方式遍历数组
	for i in ${!array_test[*]};do
	        echo ${array_test[$i]}
	done
	echo "----------------"

	# 以数组元素个数的方式遍历数组
	for ((i=0;i<${#array_test[*]};i++));do
	        echo ${array_test[$i]}
	done

	# 执行结果如下
	# anaconda-ks.cfg demo.sh test1.sh test.sh
	# ----------------
	# anaconda-ks.cfg
	# emo.sh
	# est1.sh
	# test.sh
	# ----------------
	# anaconda-ks.cfg
	# demo.sh
	# test1.sh
	# test.sh
	# ----------------
	# anaconda-ks.cfg
	# demo.sh
	# test1.sh
	# test.sh


.. _associaearray:

0x0201 关联数组
^^^^^^^^^^^^^^^^^^

关联数组也可以称为字符索引数组，它的声明定义方式有以下几种

.. code-block:: sh

	#!/bin/bash

	# 声明定义字符索引数组时必须使用declare -A
	# 数组中各元素间使用空白字符分隔
	declare -A array1=([name1]=jack [name2]=anony)
	# 依次引用name1和name2对应的值
	echo "the value of name1 element is ${array1[name1]}"
	echo "the value of name2 element is ${array1[name2]}"


	# 声明定义字符索引数组时必须使用declare -A
	# 如果数组中各元素间使用逗号，则它们将作为一个整体
	declare -A array2=([name1]=jack,[name2]=anony)
	echo "the value of name1 element is ${array2[name1]}"
	# 查看name1对应值的字符长度
	echo "the length of name1 element is ${#array2[name1]}"


	# 声明定义字符索引数组时必须使用declare -A
	declare -A array3=([name1]=jack [name2]=anony)
	echo "the value of name1 element is ${array3[name1]}"
	echo "the value of name2 element is ${array3[name2]}"
	# 通过字符索引进行赋值
	array3[name3]=zhangsan
	echo "the value of name3 element is ${array3[name3]}"
	# 通过字符索引进行赋值
	array3[name5]=lisi
	# 查看数组所有元素
	echo "the all effective element is ${array3[*]}"
	echo "the all effective element is ${array3[@]}"
	# 查看数组中所有有效元素(不为空)的字符索引号，默认是对应值的排列顺序
	echo "the index of all effective element is ${!array3[*]}"
	echo "the index of all effective element is ${!array3[@]}"
	# 查看数组中的有效元素个数(只统计值不为空的元素)
	echo "the length of array is ${#array3[*]}"
	echo "the length of array is ${#array3[@]}"

	# 执行结果如下
	# the value of name1 element is jack
	# the value of name2 element is anony
	# the value of name1 element is jack,[name2]=anony
	# the length of name1 element is 18
	# the value of name1 element is jack
	# the value of name2 element is anony
	# the value of name3 element is zhangsan
	# the all effective element is zhangsan anony jack lisi
	# the all effective element is zhangsan anony jack lisi
	# the index of all effective element is name3 name2 name1 name5
	# the index of all effective element is name3 name2 name1 name5
	# the length of array is 4
	# the length of array is 4

和普通数组一样，关联数组也支持以下运算操作

- 返回数组长度(即有效元素的个数，不包括空元素)

	- \ ``${#Array_Name[*]}``\ 
	- \ ``${#Array_Name[@]}``\ 
- 数组元素消除，该操作不会修改原数组元素，操作执行结果用数组来接收

	- \ ``declare -A Array_Name1=${Array_Name[*]#*word}``\ ：功能同下
	- \ ``declare -A Array_Name1=${Array_Name[*]##*word}``\ ：自左而右查找\ ``Array_Name``\ 数组中所有被匹配到的\ ``word``\ 匹配到的元素，并将所有匹配到的元素删除(并不会删除原数组中的元素)，最后返回剩余的数组元素
	- \ ``declare -A Array_Name1=${Array_Name[*]%word*}``\ ：功能同下
	- \ ``declare -A Array_Name1=${Array_Name[*]%%word*}``\ ：自右而左查找\ ``Array_Name``\ 数组中所有被匹配到的\ ``word``\ 匹配到的元素，并将所有匹配到的元素删除(并不会删除原数组中的元素)，最后返回剩余的数组元素
- 数组元素提取，该操作不会修改原数组元素，操作执行结果用数组来接收

	- \ ``declare -A Array_Name1=${Array_Name[*]:offset}``\ ：返回\ ``Array_Name``\ 数组中索引为\ ``offset``\ 的数组元素以及后面所有元素；其中\ ``offset``\ 为整型数
	- \ ``declare -A Array_Name1=${Array_Name[*]:offset:length}``\ ：返回\ ``Array_Name``\ 数组中索引为\ ``offset``\ 的数值元素以及后面\ ``length-1``\ 个元素；其中\ ``offset``\ 和\ ``length``\ 都为整型数
- 数组元素替换，该操作不会修改原数组元素，操作执行结果用数组来接收

	- \ ``declare -A Array_Name1=${Array_Name[*]/Pattern/Replaceplacement}``\ ：功能同下
	- \ ``declare -A Array_Name1=${Array_Name[*]//Pattern/Replaceplacement}``\ ：以\ ``Pattern``\ 为模式匹配\ ``Array_Name``\ 数组中的元素，将全部匹配到的替换为\ ``Replaceplacement``\ (不会修改原数组中的元素)，并返回全部数组元素；\ ``Pattern``\ 模式可参考\ `正则表达式 <../../../../5-Wildcard/2-Regular/1-syntax/index.html>`_\ 

代码示例如下

.. code-block:: sh

	#!/bin/bash

	declare -A array_test=([ele1]=/usr/bin [ele2]=/root/bin [ele3]=/usr/apache/bin [ele4]=/usr/mysql [ele5]=/usr/apache/bin)

	# 返回数组长度(即有效元素的个数，不包括空元素)
	echo "the length of array_test is ${#array_test[*]}"
	echo "the length of array_test is ${#array_test[@]}"

	# 数组元素消除，该操作不会修改原数组元素，操作执行结果用数组来接收
	declare -A array_test1=${array_test[*]#*/usr/apache/bin}
	echo "array_test:${array_test[*]}"
	echo "array_test1:${array_test1[@]}"
	declare -A array_test2=${array_test[*]##*/usr/apache/bin}
	echo "array_test:${array_test[*]}"
	echo "array_test2:${array_test2[@]}"
	declare -A array_test3=${array_test[*]%/usr/apache/bin*}
	echo "array_test:${array_test[*]}"
	echo "array_test3:${array_test3[@]}"
	declare -A array_test4=${array_test[*]%%/usr/apache/bin*}
	echo "array_test:${array_test[*]}"
	echo "array_test4:${array_test4[@]}"

	# 数组元素提取，该操作不会修改原数组元素，操作执行结果用数组来接收
	declare -A array_test5=${array_test[*]:2}
	echo "array_test:${array_test[*]}"
	echo "array_test5:${array_test5[@]}"
	declare -A array_test6=${array_test[*]:2:2}
	echo "array_test:${array_test[*]}"
	echo "array_test6:${array_test6[@]}"

	# 数组元素替换，该操作不会修改原数组元素，操作执行结果用数组来接收
	declare -A array_test7=${array_test[*]/\/usr\/apache\/bin/}
	echo "array_test:${array_test[*]}"
	echo "array_test7:${array_test7[@]}"
	declare -A array_test8=${array_test[*]//\/usr\/apache\/bin/}
	echo "array_test:${array_test[*]}"
	echo "array_test8:${array_test8[@]}"

	# 执行结果如下
	# the length of array_test is 5
	# the length of array_test is 5
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test1:/usr/mysql  /usr/bin /root/bin 
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test2:/usr/mysql  /usr/bin /root/bin 
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test3:/usr/mysql  /usr/bin /root/bin 
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test4:/usr/mysql  /usr/bin /root/bin 
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test5:/usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test6:/usr/apache/bin /usr/bin
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test7:/usr/mysql  /usr/bin /root/bin 
	# array_test:/usr/mysql /usr/apache/bin /usr/bin /root/bin /usr/apache/bin
	# array_test8:/usr/mysql  /usr/bin /root/bin 

.. _forloopgl:

关联数组和普通数组一样，也可用于for循环遍历

先创建\ ``test.log``\ 文件，内容如下

.. code-block:: sh
	
	#cat ~/test.log
	portmapper
	portmapper
	portmapper
	portmapper
	portmapper
	portmapper
	status
	status
	mountd
	mountd
	mountd
	mountd
	mountd
	mountd
	nfs
	nfs
	nfs_acl
	nfs
	nfs
	nfs_acl
	nlockmgr
	nlockmgr
	nlockmgr
	nlockmgr
	nlockmgr
	nlockmgr

代码示例如下：统计文件中重复行的次数

.. code-block:: sh

	#!/bin/bash

	declare -A array_test

	for i in `cat ~/test.log`;do
	        let ++array_test[$i]  # 修改数组元素值
	done

	for j in ${!array_test[*]};do
	        printf "%-15s %3s\n" $j :${array_test[$j]}
	done

	# 执行结果如下
	# status           :2
	# nfs              :4
	# portmapper       :6
	# nlockmgr         :6
	# nfs_acl          :2
	# mountd           :6


.. _listsl:

0x03 列表型
~~~~~~~~~~~~~

列表型变量常用来for循环遍历，但是一般是在for循环中直接使用，当然也可以通过变量进行引用

.. _forlistl:

.. _forlistll:

代码示例如下

.. code-block:: sh

	#!/bin/bash

	# 生成数字列表：使用{}运算符
	for i in {1..4};do
	        echo $i
	done
	echo "-------------------"

	# 生成数字列表：使用seq命令
	for i in `seq 1 2 7`;do
	        echo $i
	done
	echo "-------------------"

	# 生成文件列表：直接给出列表
	for fileName in /etc/init.d/functions /etc/rc.d/rc.sysinit /etc/fstab;do
	        echo $fileName
	done
	echo "-------------------"

	# 生成文件列表：使用文件名通配机制生成列表
	dirName=/etc/rc.d
	for fileName in $dirName/*.d;do
	        echo $fileName
	done
	echo "-------------------"

	# 生成文件列表：使用``运算符引用相关命令的执行结果
	for fileName in `ls ~`;do
	        echo $fileName
	done

	# 执行结果如下
	# 1
	# 2
	# 3
	#4
	# -------------------
	# 1
	# 3
	# 5
	# 7
	# -------------------
	# /etc/init.d/functions
	# /etc/rc.d/rc.sysinit
	# /etc/fstab
	# -------------------
	# /etc/rc.d/init.d
	# /etc/rc.d/rc0.d
	# /etc/rc.d/rc1.d
	# /etc/rc.d/rc2.d
	# /etc/rc.d/rc3.d
	# /etc/rc.d/rc4.d
	# /etc/rc.d/rc5.d
	# /etc/rc.d/rc6.d
	# -------------------
	# anaconda-ks.cfg
	# demo.sh
	# test1.sh
	# test.log
	# test.sh


