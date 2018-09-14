#!/usr/bin/env python
#coding:utf-8
import os
import json
import hashlib
import subprocess


assetsDir = {
    "searchDir" : ["src", "res"],
    "ignorDir" : ["cocos", "obj","version"]
}

versionConfigFile = "bin\\config\\version_info.json"  #°æ±¾ÐÅÏ¢µÄÅäÖÃÎÄ¼þÂ·¾¶

versionManifestPath = "bin/version/version.manifest"    #ÓÉ´Ë½Å±¾Éú³ÉµÄversion.manifestÎÄ¼þÂ·¾¶

projectManifestPath = "bin/version/project.manifest"    #ÓÉ´Ë½Å±¾Éú³ÉµÄproject.manifestÎÄ¼þÂ·¾¶


class SearchFile:
    def __init__(self):
        self.fileList = []
        grader_father = getGraderFatherPath()
        for k in assetsDir:
            if (k == "searchDir"):
                for searchdire in assetsDir[k]:                 
                    tmp = os.path.join(grader_father, searchdire)
                    self.recursiveDir(tmp)

    def recursiveDir(self, srcPath):
        ''' µÝ¹éÖ¸¶¨Ä¿Â¼ÏÂµÄËùÓÐÎÄ¼þ'''
        dirList = []    #ËùÓÐÎÄ¼þ¼Ð  

        files = os.listdir(srcPath) #·µ»ØÖ¸¶¨Ä¿Â¼ÏÂµÄËùÓÐÎÄ¼þ£¬¼°Ä¿Â¼£¨²»º¬×ÓÄ¿Â¼£©

        for f in files:         
            #Ä¿Â¼µÄ´¦Àí
            if (os.path.isdir(srcPath + '/' + f)):              
                if (f[0] == '.' or (f in assetsDir["ignorDir"])):
                    #ÅÅ³ýÒþ²ØÎÄ¼þ¼ÐºÍºöÂÔµÄÄ¿Â¼
                    pass
                else:
                    #Ìí¼Ó·ÇÐèÒªµÄÎÄ¼þ¼Ð                                  
                    dirList.append(f)

            #ÎÄ¼þµÄ´¦Àí
            elif (os.path.isfile(srcPath + '/' + f)):               
                self.fileList.append(srcPath + '/' + f) #Ìí¼ÓÎÄ¼þ

        #±éÀúËùÓÐ×ÓÄ¿Â¼,²¢µÝ¹é
        for dire in dirList:        
            #µÝ¹éÄ¿Â¼ÏÂµÄÎÄ¼þ
            self.recursiveDir(srcPath + '/' + dire)

    def getAllFile(self):
        ''' get all file path'''
        return tuple(self.fileList)

def GetSvnCurrentVersion(path): 

    popen = subprocess.Popen(['svn', 'info'], stdout = subprocess.PIPE, cwd = path)    
    while True:
        next_line = popen.stdout.readline()         
        if next_line == '' and popen.poll() != None:
            break

        valList = next_line.split(':')      
        if len(valList)<2:
            continue
        valList[0] = valList[0].strip().lstrip().rstrip(' ')
        valList[1] = valList[1].strip().lstrip().rstrip(' ')

        if(valList[0]=="Revision"):
            return ("%06.0f" %(float(valList[1])))
    return ""


def CalcMD5(filepath):
    """generate a md5 code by a file path"""
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        return md5obj.hexdigest()


def getVersionInfo(path):
    print("pathpathpathpath = %s" %path)
    '''get version config data'''
 
    filename = os.path.join(path, versionConfigFile)
    print("filename = %s" %filename)

    configFile = open(filename,"r")
    json_data = json.load(configFile)
    configFile.close()
    json_data["version"] = json_data["version"] + '.' + str(GetSvnCurrentVersion(getGraderFatherPath()))
    return json_data

def getGraderFatherPath():
    pwd = os.getcwd()

    print os.getcwd() #获取当前工作目录路径
    print os.path.abspath('.') #获取当前工作目录路径
    print os.path.abspath('test.txt') #获取当前目录文件下的工作目录路径
    print os.path.abspath('..') #获取当前工作的父目录 ！注意是父目录路径
    print os.path.abspath(os.curdir) #获取当前工作目录路径
    #当前文件的父路径
    father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
    #当前文件的前两级目录
    grader_father=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
    return grader_father

def GenerateversionManifestPath():
    ''' Éú³É´ó°æ±¾µÄversion.manifest'''
    pwd = os.getcwd()
    grader_father=getGraderFatherPath()
    print("grader_father == %s" %grader_father)
    json_str = json.dumps(getVersionInfo(grader_father), indent = 2)
    filename = os.path.join(grader_father, versionManifestPath)
    fo = open(filename,"w")  
    fo.write(json_str)  
    fo.close()


def GenerateprojectManifestPath():
    pwd = os.getcwd()
    grader_father=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
    searchfile = SearchFile()
    fileList = list(searchfile.getAllFile())
    project_str = {}
    project_str.update(getVersionInfo(grader_father))
    dataDic = {}
    for f in fileList:      
        dataDic[f] = {"md5" : CalcMD5(f), "size" : os.path.getsize(f)}

    project_str.update({"assets":dataDic})
    json_str = json.dumps(project_str, sort_keys = True, indent = 2)

    filename = os.path.join(grader_father, projectManifestPath)
    fo = open(filename,"w")  
    fo.write(json_str)  
    fo.close()


if __name__ == "__main__":
    GenerateversionManifestPath()
    GenerateprojectManifestPath()