shell编程
==========

参考文档

- \ `Shell脚本 <http://www.cnblogs.com/f-ck-need-u/p/7048359.html>`_\ 
- \ ``man bash文档``\ 

\ ``shell``\ 可以理解为一种脚本语言，像\ ``javascript``\ 等其它脚本语言一样，只需要一个能编写代码的文本编辑器和一个能解释执行的脚本解释器就可以

\ ``shell脚本``\ 的本质是：以某种语法格式将shell命令组织起来的由shell程序解析执行的脚本文本文件

由本质可知，要想掌握\ ``shell脚本``\ ，就需要了解并掌握下列三部分内容 

- \ **shell命令**\ ：即\ ``ls/cd``\ 等linux命令，详细可参考\ `shell命令 <http://codetoolchains.readthedocs.io/en/latest/4-Linux/2-shellcmd/index.html>`_\ 
- \ **shell解释器**\ ：即\ ``sh/bash/csh``\ 等shell应用程序，详细可参考\ `shell应用程序 <http://codetoolchains.readthedocs.io/en/latest/4-Linux/1-shellenv/1-shellsoft/index.html>`_\ 
- \ **shell语法**\ ：即\ ``数据类型/变量/控制流语句/函数``\ 等编程语法

关于\ ``shell命令``\ 和\ ``shell解释器``\ 可参考上述指定的文档，本系列主要是对\ ``shell语法``\ 进行相关讲解，将从以下方面展开介绍：


.. toctree::
   :titlesonly:
   :glob:


   1-syntax/index
   2-library/index
   3-sample/index
