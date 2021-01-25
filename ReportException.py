import os, sys, time, datetime, subprocess, logging, traceback
from PyQt5.Qt import *

def uncaughtExceptionHandler(exctype, value, tb):
    logging.error("\n************!!!UNCAUGHT EXCEPTION!!!*********************\n" +
                  ("Type: %s" % exctype) + '\n' +
                  ("Value: %s" % value) + '\n' +
                  ("Traceback:" + '\n') +
                    " ".join(traceback.format_tb(tb)) +
                  "************************************************************\n")
    showFaultDialog(err_type=exctype, err_value=value, tb=tb)

def unraisableExceptionHandler(exc_type,exc_value,exc_traceback,err_msg,object):
    logging.error("\n************!!!UNHANDLEABLE EXCEPTION!!!******************\n" +
                  ("Type: %s" % exc_type) + '\n' +
                  ("Value: %s" % exc_value) + '\n' +
                  ("Message: %s " % err_msg) + '\n' +
                  ("Traceback:" + '\n') +
                    " ".join(traceback.format_tb(exc_traceback)) + '\n' +
                  ("On Object: %s" + object) + '\n' +
                  "************************************************************\n")
    showFaultDialog(err_type=exc_type, err_value=exc_value, tb=exc_traceback)

def thraedingExceptionHandler(exc_type,exc_value,exc_traceback,thread):
    logging.error("\n************!!!UNCAUGHT THREADING EXCEPTION!!!***********\n" +
                  ("Type: %s" % exc_type) + '\n' +
                  ("Value: %s" % exc_value) + '\n' +
                  ("Traceback on thread %s: " % thread + '\n') +
                    " ".join(traceback.format_tb(exc_traceback)) +
                  "************************************************************\n")
    showFaultDialog(err_type=exc_type, err_value=exc_value, tb=exc_traceback)

def getSystemInfo():
    systemInfoProcess = subprocess.Popen("C:\Windows\System32\systeminfo.exe", shell=True, stdout=subprocess.PIPE,universal_newlines=True)
    systemInfoProcessReturn = systemInfoProcess.stdout.read()
    gpuInfoProcess = subprocess.Popen("C:\Windows\System32\wbem\WMIC.exe PATH Win32_videocontroller GET Description /format:list",
                                      shell=True, stdout=subprocess.PIPE,universal_newlines=True)
    gpuInfoProcessReturn = gpuInfoProcess.stdout.read()
    return systemInfoProcessReturn, gpuInfoProcessReturn

def showFaultDialog(err_type, err_value, tb):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("不好，出现了一个问题: %s" % err_type)
    msg.setInformativeText("运行中出现了%s故障,请到logs文件夹中找到log-%s.txt并上报。" % (err_value, datetime.datetime.today().strftime('%Y-%m-%d')))
    msg.setWindowTitle("DD监控室出现了问题")
    msg.setDetailedText("Traceback:\n%s" % (" ".join(traceback.format_tb(tb))))
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()