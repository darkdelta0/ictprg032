#!/usr/bin/python3

import sys
import os
import pathlib
import shutil
import smtplib
from datetime import datetime
from backupcfg import jobs, dstPath, logPath, smtp

#Author: Max Cosby
#Version:1,2
#program name
#description
#copyright

def sendEmail(errorMessage, dateTimeStamp):
  email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Log\n\n' + errorMessage + '\n'

    # connect to email server and send email
  try:
      smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
      smtp_server.ehlo()
      smtp_server.starttls()
      smtp_server.ehlo()
      smtp_server.login(smtp["user"], smtp["password"])
      smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
      smtp_server.close()
  except Exception as e:
      print("ERROR: An error occurred.")
  pass

def Errorlogging(errorMessage, dateTimeStamp):
  #this code is used to log
    try:
        file = open(logPath, "a") #this is used for to find the document and to be able to use it
        file.write(f"{errorMessage} {dateTimeStamp}\n") #this code is writing in the document
        file.close() #this closes the document
        
        print("error has been found, proceeding to log")
        #this code is telling us that the main code has not worked and has occured a error and is now being logged 
        
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")

def error(errorMessage, dateTimeStamp):
  print(errorMessage)#print error message on screen 
  
  Errorlogging(f"FAILURE {errorMessage}", dateTimeStamp)
  sendEmail(f"FAILURE {errorMessage}", dateTimeStamp)
  #write failure to log file
  
  #email error message to administrator


def Succesfullogging(errorMessage, dateTimeStamp):
    try:
        file = open(logPath, "a")
        file.write(f"{errorMessage} {dateTimeStamp}\n")
        file.close()
        
        print("Succes: proceeding to log")
        
    except FileNotFoundError:
        print("ERROR: File does not exist.")
    except IOError:
        print("ERROR: File is not accessible.")

def success(Message, dateTimeStamp):
  print(Message)#print error message on screen 
  
  Succesfullogging(f"Success {Message}", dateTimeStamp)
  sendEmail(f"Success {Message}", dateTimeStamp)
  


def main(): 
    #code for the time stamp for backups
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    argCount = len(sys.argv)
    #code to find 
    if argCount != 2:
        error("ERROR: jobname missing from command line. ", dateTimeStamp) 
    else: #checks to see if the input in the console alighns with the jobs in backupcfg.py
        jobName = sys.argv[1]
        if jobName not in jobs:
            error(f"ERROR: jobname {jobName} not defined. ", dateTimeStamp) 
        else:
            srcPath=jobs[jobName]
            if not os.path.exists(srcPath):
                error(f"ERROR: Source path {srcPath} does not exist", dateTimeStamp)
            else:
                if not os.path.exists(dstPath): #sees if the path is actually a thing
                  error(f"ERROR: Destination path {dstPath} does not exist", dateTimeStamp)
                else:
                    srcDetails = pathlib.PurePath(srcPath)
                    dstLoc = dstPath + "/" + srcDetails.name + "-" + dateTimeStamp
                    
                    if pathlib.Path(srcPath).is_dir():
                      shutil.copytree(srcPath, dstLoc)
                      
                    else:
                      shutil.copy2(srcPath, dstLoc)
                      success("backup created ", dateTimeStamp)
                    #* * * * * /home/ec2-user/environment/ictprg032/backup.py job17
 
if __name__ == '__main__':
    main()