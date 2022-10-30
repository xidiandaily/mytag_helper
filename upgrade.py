import os
import sys
import subprocess
import shutil
import pdb

def run_cmds(cmds,cwd=os.getcwd(),ignored=False):
    try:
        output=subprocess.check_call(cmds,cwd=cwd,env=os.environ)
    except subprocess.CalledProcessError as e:
        if ignored:
            pass
        raise

def upgrade_file(strName):
    global version
    global newversion

    strCon=''
    with open(strName,'r',encoding='utf-8') as fileObj:
        strCon=fileObj.read()

    strNewCon=strCon.replace(version,newversion)
    if strNewCon != strCon:
        with open(strName,'w',encoding='utf-8',newline='') as fileObj:
            fileObj.write(strNewCon)
            print('upgrade file:{} done'.format(strName))

version='unknow'
fname='version'
if os.path.exists(fname):
    with open(fname,'r') as fileObj:
        version=fileObj.read().strip()

verlist=version.split('.')
verlist[2]='{}'.format(int(verlist[2])+1)
newversion='.'.join(verlist)
print('upgrade from "{}"=>"{}"'.format(version,newversion))

upgrade_file('./version')
for root,paths,files in os.walk('.'):
    for filename in files:
        if os.path.splitext(filename)[1]=='.py':
            upgrade_file(os.path.join(root,filename))

