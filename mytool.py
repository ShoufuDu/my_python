import argparse
import getopt
import os
import re
import shutil
import subprocess
import sys
import time

const_short_opt="hps:d:"
const_long_opt=["help","pid","src=","dst="]

# arguments for all process procedure
process_pid=False
process_src=None
process_dst=None

class Args:
    def __init__(self):
        self.process_pid=False
        self.process_src=None
        self.process_dst=None
        self.process_wd=False
        
def showUsage():
    print ("-h|--help for help")
    print ("-p|--pid")
    print ("-s src -d dst")
    print ("exp: -p -s c:\\src -d d:\\")
    return 0

def parseCmd(opts):
    args = Args()

    for o,p in opts:
        if o in('-h','--help'):
            showUsage()
            return 0

        # parse process pid arguments
        if o in('-p','--pid'):
            args.pid=True

        if o in('-wd','--wizardswand'):
            args.process_wd=True

        if o in('-s','--src'):
            if args.pid or args.process_wd:
                args.src=p

        if o in('-d','--dst'):
            if args.pid or args.process_wd:
                args.dst=p

        # parse new process arguments...

    return args

def walkDir(top,**args):
    for root,dirs,files in os.walk(top,True):
        # exclude dirs
        # dirs[:] = [os.path.join(root, d) for d in dirs]
        if 'excludes' in args:
            dirs[:] = [d for d in dirs if not re.endswith(tuple(args['excludes']))]

        # exclude/include files
        # files = [os.path.join(root, f) for f in files]
        if 'excludes' in args:
            files = [f for f in files if not f.endswith(tuple(args['excludes']))]
        if 'includes' in args:
            files = [f for f in files if f.endswith(tuple(args['includes']))]

        for fname in files:
            args['hook_f'](root,fname,args['hook_f_arg'])
            # print(fname)

#--------------------------------------------------------------------------------------
#   name : process_pid_hook
#   func:  process pid
#   root : the root dir of source file to be processed
#   file : the source file to be processed
#   arg  : additional arguments needed
#--------------------------------------------------------------------------------------
def process_pid_hook(root,file,arg):
    (fn,ext) = os.path.splitext(file)
    new_name = fn+'_bk'+ext
    old_path = os.path.join(root,file)
    new_path= os.path.join(arg,new_name)
    if not os.path.exists(arg):
        os.mkdir(arg)
    shutil.copy(old_path,new_path)
    return 0

def process_pid_proc(src,dst):
    args={'hook_f':process_pid_hook,
          'hook_f_arg':"./a12"}
    walkDir(src,**args)
    return 0

#--------------------------------------------------------------------------------------
#   name : # add new process ...
#   func:  process pid
#   root : the root dir of source file to be processed
#   file : the source file to be processed
#   arg  : additional arguments needed
#--------------------------------------------------------------------------------------
def process_wd_hook(root,file,arg):
    winegPath = os.path.join(root,"GameCompiler.exe")
    inputFile = os.path.join(root,file)

    cmdline = winegPath,inputFile
    subprocess.call(cmdline,shell=True)
    outfile = os.path.join(root,"GameDef.dat.enc")

    # time.sleep(1)

    try:
        if not os.path.exists(outfile):
            exit(1)
        
        varation = re.sub(r"WW_(V\d+).agm",r"\1",file)

        outDir = os.path.join(arg,varation)
        if not os.path.exists(outDir):
            os.mkdir(outDir)
        
        # #copy GameDef.dat.enc
        dstFile = os.path.join(outDir,"GameDef.dat.enc")
        shutil.copy(outfile,dstFile)
        os.remove(outfile)
        
        #copy agm files
        shutil.copy(inputFile,os.path.join(outDir,file))

    except IOError as e:
            print(e)

    return 0

def process_wd_proc(src,dst):
    args={'includes':['.agm'],'hook_f':process_wd_hook,'hook_f_arg':dst}
    walkDir(src,**args)
    return 0


def processMain(args):
    # process pid
    if args.pid:
        return process_pid_proc(args.src,
                                args.dst)
    # add new process ...
    if args.wizardswand:
        return process_wd_proc(args.src,args.dst)
#--------------------------------------------------------------------------------------
# main
#--------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="mypython tool for game")
    # group = parser.add_mutually_exclusive_group()
    parser.add_argument("-p","--pid", help="process pid",action="store_true")
    parser.add_argument("-s",'--src',help="source path")
    parser.add_argument("-d",'--dst',help="destination path")
    parser.add_argument("-wd","--wizardswand", help="process wizardswand agm files",action="store_true")
    args = parser.parse_args()

    processMain(args)

if __name__ == "__main__":
    main()


def example_xopy():
    Dest = "/a1"
    rules = re.compile("/a")

    for root,dirs,files in os.walk(top,True):
        newTop = rules.sub(Dest,root)
        if not os.path.exists(newTop):
            os.mkdir(newTop)

        for d in dirs:
            print(os.path.join(root,d))
            d = os.path.join(newTop,d)
            if not os.path.exists(d):
                os.mkdir(d)

        for f in files:
            (fn,ext) = os.path.splitext(f)
            old_path = os.path.join(root,f)
            new_name = fn+'_bk'+ext
            new_path= os.path.join(newTop,new_name)
            try:
                shutil.copy(old_path,new_path)
            except IOError as e:
                print(e)
    return 1
