import os
import sys
import subprocess
import shutil

version='unknow'
fname='version'
if os.path.exists(fname):
    with open(fname,'r') as fileObj:
        version=fileObj.read().strip()

if os.path.exists('./config.ini') and os.path.exists('dist'):
    if sys.platform=='linux' and os.path.exists('config.ini.linux'):
        shutil.copy('config.ini.linux','./dist/config.ini.v{}'.format(version))
    else:
        shutil.copy('config.ini','./dist/config.ini.v{}'.format(version))

if os.path.exists('dist'):
    for root,paths,files in os.walk('./dist'):
        for filename in files:
            if filename.find(version)==-1:
                shutil.move(os.path.join(root,filename),os.path.join(root,'{}.v{}{}'.format(os.path.splitext(filename)[0],version,os.path.splitext(filename)[1])))
    os.rename('dist','release.v{}'.format(version))
    subprocess.check_call(['d:\\zip\\zip.exe','-r','release.v{}.zip'.format(version),"release.v{}".format(version)])

