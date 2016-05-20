'''
Created on 2015-05-29
@author: solomonlu(mengyi.lu)
'''
import os
import hashlib
import json
import argparse
import re

def calcMD5(fileName):
    m = hashlib.md5()
    n = 1024*4
    file = open(fileName,"rb")
    while True:  
        buf = file.read(n)  
        if buf:  
            m.update(buf)  
        else:  
            break  
    file.close()
    md5value = m.hexdigest()
    return md5value

class ResourceScanner:
    def __init__(self,directory,output,debug):
        self.output = output
        self.debug = debug
        self.fileList = {}
        if directory[-1] == '\\' or directory[-1] == '/':
            directory = directory[:-1]
        self.realDirectory = os.path.split(directory)[1]

        def findFile(arg,dirname,files):
            for file in files:
                file_path=os.path.join(dirname,file)
                if ".svn" in file_path:
                    continue
                if os.path.isfile(file_path):
                    md5 = calcMD5(file_path)
                    size=os.path.getsize(file_path)
                    file_path = file_path.replace(directory,self.realDirectory)
                    file_path = file_path.replace("\\", "/")
                    self.fileList[file_path] = (md5,size)
                    self.printf("find file:%s,md5:%s,size:%d" %(file_path,md5,size))
        os.path.walk(directory,findFile,())

    def printf(self,*msg):
        if self.debug == True:
            for m in msg:
                print m

    def doGenerate(self):
        self.doConfigGenerate()

    def doConfigGenerate(self):
        jsonString = json.dumps(self.fileList, sort_keys=True, indent=2)
        file = open(os.path.join(self.output,"resource.md5.txt"),"w")
        file.write(jsonString)
        file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='analyze resource directory then generate md5 file')
    parser.add_argument("-o","--output", dest="output", default=".", help="set file output path")
    parser.add_argument("-d","--debug", action="store_true", dest="debug", default=False, help="print debug info")
    parser.add_argument("directory",help="resource directory")
    args = parser.parse_args()
    
    if not os.path.exists(args.directory):
        print args.directory+" not exists!"
    elif not os.path.isdir(args.directory):
        print args.directory+" is not directory!"
    else:
        ResourceScanner(args.directory,args.output,args.debug).doGenerate()





