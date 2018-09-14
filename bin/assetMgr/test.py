import os
pwd = os.getcwd()
grader_father=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
print("grader_father = %s" %grader_father)

fullpath = os.path.join(pwd, "hh.txt")
print("fullpath = %s" %fullpath)
pwd = os.getcwd()
print(pwd)