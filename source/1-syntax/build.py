#-*- coding:utf-8 -*-
#author:anony

import os
import sys

# 当前python文件所在的目录
py_dir = os.path.dirname(os.path.abspath(__file__))

# 平台标志位：0代表Window平台，1代表类Unix平台
arch_flag = 0

# index文件名
index = "index.rst"

# 目录结构
dir_tree = {
	"1-scriptstruct": "脚本结构",
	"2-datatype": "数据类型",
	"3-variable": "变量",
	"4-operator": "运算符",
	"5-control": "控制流程语句",
	"6-functions": "函数",
	"7-pieceofkn": "知识碎片",
}


# rst文件的目录树
info = '''


目录
------

.. toctree::
   :titlesonly:
   :glob:


'''

# rst文件中一级标题
title_sign = "=================\n"


def write_data(file_name, data):
	"""
	向指定文件写入数据
	:param file_name:
	:param data:
	:return:
	"""
	ret = True
	try:
		with open(file_name, "a", encoding="utf-8") as f:
			f.write(data)
	except Exception as e:
		print(e)
		ret = False
	finally:
		return ret


def dir_create(dir_name):
	"""
	创建目录
	:param dir_name:
	:return:
	"""
	ret = True
	try:
		os.mkdir(dir_name)
	except FileExistsError as e:
		print("The file exist")
		ret = False
	except Exception as e:
		print(e)
		ret = False
	finally:
		return ret


def dir_change(dir_name):
	"""
	切换工作目录
	:param dir_name:
	:return:
	"""
	ret = True
	try:
		os.chdir(dir_name)
	except Exception as e:
		print(e)
		ret = False
	finally:
		return ret


def dir_init(dir_tree):
	write_data(index, info)
	for key in dir_tree:
		tmp_dir = os.path.abspath(__file__)
		if (tmp_dir != py_dir) and dir_change(py_dir):
			data = "   " + key + "/index" + '\n'
			write_data(index, data)
			if not dir_create(key):
				print(key, "创建失败")
				return False
			if dir_change(key):
				data = dir_tree[key] + '\n'
				if not (write_data(index, data) and write_data(index, title_sign)):
					print(key, "/index 写入失败")
					return False
			else:
				print(key, "切换失败")
				return False
		else:
			print(py_dir, "切换失败")
			return False
	return True


if __name__ == '__main__':
	if not dir_init(dir_tree):
		print("\033[31;1mbulid fail\033[0m")

