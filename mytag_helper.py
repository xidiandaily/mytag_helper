#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import logging
import re
import argparse
import pdb
import tempfile
import shutil


_VER="1.0.1"
logfilename=os.path.splitext(sys.argv[0])[0]+".log"

parser=argparse.ArgumentParser()
parser.add_argument('-l',dest="enable_debug_log",action='store_true',help='enable debug log')
parser.add_argument('-f',dest="enable_log_file",action='store_true',help='if this argument has been set,output log to logfile:{}'.format(logfilename))
parser.add_argument('-t',dest="tagfilename",action='store',help='input and ouput tag filename')
parser.add_argument('-r',dest="run",action='store_true',help='replace')
parser.add_argument('-c',dest="check",action='store_true',help='just check')
parser.add_argument('--version',action='version',version=_VER)
args=parser.parse_args()


logger = logging.getLogger()
#simpleformatter = logging.Formatter('%(message)s')
detailformatter = logging.Formatter('%(asctime)s - %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)
# create console handler with stdout output
stdout = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(stdout)

#log file
if args.enable_log_file or args.enable_debug_log:
    logfile=logging.FileHandler(logfilename)
    logfile.setFormatter(detailformatter)
    logger.addHandler(logfile)

if args.enable_debug_log:
    logger.setLevel(logging.DEBUG)
    stdout.setFormatter(detailformatter)
    logger.debug("if enable_debug_log, you will see this log")

if args.run:
    temptagdir=tempfile.TemporaryDirectory(prefix='mytag_helper')
    temptagfile = os.path.join(temptagdir.name,"mytag.out")
    with open(temptagfile,'w',encoding="utf-8",newline='') as fw:
        with open(args.tagfilename,'rb') as fr:
            while True:
                my_input=fr.readline()
                if not my_input:
                    break
                
                is_trans = False
                is_need_re=False
                while not is_trans:
                    try:
                        str_utf8=my_input.decode('utf-8')
                        is_trans=True
                    except UnicodeDecodeError as e:
                        is_need_re=True
                        my_input=e.object.replace(e.object[e.start:e.end],b'.*')

                if is_need_re:
                    str_utf8=re.sub('(\.\*)+','.*',str_utf8)
                fw.writelines(str_utf8)
    logger.info('done')
    os.remove(args.tagfilename)
    shutil.copy(temptagfile,args.tagfilename)

elif args.check:
    with open(args.tagfilename,'rb') as fr:
        while True:
            my_input=fr.readline()
            if not my_input:
                break

            try:
                str_utf8=my_input.decode('utf-8')
            except UnicodeDecodeError as e:
                logger.error('tag:{} contain Illegal character, head:{}'.format(args.tagfilename,e.object[0:e.start].decode('utf-8')))
    logger.info('done')
else:
    parser.print_help()

