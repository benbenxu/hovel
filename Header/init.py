#coding = utf-8

import os
import shutil

newestFolderName = 'newest'
lastFolderName = 'last'

#svn 地址
svnswf = 'http://192.168.0.110/svn/client/SLAM_DUNK/src/swf'
svnasset = 'http://192.168.0.110/svn/client/SLAM_DUNK/src/asset'
svnconfig = 'http://192.168.0.110/svn/client/SLAM_DUNK/src/config'


def mkdir(dirName):
    try:
        os.mkdir(dirName)
        print u'创建文件夹 %s' % dirName
        return True
    except WindowsError:
        #文件已经存在
        return False


if __name__ == '__main__':
    if mkdir(newestFolderName):
        os.system('TortoiseProc /command:checkout /path:"%s" /url:"%s" ' % (newestFolderName+'/swf', svnswf)) 
        os.system('TortoiseProc /command:checkout /path:"%s" /url:"%s" ' % (newestFolderName+'/asset', svnasset)) 
        os.system('TortoiseProc /command:checkout /path:"%s" /url:"%s" ' % (newestFolderName+'/config', svnconfig)) 
        
        print u'正在复制文件, 请耐心等待...'
        shutil.copytree(newestFolderName, lastFolderName, True)
        shutil.rmtree(lastFolderName+'/swf'+'/.svn', 'True')
        shutil.rmtree(lastFolderName+'/asset'+'/.svn', 'True')    
        shutil.rmtree(lastFolderName+'/config'+'/.svn', 'True')
        print u'创建文件夹 %s' % lastFolderName