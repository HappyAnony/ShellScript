实用脚本
=========

shell脚本常用来启动相关系统服务

- \ `memcached服务启动脚本 <#memcachedl>`_\ 


.. _memcachedl:

0x00 memcached服务启动脚本
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

以下是\ ``memcached``\ 服务启动脚本的示例，是一个非常简单但却非常通用的\ ``SysV``\ 服务启动脚本

- 关于\ ``SysV``\ 服务启动脚本的详解请参考：\ `如何写SysV服务管理脚本 <http://www.cnblogs.com/f-ck-need-u/p/7524401.html>`_\ 

.. code-block:: sh

	#!/bin/bash
	#
	# chkconfig: - 86 14
	# description: Distributed memory caching daemon

	## Default variables
	PORT="11211"
	USER="nobody"
	MAXCONN="1024"
	CACHESIZE="64"
	OPTIONS=""

	RETVAL=0
	prog="/usr/local/memcached/bin/memcached"
	desc="Distributed memory caching"
	lockfile="/var/lock/subsys/memcached"

	. /etc/rc.d/init.d/functions
	[ -f /etc/sysconfig/memcached ] && source /etc/sysconfig/memcached

	start() {
	        echo -n $"Starting $desc (memcached): "
	        daemon $prog -d -p $PORT -u $USER -c $MAXCONN -m $CACHESIZE "$OPTIONS"
	        RETVAL=$?
	        echo
	        [ $RETVAL -eq 0 ] && touch $lockfile
	        return $RETVAL
	}

	stop() {
	        echo -n $"Shutting down $desc (memcached): "
	        killproc $prog
	        RETVAL=$?
	        echo
	        [ $RETVAL -eq 0 ] && rm -f $lockfile
	        return $RETVAL
	}

	restart() {
	        stop
	        start
	}

	reload() {
	        echo -n $"Reloading $desc ($prog): "
	        killproc $prog -HUP
	        RETVAL=$?
	        echo
	        return $RETVAL
	}

	case "$1" in
	  start)
	        start
	        ;;
	  stop)
	        stop
	        ;;
	  restart)
	        restart
	        ;;
	  condrestart)
	        [ -e $lockfile ] && restart
	        RETVAL=$?
	        ;;       
	  reload)
	        reload
	        ;;
	  status)
	        status $prog
	        RETVAL=$?
	        ;;
	   *)
	        echo $"Usage: $0 {start|stop|restart|reload|condrestart|status}"
	        RETVAL=1
	esac

	exit $RETVAL


