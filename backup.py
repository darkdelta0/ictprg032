#!/usr/bin/python3

import sys
import os
import pathlib
import shutil
from datetime import datetime
from backupcfg import jobs, dstPath

def main():
    #code for the time stamp for backups
    dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    argCount = len(sys.argv)
    #code to find 
    if argCount != 2:
        print("ERROR: jobname missing from command line.")
    else:
        jobName = sys.argv[1]
        if jobName not in jobs:
            print(f"ERROR: jobname {jobName} not defined")
        else:
            srcPath=jobs[jobName]
            if not os.path.exists(srcPath):
                print(f"ERROR: Source path {srcPath} does not exist")
            else:
                if not os.path.exists(dstPath):
                    print(f"ERROR: Destination path {dstPath} does not exist")
                else:
                    srcDetails = pathlib.PurePath(srcPath)
                    
                    dstLoc = dstPath + "/" + srcDetails.name + "-" + dateTimeStamp
                    
                    if pathlib.Path(srcPath).is_dir():
                      shutil.copytree(srcPath, srcPath)
                      
                    else:
                      shutil.copy2(srcPath, dstLoc)
                    
if __name__ == '__main__':
    main()