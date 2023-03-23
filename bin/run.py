#!/use/bin/env python
#coding:utf-8

#Author:6449694@qq.com

import  unittest
import  os,sys
import  time as t
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from utils.HTMLTestRunnerCN import HTMLTestRunner

class Runner:

	def __init__(self):
		pass

	def getSuite(self):
		'''获取要执行的测试套件'''
		suite = unittest.TestLoader().discover(
			start_dir=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests'),
			pattern='test_*.py',
			top_level_dir=None)
		print("suite",suite)
		return suite

	def main_runTextTest(self):
		'''批量执行测试用例'''
		unittest.TextTestRunner().run(self.getSuite())
		content='通过数：{0} 失败数：{1} 通过率：{2}'.format(
			self.excel.run_success_result(),
			self.excel.run_fail_result(),self.excel.run_pass_rate())
		print('Please wait while the statistics test results are sent in the mail')
		self.mail.send_mail('wanghailin@baice100.com','预付款接口测试报告',content)

	def main_runHTMLTest(self):
		'''HTMLTestRunner的方式'''
		testrun = unittest.TestSuite()
		testrun.addTest( self.getSuite() )
		# now = t.strftime("%Y-%m-%d-%H_%M_%S", t.localtime(t.time()))
		# tmp= now+'_apitest.html'
		tmp = "index.html"
		filename = os.path.join(
			os.path.dirname( os.path.dirname( __file__ ) ), "report", tmp )
		# filename =os.path.join("/export/server/jenkins_home/workspace/InformationFlowMonitoring/","report",tmp)
		print( "filename", filename )
		fp = open( filename, 'wb' )
		runner = HTMLTestRunner(
			# 报告写入的文件
			stream=fp,
			# 报告标题
			title=u'业务流接口测试报告',
			# 报告的说明与描述
			description=u'用例执行情况' )
		runner.run( testrun )



if __name__ == '__main__':
	# curPath = os.path.abspath( os.path.dirname( __file__ ) )
	# print( "curPath", curPath )
	# rootPath = os.path.split( curPath )[0]
	# print( "rootPath", rootPath )
	# sys.path.append(rootPath )
	# print( sys.path )
	# print("rr",rootPath )
	print("running")
	Runner().main_runHTMLTest()
	print("stoping")
