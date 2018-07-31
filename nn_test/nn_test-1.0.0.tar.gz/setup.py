from distutils.core import setup

setup(
	  name="nn_test", #模块的名称
	  version="1.0.0",#版本号，每次修改代码的时候，可以改一下
	  description="牛牛使用发布测试的模块",#描述
	  author="牛牛",#作者
	  author_email="niuhanyang@163.com",#联系邮箱
	  url="http://www.nnzhp.cn",#你的主页
	  py_modules=['nn_test.my_test','nn_test.my_python']#这个是下面有哪些模块可以用
	  )

