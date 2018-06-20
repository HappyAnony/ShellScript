函数
=================

在编程语言中，函数是能够实现模块化编程的工具，每个函数都是一个功能组件，但是函数必须被调用才能执行

函数存在的主要作用在于：最大化代码重用，最小化代码冗余

在shell中，函数可以被当做命令一样执行，它的本质是命令的组合结构体，即可以将函数看成一个普通命令或一个小型脚本。接下来本章内容将从以下几个方面来介绍函数

- \ `函数定义 <#funcdefine>`_\ 
- \ `函数调用 <#funccall>`_\ 
- \ `函数退出 <#funcexit>`_\ 
- \ `示例代码 <#funccode>`_\ 


.. _funcdefine:

0x00 函数定义
~~~~~~~~~~~~~~~~

在shell中函数定义的方法有两种(使用\ ``help function``\ 命令可以查看)

.. code-block:: sh

	# 方法一
	function FuncName {
		COMMANDS_LIST
	} [&>/dev/null]

	# 方法二
	FuncName() {
		COMMANDS_LIST
	} [&>/dev/null]

上面两种函数定义方法定义了一个名为\ ``FuncName``\ 的函数

- 方法一中：使用了\ ``function``\ 关键字，此时函数名\ ``FuncName``\ 后面的括号可以省略
- 方法二中：省略了\ ``function``\ 关键字，此时函数名\ ``FuncName``\ 后面的括号不能省略

\ ``COMMANDS_LIST``\ 是函数体，它与以下特点

- 函数体通常使用大括号\ ``{}``\ 包围，由于历史原因，在shell中大括号本身也是关键字，所以为了不产生歧义，函数体和大括号之间必须使用\ ``空格、制表符、换行符``\ 分隔开来；一般我们都是通过换行符进行分隔
- 函数体中的每一个命令必须使用\ ``;``\ 或\ ``换行符``\ 进行分隔；如果使用\ ``&``\ 结束某条命令，则表示该条命令会放入后台执行

需要注意的是

- \ ``&>/dev/null``\ 表示将函数体执行过程中可能输出的信息重定向至\ ``/dev/null``\ 中，该功能可选
- 定义函数时，还可以指定可选的函数重定向功能，这样当函数被调用的时候，指定的重定向也会被执行
- 当前shell定义的函数只能在当前shell使用，子shell无法继承父shell的函数定义，除非使用\ ``export -f``\ 将函数导出为全局函数；如果想取消函数的导出可以使用\ ``export -n``\ 
- 定义了函数后，可以使用\ ``unset -f``\ 移除当前shell中已定义的函数
- 可以使用\ ``typeset -f [func_name]``\ 或\ ``declare -f [func_name]``\ 查看当前shell已定义的函数名和对应的定义语句；使用\ ``typeset -F``\ 或\ ``declare -F``\ 则只显示当前shell中已定义的函数名
- 只有先定义了函数，才可以调用函数；不允许函数调用语句在函数定义语句之前
- 在shell脚本中，函数没有形参的概念，使用方法二定义函数时，括号里什么都不用写，只需要在函数体内使用相关的调用机制调用接收参数即可


.. _funccall:

0x01 函数调用
~~~~~~~~~~~~~~~~

函数的调用格式如下

.. code-block:: sh

	FuncName ARGS_LIST

其中

- \ ``FuncName``\ ：表示被调用函数的函数名，需要注意的是在shell中函数调用时函数名后面没有\ ``()``\ 操作符
- \ ``ARGS_LIST``\ ：表示被调用函数的传入参数，在shell中给函数传入参数和脚本接收参数的方法相似，直接在函数名后面加上需要传入的参数即可

函数调用时需要注意以下几点

- 如果函数名和命令名相同，则优先执行函数，除非使用\ ``command``\ 命令。例如：定义了一个名为\ ``rm``\ 的函数，在bash中输入\ ``rm``\ 执行时，执行的是\ ``rm函数``\ ，而非\ ``/bin/rm命令``\ ，除非使用\ ``command rm ARGS``\ ，表示执行的是\ ``/bin/rm命令``\ 
- 如果函数名和命令别名相同，则优先执行命令别名，即在优先级方面：\ ``别名别名>函数>命令自身``\ 

当函数调用函数被执行时，它的执行逻辑如下

- 接收参数：shell函数也接受位置参数变量，但函数的位置参数是调用函数时传递给函数的，而非传递给脚本的参数，所以脚本的位置变量和函数的位置变量是不同的；同时shell函数也接收特殊变量。函数体内引用位置参数和特殊变量方式如下

	- 位置参数

		- \ ``$0``\ ：和脚本位置参数一样，引用脚本名称
		- \ ``$1``\ ：引用函数的第1个传入参数
		- \ ``$n``\ ：引用函数的第n个传入参数
	- 特殊变量

		- \ ``$?``\ ：引用上一条命令的执行状态返回值，状态用数字表示\ ``0-255``\ 

			- \ ``0``\ ：表示成功
			- \ ``1-255``\ ：表示失败；其中\ ``1/2/127/255``\ 是系统预留的，写脚本时要避开与这些值重复
		- \ ``$$``\ ：引用当前shell的PID。除了执行bash命令和shell脚本时，$$不会继承父shell的值，其他类型的子shell都继承
		- \ ``$!``\ ：引用最近一次执行的后台进程PID，即运行于后台的最后一个作业的PID
		- \ ``$#``\ ：引用函数所有位置参数的个数
		- \ ``$*``\ ：引用函数所有位置参数的整体，即所有参数被当做一个字符串
		- \ ``$@``\ ：引用函数所有单个位置参数，即每个参数都是一个独立的字符串
- 执行函数体：在函数体执行时，需要注意的是

	- 函数内部引用变量的查找次序：\ ``内层函数自己的变量>外层函数的变量>主程序的变量>bash内置的环境变量``\ 
	- 函数内部引用变量的作用域

		- \ `本地变量 <../3-variable/index.html#locall>`_\ ：函数体引用本地变量时，重新赋值会覆盖原来的值，如果不想覆盖值，可以使用\ ``local``\ 进行修饰
		- \ `局部变量 <../3-variable/index.html#sidel>`_\ ：函数体引用局部变量时，函数退出，将会被撤销
		- \ `环境变量 <../3-variable/index.html#envl>`_\ ：函数体引用环境变量时，重新赋值会覆盖原来的值，如果不想覆盖值，可以使用\ ``local``\ 进行修饰
		- \ `位置变量 <../3-variable/index.html#positionl>`_\ ：函数体引用位置变量表示引用传递给函数的参数
		- \ `特殊变量 <../3-variable/index.html#speciall>`_\ 
- 函数返回：函数返回值可分为两类

	- 执行结果返回值：正常的执行结果返回值有以下几种

		- 函数中的打印语句：如\ ``echo``\ 、\ ``print``\ 等
		- 最后一条命令语句的执行结果值
	- 执行状态返回值：执行状态返回值主要有以下几种

		- 使用\ ``return``\ 语句自定义返回值，即return n，n表示函数的退出状态码，不给定状态码时默认状态码为0
		- 取决于函数体中最后一条命令语句的执行状态返回值


在shell中不仅可以调用本脚本文件中定义的函数，还可以调用其它脚本文件中定义的函数

- 先使用\ ``. /path/to/shellscript``\ 或\ ``source /path/to/shellscript``\ 命令导入指定的脚本文件
- 然后使用相应的函数名调用函数即可

.. _funcexit:

0x02 函数退出命令
~~~~~~~~~~~~~~~~~~~

函数退出命令有

- \ ``return [n]``\ ：可以在函数体内的任何地方使用，表示退出整个函数；数值n表示函数的退出状态码
- \ ``exit [n]``\ ：可以在脚本的任何地方使用，表示退出整个脚本；数值n表示脚本的退出状态码

此处需要注意的是：\ ``return``\ 并非只能用于\ ``function内部``\ 

- 如果\ ``return``\ 在\ ``function之外``\ ，但在\ ``.``\ 或者\ ``source``\ 命令的执行过程中，则直接停止该执行操作，并返回给定状态码n(如果未给定，则为0)
- 如果\ ``return``\ 在\ ``function之外``\ ，且不在\ ``source``\ 或\ ``.``\ 的执行过程中，则这将是一个错误用法

可能有些人不理解为什么不直接使用\ ``exit``\ 来替代这时候的\ ``return``\ 。下面给个例子就能清楚地区分它们

先创建一个脚本文件\ ``proxy.sh``\ ，内容如下，用于根据情况设置代理的环境变量

.. code-block:: sh

	#!/bin/bash

	proxy="http://127.0.0.1:8118"
	function exp_proxy() {
	        export http_proxy=$proxy
	        export https_proxy=$proxy
	        export ftp_proxy=$proxy
	        export no_proxy=localhost
	}

	case $1 in 
	        set) exp_proxy;;
	        unset) unset http_proxy https_proxy ftp_proxy no_proxy;;
	        *) return 0
	esac

首先我们来了解下\ ``source``\ 的特性：即\ ``source``\ 是在当前shell而非子shell执行指定脚本中的代码

当进入bash

- 需要设置环境变量时：使用\ ``source proxy.sh set``\ 即可
- 需要取消环境变量时：使用\ ``source proxy.sh unset``\ 即可

此时如果不清楚该脚本的用途或者一时手快直接输入\ ``source proxy.sh``\ ，就可以区分\ ``exit``\ 和\ ``return``\ 

- 如果上述脚本是\ ``return 0``\ ，那么表示直接退出脚本而已，不会退出bash
- 如果上述脚本是\ ``exit 0``\ ，则表示退出当前bash，因为\ ``source``\ 是在当前shell而非子shell执行指定脚本中的代码

可能你想象不出在source执行中的return有何用处：从source来考虑，它除了用在某些脚本中加载其他环境，更主要的是在bash环境初始化脚本中使用，例如\ ``/etc/profile``\ 、\ ``~/.bashrc``\ 等，如果你在\ ``/etc/profile``\ 中用\ ``exit``\ 来替代\ ``function外面``\ 的\ ``return``\ ，那么永远也登陆不上\ ``bash``\ 


.. _funccode:

0x03 示例代码
~~~~~~~~~~~~~~~

- 随机生成密码

.. code-block:: sh

	#!/bin/bash

	genpasswd(){
	        local l=$1
	        [ "$l" == ""  ]&& l=20
	        tr -dc A-Za-z0-9_</dev/urandom | head -c ${l} | xargs
	}

	genpasswd $1   # 将脚本传入的位置参数传递给函数，表示生成的随机密码的位数

- 写一个脚本，完成如下功能：

	- 1、脚本使用格式：\ ``mkscript.sh [-D|--description "script description"] [-A|--author "script author"] /path/to/somefile``\ 
	- 2、如果文件事先不存在，则创建；且前几行内容如下所示：

		- #!/bin/bash
		- # Description: script description
		- # Author: script author
	- 3、如果事先存在，但不空，且第一行不是\ ``#!/bin/bash``\ ，则提示错误并退出；如果第一行是\ ``#!/bin/bash``\ ，则使用vim打开脚本；把光标直接定位至最后一行
	- 4、打开脚本后关闭时判断脚本是否有语法错误；如果有，提示输入y继续编辑，输入n放弃并退出；如果没有，则给此文件以执行权限

.. code-block:: sh

	#!/bin/bash
	read -p "Enter a file: " filename
	declare authname
	declare descr

	options(){
	if [[ $# -ge 0 ]];then
		case $1 in
	    -D|--description)
	    	authname=$4
	     	descr=$2
	     	;;
	    -A|--author)
	    	descr=$4
	     	authname=$2
	      	;;
	   	esac
	fi
	}

	command(){
	if  bash -n $filename &> /dev/null;then
		chmod +x $filename
	else
	    while true;do
	    	read -p "[y|n]:" option
	    	case $option in
	     	y)
	       		vim + $filename
	       		;;
	     	n)
	       		exit 8
	       		;;
	    	esac
	   	done
	fi
	exit 6
	}

	oneline(){
	if [[ -f $filename ]];then
		if [ `head -1 $filename` == "#!/bin/bash" ];then
	    	vim + $filename  
		else 
	    	echo "wrong..."
	    	exit 4
		fi
	else
	 	touch $filename && echo -e "#!/bin/bash\n# Description: $descr\n# Author: $authname" > $filename
	 	vim + $filename
	fi
	command
	}

	options $*
	oneline


- 写一个脚本，完成如下功能：

	- 1、提示用户输入一个可执行命令
	- 2、获取这个命令所依赖的所有库文件(使用ldd命令)
	- 3、复制命令至\ ``/mnt/sysroot/``\ 对应的目录中；如果复制的是\ ``cat``\ 命令，其可执行程序的路径是\ ``/bin/cat``\ ，那么就要将\ ``/bin/cat``\ 复制到\ ``/mnt/sysroot/bin/``\ 目录中，如果复制的是\ ``useradd``\ 命令，而\ ``useradd``\ 的可执行文件路径为\ ``/usr/sbin/useradd``\ ，那么就要将其复制到\ ``/mnt/sysroot/usr/sbin/``\ 目录中
	- 4、复制各库文件至\ ``/mnt/sysroot/``\ 对应的目录中

.. code-block:: sh

	#!/bin/bash

	options(){
		for i in $*;do
			dirname=`dirname $i`
			[ -d /mnt/sysroot$dirname ] || mkdir -p /mnt/sysroot$dirname
			[ -f /mnt/sysroot$i ]||cp $i /mnt/sysroot$dirname/
		done
	} 

	while true;do
		read -p "Enter a command : " pidname
		[[ "$pidname" == "quit" ]] && echo "Quit " && exit 0
		bash=`which --skip-alias $pidname`
		if [[ -x $bash ]];then
	 		options `/usr/bin/ldd $bash |grep -o "/[^[:space:]]\{1,\}"`
			options $bash
		else
			echo "PLZ a command!"
		fi
	done

	# 说明
	# 将bash命令的相关bin文件和lib文件复制到/mnt/sysroot/目录中后
	# 使用chroot命令可切换根目录，切换到/mnt/sysroot/后可当做bash执行复制到该处的命令，作为bash中的bash

- 写一个脚本，用来判定172.16.0.0网络内有哪些主机在线，在线的用绿色显示，不在线的用红色显示

.. code-block:: sh

	#!/bin/bash
	Cnetping(){
		for i in {1..254};do
	    	ping -c 1 -w 1 $1.$i
	    	if [[ $? -eq 0 ]];then
	    		echo -e -n "\033[32mping 172.16.$i.$j ke da !\033[0m\n"
	    	else
	    		echo -e -n "\033[31mping 172.16.$i.$j bu ke da !\033[0m \n"
	    	fi
	   	done
	}

	Bnetping(){
		for j in {0..255};do
			Cnetping $1.$j
		done
	}

	Bnetping 172.16


- 写一个脚本，用来判定随意输入的ip地址所在网段内有哪些主机在线，在线的用绿色显示，不在线的用红色显示

.. code-block:: sh


	#!/bin/bash
	Cnetping(){
		for i in {1..254};do
	    	ping -c 1 -w 1 $1.$i
	    	if [[ $? -eq 0 ]];then
	    		echo -e -n "\033[32mping 172.16.$i.$j ke da !\033[0m\n"
	    	else
	    		echo -e -n "\033[31mping 172.16.$i.$j bu ke da !\033[0m \n"
	    	fi
	   	done
	}

	Bnetping(){
		for j in {0..255};do
			Cnetping $1.$j
		done
	}

	Anetping(){
		for m in {0.255};do
			Bnetping $1.$m
		done
	}

	netType=`echo $1 | cut -d'.' -f1`

	if [ $netType -gt 0 -a $netType -le 126 ];then
		Anetping $1
	elif [ $netType -ge 128 -a $netType -le 191 ];then
		Bnetping $1
	elif [ $netType -ge 192 -a $netType -le 223 ];then
		Cnetping $1
	else
		echo "Wrong"
		exit 3
	fi