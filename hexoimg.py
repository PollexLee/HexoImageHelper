#! /usr/local/bin/python
#coding=utf-8

import os
import sys
import time
import shlex
import datetime
import subprocess
import shutil

'''
open GitHub client:
open /Applications/GitHub\ Desktop.app/
'''

def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=shell, bufsize=4096)

    while sub.poll() is None:
        log = sub.stdout.readline()
        if log != "" and log != "/n" and ("INFO" in log or "On" in log):
            print log,

        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)
    return str(sub.returncode)

# save to clipboard
def addToClipBoard(text):
    # 'Hello World!' | pbcopy
    command = 'echo ' + "'" + text.strip() + "'" + '| pbcopy'
    os.system(command)


# get image url
def getImageUrl(name):
    return "![%s](%s)\n" % (name, "https://raw.githubusercontent.com/"
                                  "xiaohongmaosimida/xiaohongmaosimida.github.io/master/img/" +
                            name)

arg = sys.argv[1]
truePath = arg
print truePath
trueName = truePath[truePath.rfind("/")+1:]
copyPath = "/Users/lipeng/hexo/themes/yelee/source/img/"
shutil.copy(arg, copyPath + trueName)
print execute_command("open /Applications/GitHub\ Desktop.app/")
time.sleep(3)
print execute_command("hexo g", "/Users/lipeng/hexo")
print execute_command("hexo d", "/Users/lipeng/hexo")
url_before_save = getImageUrl(trueName)
print url_before_save
addToClipBoard(url_before_save)
