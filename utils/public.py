# -*- coding: utf-8 -*-
# @Time    : 2019/9/3 15:55
# @Author  : alvin
# @File    : public.py
# @Software: PyCharm

import os

def data_dir(data='data', fileName=None):
    '''查找文件的路径'''
    if fileName :
        return os.path.join( os.path.dirname( os.path.dirname( __file__ ) ), data,fileName )
    else:
        return os.path.join( os.path.dirname( os.path.dirname( __file__ ) ), data)

def data_dir_file(data='data',dirPath=None,fileName=None):
    '''查找上传文件的文件的路径'''
    # print("data_dir_file fileName ",os.path.join( os.path.dirname( os.path.dirname( __file__ ) ),data,'upload_files'))
    # print("fileName",fileName)
    if fileName and dirPath :
        # print(os.path.join( os.path.dirname( os.path.dirname( __file__ ) ), data,
        #                     dirPath, fileName ))
        return os.path.join( os.path.dirname( os.path.dirname( __file__ ) ), data,
                             dirPath, fileName )
    else:
        return os.path.join( os.path.dirname( os.path.dirname( __file__ ) ),data)

def get_extend_chromedriver_file(dirPath='extend',fileName='chromedriver.exe'):
    '''chromedriver文件的路径'''
    if fileName and dirPath :
        # print(os.path.join( os.path.dirname( os.path.dirname( __file__ ) ),
        #                     dirPath, fileName ))
        return os.path.join( os.path.dirname( os.path.dirname( __file__ ) ),
                             dirPath, fileName )
    else:
        return os.path.join( os.path.dirname( os.path.dirname( __file__ ) ))

def dict_get(dict, objkey, default):
    # 获取字典中的objkey对应的值，适用于字典嵌套
    # dict:字典
    # objkey:目标key
    # default:找不到时返回的默认值
    tmp = dict
    for k, v in tmp.items():
        if k == objkey:
            return v
        else:
            if (type( v ).__name__ == 'dict'):

                ret = dict_get( v, objkey, default )
                if ret is not default:
                    return ret
    return default

if __name__ == "__main__":
    # data_dir_file(fileName="export_cpa_demo.xlsx")
    a = data_dir_file(fileName="export_cpa_demo.xlsx")
    print(a)