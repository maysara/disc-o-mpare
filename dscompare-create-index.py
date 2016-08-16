#!/usr/bin/python
'''
PLATFORM=$(uname)
if [[ $PLATFORM == "Linux" ]]
then
        MD5CMD='md5sum'
else
        MD5CMD='md5'
fi

find $1 | while read line
do
        if [[ -f "$line" ]]
        then
                fileMd5=$($MD5CMD $line|cut -f 1 -d' ')
        else
                fileMd5=00000000000000000000000000000000
        fi
        stat -c $fileMd5,%F,%i,%n $line

done
#; xargs -0 -l md5sum



S_IFMT     0170000   bit mask for the file type bit field

   S_IFSOCK   0140000   socket
   S_IFLNK    0120000   symbolic link
   S_IFREG    0100000   regular file
   S_IFBLK    0060000   block device
   S_IFDIR    0040000   directory
   S_IFCHR    0020000   character device
   S_IFIFO    0010000   FIFO
'''

import sys
import os
import csv
import hashlib
import json
import stat
import argparse

parser = argparse.ArgumentParser(description='This is a script that generates a file structure based on a csv file, with pre defined fields.')
parser.add_argument('PATH', default=sys.stdin, help='Path to be indexed')
#parser.add_argument('--dry-run','-n',help='Dry run',action='store_true')
#parser.add_argument('--verbose','-v',help='be verbose about what you do',action='store_true')
parser.add_argument('--output','-o',default="-",help='optional file path and name to write output')
args = parser.parse_args()

if args.output == "-":
    outputfile=csv.writer(sys.stdout, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
else:
    try:
        outputobject = open(args.output,'w')
        outputfile=csv.writer(outputobject, delimiter=',', quotechar='"',quoting=csv.QUOTE_ALL)
    except OSError:
        print('attempting to open file '+args.output+' for writing caused an error, make sure that the file location exists and is writable.')
for root,dirs, files in os.walk(args.PATH):
    for filename in files:
        #print os.path.join(root,filename)
        #print hashlib.md5(open(os.path.join(root,filename),'rb').read()).hexdigest()
        #print os.stat(os.path.join(root,filename)).st_ino
        #print oct(stat.S_IFMT(os.stat(os.path.join(root,filename)).st_mode))
        m = hashlib.md5()
        blocksize=8192
        #handle softlinks
        if not os.path.islink(filename):
            with open(os.path.join(root,filename),'rb') as f:
                while True:
                    buf = f.read(blocksize)
                    if not buf:
                        md5hash = m.hexdigest()
                        break
                    m.update(buf)
                #hashlib.md5(open(os.path.join(root,filename),'rb').read()).hexdigest(),
        else:
            md5hash="0"*32,
        outputfile.writerow([
        #print json.dumps( [
            md5hash,
            oct(os.lstat(os.path.join(root,filename)).st_mode),
            os.lstat(os.path.join(root,filename)).st_ino,
            os.path.join(root,filename)
        ])
    for dirname in dirs:
        outputfile.writerow([
        #print json.dumps( [
            "0"*32,
            oct(os.lstat(os.path.join(root,dirname)).st_mode),
            os.lstat(os.path.join(root,dirname)).st_ino,
            os.path.join(root,dirname)
        ])


