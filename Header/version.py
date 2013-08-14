#coding = utf-8
from hashlib import md5
import os
import shutil
import time
import subprocess

newestFolder = 'newest'
lastFolder = 'last'



def file_md5(filePath):
    m = md5()
    a_file = open(filePath, 'rb')    #需要使用二进制格式读取文件内容
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()    

def copyFile(src, dest):
    pathFolders = dest.split('/')
    #去掉根目录和文件名
    del pathFolders[0]
    del pathFolders[0]
    del pathFolders[len(pathFolders)-1]
    #文件路径
    p = './'+ logFolderName
    for folder in pathFolders:
        p += '/'+folder
        try:
            #print 'mkdir', p
            os.mkdir(p)
        except:
            #文件夹已经存在
            pass

    shutil.copyfile(src, dest)

def getSvnInfo(folder):
    cmd = 'svn info %s' % newestFolder+'/'+folder
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.wait()
    fileInfo = p.stdout.read()
    return fileInfo

def saveSVNInfo(folder):
    info = getSvnInfo('asset')+'------------------------------\n'
    info += getSvnInfo('config')+'------------------------------\n'
    info += getSvnInfo('swf')+'------------------------------\n'

    logFileName = '%s/svnlog.txt' % (folder)
    open(logFileName, 'w').write(info)



if __name__ == '__main__':
    #变动文件
    changefiles = []

    for root, dirs, files in os.walk('./newest'):
        if root.find('.svn') != -1:
            #. 隐藏文件夹
            continue 

        #比较文件md5
        for name in files:
            newFilePath =  root + '/' + name
            newFilePath = newFilePath.replace('\\', '/')
            cmpPath = newFilePath.replace(newestFolder, lastFolder)
            if not os.path.isfile(cmpPath):
                changefiles.append(newFilePath)
            elif not file_md5(newFilePath) == file_md5(cmpPath):
                changefiles.append(newFilePath)
    
    if 0 == len(changefiles):
        print u'没有文件改变'
        exit(0)
    
    print u'变动文件:'
    print changefiles
    #复制到目录
    logFolderName = time.strftime('%Y-%m-%d_%H-%M-%S')
    os.mkdir(logFolderName)
    for f in changefiles:
        copyFile(f, f.replace(newestFolder, logFolderName))
        copyFile(f, f.replace(newestFolder, lastFolder))
    
    #svn log
    saveSVNInfo(logFolderName)

    
    