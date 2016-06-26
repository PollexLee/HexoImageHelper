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
打开github客户端的命令:
open /Applications/GitHub\ Desktop.app/
'''

def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
            封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
           参数:
        cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
        timeout: 超时时间，秒，支持小数，精度0.1秒
        shell: 是否通过shell运行
    Returns: return_code
    Raises:  Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # 没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
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