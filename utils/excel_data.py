#!/use/bin/env python
#coding:utf-8 

#Author:6449694@qq.com
from utils.public import data_dir

class ExcelVariable:
	caseID=0
	url=2
	request_data=3
	expect=4
	result=5

def getCaseID():
	return ExcelVariable.caseID

def getUrl():
	return ExcelVariable.url

def get_request_data():
	return ExcelVariable.request_data

def getExpect():
	return ExcelVariable.expect

def getResult():
	return ExcelVariable.result

def getHeadersValue():
	'''获取请求头'''
	headers={
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
		'Cookie':'user_trace_token=20190120115322-ee9b4525-1c66-11e9-b6aa-5254005c3644; LGUID=20190120115322-ee9b48e7-1c66-11e9-b6aa-5254005c3644; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=ABAAABAAAFCAAEGC8C505815945137FB33FB872BA3047CA; WEBTJ-ID=2019-1-20145436-1686a0a2487280-000970e81522ab-10724c6f-1440000-1686a0a248852; PRE_UTM=m_cf_cpt_sogou_pc; PRE_HOST=www.sogou.com; PRE_SITE=https%3A%2F%2Fwww.sogou.com%2Fsogou%3Fprs%3D5%26rfg%3D1%26query%3Dwww.lagou.com%26pid%3DAQktG%26ie%3Dutf8; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpt_sogou_pc; TG-TRACK-CODE=index_search; SEARCH_ID=9c6702d375404e2bb73d42c774b63c28; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547967287; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1547967898; _gid=GA1.2.477000737.1547956403; _gat=1; _ga=GA1.2.1019422267.1547956403; LGSID=20190120145436-400d0fd5-1c80-11e9-b6ae-5254005c3644; LGRID=20190120150458-b2b50d9d-1c81-11e9-b6ae-5254005c3644',
		'Referer':'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='}
	return headers

