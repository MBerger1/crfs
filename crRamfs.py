#!/usr/bin/env python
'''
author:		MBerger
Filename:	crRamfs.py

crfs assumes available storage on a given device ( /dev/sda:b:c )

'''

import os
import sys
import argparse
import operator
#from fstab import Fstab
import fstab
import sh
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mount", required=True, dest="mount", help="ramdisk mount point")
parser.add_argument("-s", "--size", required=True, dest="size", help="enter the ramdisk size")
parser.add_argument("-t", "--vfstype", required=False, dest="vfstype", help="enter the vfstype ( tmpfs assumed )")

args = parser.parse_args()

# setup vars from argparse
m = args.mount
s = args.size
t = args.vfstype if args.vfstype else 'tmpfs'

def doCrfs(mnt,size,vfstype):
    doMkMount(mnt)
    mountFs(mnt,size,vfstype)
    doFsTab(mnt,size,vfstype)

def doMkMount(dirname):
    try:
        os.makedirs(dirname, mode=0755)
    except OSError:
        if os.path.exists(dirname):
            pass
        raise ValueError(dirname, 'exists')

def mountFs(mnt,size,vfstype):
    # mountIt = sh.Command('/bin/mount')
    # mountIt('-t', vfstype, '-o', 'size='+size, vfstype, mnt)
    subprocess.Popen(['/bin/mount', '-t', vfstype, '-o', 'size='+size, vfstype, mnt])

def doFsTab(mnt,size,vfstype):
    # fstab = fstab.Fstab.open_file()
    # for entry in fstab.Line:
        # print entry
    today = time.strftime("%Y%m%d")
    # print today
    if os.path.exists('/etc/fstab'+today):
        pass
    else:
        # fstabBak = sh.Command('/bin/cp')
        # fstabBak('/etc/fstab', '/etc/fstab.'+today)
        subprocess.Popen(['/bin/cp', '/etc/fstab', '/etc/fstab.'+today])
    try:
        with open("/etc/fstab", "a") as f:
            str = 'tmpfs\t'+mnt+' tmpfs\tnodev,nosuid,noexec,nodiratime,size='+size+'\t0 0'
            f.write(str+"\n")
    except:
        raise ValueError('cant write fstab')

if __name__ == '__main__':
    # doCrfs(sys.argv[1])
    doCrfs(m,s,t)

