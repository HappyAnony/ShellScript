示例脚本
=========

- 写一个脚本，实现如下功能：让用户通过键盘输入一个用户名，如果用户存在，就显示其用户名和UID，否则，就显示用户不存在

.. code-block:: sh

	#!/bin/bash

	read -p "please input userName: " userName
	if grep "^$userName\>" /etc/passwd &> /dev/null;then
		echo "$userName :`id -u $userName`";
	else
		echo "$userName is not exist !!";
	fi

- 写一脚本，实现如下功能

	- 1、让用户通过键盘输入一个用户名，如果用户不存在就退出
	- 2、如果用户的UID大于等于500，就说明它是普通用户
	- 3、否则，就说明这是管理员或系统用户

.. code-block:: sh

	#!/bin/bash

	read -p "please input userName: " userName

	if ! grep "^$userName\>" /etc/passwd &> /dev/null;then
		echo "$userName  not exist"
		exit 6
	fi 

	uid=`id -u $userName`
	if [ $uid -ge 500 ];then
		echo "The $userName is common user"
	else
		echo "The $userName is system user"
	fi


- 写一脚本，实现如下功能

	- 1、让用户通过键盘输入一个用户名，如果用户不存在就退出
	- 2、如果其UID等于其GID，就说它是个"good guy"
	- 3、否则，就说它是个"bad guy"

.. code-block:: sh

	#!/bin/bash
	read -p "please input userName: " userName

	if ! grep "^$userName\>" /etc/passwd &> /dev/null;then
		echo "$userName not exist"
		exit 62
	fi

	if [ `id -u $userName` -eq `id -g $userName` ];then
		echo "$userName is good guy"
	else
		echo "$userName is bad guy"
	fi

- 判断当前系统的所有用户是goodguy还是badguy

.. code-block:: sh

	#!/bin/bash

	for userName in `cut -d: -f1 /etc/passwd`;do
		if [ `id -u $userName` -eq `id -g $userName` ];then
			echo "$userName is good guy"
		else
			echo "$userName is bad guy"
		fi
	done

- 写一个脚本，实现如下功能

	- 1、添加10个用户stu1-stu10；但要先判断用户是否存在
	- 2、如果存在，就用红色显示其已经存大在
	- 3、否则，就添加此用户；并绿色显示
	- 4、最后显示一共添加了几个用户

.. code-block:: sh

	declare -i userCount=0

	for i in {1..10};do
		if grep "^stu$i\>" /etc/passwd &> /dev/null;then
			echo -e "\033[31mstu$i\033[0m exist"
		else
			useradd stu$i && echo -e "useradd \033[32mstu$i\033[0m finished"
			let userCount++
		fi
	done

	echo "Add $userCount users"

- 判断当前系统中所有用户是否拥有可登录shell

.. code-block:: sh

	#!/bin/bash

	for userName in `cut -d: -f1 /etc/passwd`; do
		if [[ `grep "^$userName\>" /etc/passwd | cut -d: -f7` =~ sh$ ]];then
			echo "login shell user: $userName"
		else
			echo "nologin shell user: $userName"
		fi
	done

- 写一个脚本，实现如下功能

	- 1.显示如下菜单

		- cpu) show cpu info
		- mem) show memory info
		- quit) quit
	- 2.如果用户选择cpu，则显示/proc/cpuinfo的信息
	- 3.如果用户选择mem，则显示/proc/meminfo的信息
	- 4.如果用户选择quit，则退出，且退出码为5
	- 5.如果用户键入其它字符，则显示未知选项，请重新输入

.. code-block:: sh

	#!/bin/bash

	info="cpu) show cpu info\nmem) show memory info\nquit) quit"
	while true;do
		echo -e $info

		read -p "Enter your option: " userOption
		userOption=`echo $userOption | tr 'A-Z' 'a-z'`

		if [[ "$userOption" == "cpu" ]];then
			cat /proc/cpuinfo
		elif [[ "$userOption" == "mem" ]];then
			cat /proc/meminfo
		elif [[ "$userOption" == "quit" ]];then
			echo "quit"
			retValue=5
			break
		else
			echo "unkown option"
			retValue=6
		fi
	done

	[ -z $retValue ] && retValue=0

	exit $retValue

- 写一个脚本，实现如下功能

	- 1.分别复制/var/log下的文件至/tmp/logs目录中
	- 2.复制目录时，使用cp -r
	- 3.复制文件时，使用cp
	- 4.复制链接文件时，使用cp -d
	- 5.余下的类型，使用cp -a

.. code-block:: sh

	#!/bin/bash

	targetDir='/tmp/logs'

	[ -e $targetDir ] && mkdir -p $targetDir

	for fileName in /var/log/*;do
		if [ -d $fileName ]; then
			copyCmd='cp -r'
		elif [ -f $fileName ]; then
			copyCmd='cp'
		elif [ -h $fileName ]; then
			copyCmd='cp -d'
		else
			copyCmd='cp -a'
		fi

		$copyCmd $fileName $targetDir
	done

- 写一个脚本，使用形式：\ ``userinfo.sh -u username [-v {1|2}]``\ 

	- \ ``-u``\ 选项用于指定用户，而后脚本显示用户的UID和GID
	- \ ``-v``\ 选项后面是1，则显示用户的家目录路径；如果是2，则显示用户的家目录路径和shell

.. code-block:: sh

	#!/bin/bash

	[ $# -lt 2 ] && echo "less arguments" && exit 3

	if [[ "$1" == "-u" ]]; then
		userName="$2"
		shift 2       # 剔除前2个位置参数
	fi

	if [[ $# -ge 2 ]] && [ "$1" == "-v" ]; then
		verFlag=$2
	fi
	
	verFlag=${verFlag:-0}

	if [ -n $verFlag ]; then
		if ! [[ $verFlag =~ [012] ]]; then
			echo "Wrong Parameter"
			echo "Usage: `basename $0` -u UserName -v {1|2}"
			exit 4
		fi
	fi

	if [ $verFlag -eq 1 ];then
		grep "^$userName" /etc/passwd | cut -d: -f1,3,4,6
	elif [ $verFlag -eq 2 ];then
		grep "^$userName" /etc/passwd | cut -d: -f1,3,4,6,7
	else
		grep "^$userName" /etc/passwd | cut -d: -f1,3,4
	fi

- 写一个脚本，实现功能如下

	- 提示用户输入一个用户名，判断用户是否登录了当前系统
	- 如果没有登录，则停止5秒之后，再次判定；直到用户登陆系统，显示用户来了，然后退出

.. code-block:: sh

	#!/bin/bash

	read -p "Enter a user name: " userName

	# 判断输入是否为空并且是否存在该用户
	until [ -n "$userName" ] && id $userName &> /dev/null; do
		read -p "Enter a user name again: " userName
	done

	until who | grep "^$userName" &> /dev/null; do
		echo "$userName is offline"
		sleep 5
	done

	echo "$userName is online"

- 写一个脚本，实现功能如下

	- 1.提示用户输入一个磁盘设备文件路径不存在或不是一个块设备，则提示用户重新输入，知道输入正确为止，或者输入quit以9为退出码结束脚本
	- 2.提示用户"下面的操作会清空磁盘的数据，并提问是否继续"。如果用户给出字符y或yes，则继续，否则，则提供以8为退出码结束脚本
	- 3.将用户指定的磁盘上的分区清空，而后创建两个分区，大小分别为100M和512M
	- 4.格式化这两个分区
	- 5.将第一个分区挂载至/mnt/boot目录，第二个分区挂载至/mnt/sysroot目录


.. code-block:: sh

	#！/bin/bash
	read -p "Enter you dev " devdir
	umonut /mnt/boot
	umonut /mnt/sysroot

	while [[ "$devdir" != "quit" ]];do
		[ -a $devdir ] && [ -b $devdir ]
		if [[ $? -eq 0 ]];then
			read -p "Are you sure[y|yes]: " option
			if [[ "$option" == "y" || "$option" == "yes" ]];then
				dd if=/dev/zero of=$devdir bs=512 count=1 &> /dev/null
				echo -e "n\np\n1\n\n+100M\nn\np\n2\n\n+512M\nw" | fdisk $devdir
				mke2fs -t ext4 ${devdir}1
				mke2fs -t ext4 ${devdir}2
				mount ${devdir}1 /mnt/boot
				mount ${devdir}2 /mnt/sysroot
				echo "${devdir}1 /mnt/boot ext4 default 0 0" >> /etc/fstab
				echo "${devdir}2 /mnt/sysroot ext4 default 0 0" >> /etc/fstab
				exit 7
			else
				exit 8
			fi
	    else
	    	read -p "Enter you dev again:　"　devdir
	    fi
	done

	exit 9

- 写一个脚本，实现功能如下

	- 提示用户输入一个目录路径
	- 显示目录下至少包含一个大写字母的文件名

.. code-block:: sh

	#！/bin/bash

	while true; do
		read -p "Enter a directory: " dirname
		[ "$dirname" == "quit" ] && exit 3
		[ -d "$dirname" ] && break || echo "wrong directory..."
	done

	for filename in $dirname/*;do
		if [[ "$fileName" =~ .*[[:upper:]]{1,}.* ]]; then
	    	echo "$fileName"
	    fi
	done

- 写一个脚本，实现功能如下(前提是配置好yum源)

	- 1、如果本机没有一个可用的yum源，则提示用户，并退出脚本(4)；如果此脚本非以root用户执行，则显示仅有root才有权限安装程序包，而后退出(3)
	- 2、提示用户输入一个程序包名称，而后使用yum自动安装之；尽可能不输出yum命令执行中的信息；如果安装成功，则绿色显示，否则，红色显示失败
	- 3、如果用户输入的程序包不存在，则显示错误后让用户继续输入
	- 4、如果用户输入quit，则正常退出(0)
	- 5、正常退出前，显示本地共安装的程序包的个数

.. code-block:: sh

	#!/bin/bash

	while true;do
		if [ $UID -ne 0 ]; then
			echo "`basename $0` must be running as root"
			exit 3
		fi

		yum repolist &> /dev/null
		if  [[ $? -eq 0 ]];then
			while true; do
				read -p "Enter a pakage: " pacName
				if [[ "$pacName" == "quit" ]];then
					rpm -qa | wc -l
					exit 0
	     		fi

	   			yum list | grep "^$pacName.*" &> /dev/null
	     		if [[ $? -eq 0 ]];then
	      			yum install $pacName -y &> /dev/null
	        		if [[ $? -ne 0 ]];then
	         			echo "$pacName install fail"
	        		else
	        			echo "$pacName install success"
	        		fi
	    		else
	    			echo "$pacName is not exist"
	         		continue
	    		fi
	  		done
	  	else
	  		echo "yum repo is not ok!"
	  		exit 4
		fi
	done

- 写一个脚本，完成功能如下

	- 1.提示用户输入一个nice值
	- 2.显示指定nice指定进程名及pid
	- 3.提示用户选择要修改nice值的进程的pid和nice值
	- 4.执行修改
	- 5.别退出，继续修改

.. code-block:: sh

	#!/bin/bash
	
	if [[ $UID -eq 0 ]];then
	   echo "keyi suibian tiao nice !"
	else
	   echo "zhineng tiaoda nice !"
	fi

	while true;do
		read -p "Enter a nice : " nicename
		[ "$nicename" == "quit" ] && exit 3
		/bin/ps axo nice,user,command,pid| grep "^[[:space:]]${nicename}\>"
		read -p "Enter a nice : " niceid
		read -p "Ener a PID :　" pidid
		/usr/bin/renice $niceid $pidid
	done

- 写一个脚本，实现功能如下：能对/etc/进行打包备份，备份位置为/backup/etc-日期.后缀

	- 1.显示如下菜单给用户

		- xz) xz compress
		- gzip) gzip compress
		- bzip2) bzip2 compress
	- 2.根据用户指定的压缩工具使用tar打包压缩
	- 3.默认为xz，输入错误则需要用户重新输入

.. code-block:: sh

	#!/bin/bash

	# 方法一
	[ -d /backup ] || mkdir /backup
	cat << EOF
	xz) xz compress
	gzip) gzip compress
	bzip2) bzip2 compress
	EOF

	while true;do
		read -p "Enter a options :" tarname
		[[ "$tarname" == "quit" ]] && exit 5
		tarname=${tarname:-xz}               # tarname为空时给定默认值

		case $tarname in
			xz)
	  			tar Jcf /backup/etc-`date +%F-%H-%M-%S`.tar.xz /etc/*
	  			break
	  			;;
			gzip)
	  			tar zcf /backup/etc-`date +%F-%H-%M-%S`.tar.gz /etc/*
	  			break
	  			;;
			bzip2)
	  			tar jcf /backup/etc-`date +%F-%H-%M-%S`.tar.bz2 /etc/*
	  			break
	  			;;
			*)
	  			echo "you Enter is wrong option!"
		esac
	done


	# 方法二

	#!/bin/bash

	[ -d /backup ] || mkdir /backup

	cat << EOF
	plz choose a compress tool:

	xz) xz compress
	gzip) gzip compress
	bzip2) bzip2 compress
	EOF

	while true; do
		read -p "your optopn: " option
		option=${option:-xz}

		case $option in
		xz)
			compressTool="J"
			suffix='xz'
			break
			;;
		gzip)
			compressTool="z"
			suffix='gz'
			break
			;;
		bzip2)
			compressTool="j"
			suffix='bz2'
			break
			;;
		*)
			echo "wrong option"
			;;
		esac
	done

	tar ${compressTool}cf /backup/etc-`date +%F-%H-%M-%S`.tar.$suffix /etc/*
