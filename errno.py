#!/usr/bin/python

import os
import sys

if __name__ == '__main__':
	if (len(sys.argv) <= 1):
		print('"python errno.py 11 返回errno为11的字符串说明"')
		exit(0)
	
	errno = int(int(sys.argv[1]))
	print('errno %d:'%errno, end=' ')
	print(os.strerror(errno))
