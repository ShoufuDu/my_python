import sys
import os
import getopt
import shutil
import re

const_short_opt="hps:d:"
const_long_opt=["help","pid","src=","dst="]

# arguments for all process procedure
process_pid=False
process_pid_src=None
process_pid_dst=None

class Args:
    def __init__(self):
        self.process_pid=False
        self.process_pid_src=None
        self.process_pid_dst=None

class Usage(Exception):
    def __init__(self,msg):
        self.msg = msg

def showUsage():
    print "-h|--help for help"
    print "-p|--pid"
    print "-s src -d dst"
    print "exp: -p -s c:\\src -d d:\\"
    return 0

def parseCmd(opts):
    args = Args()

    for o,p in opts:
        if o in('-h','--help'):
            showUsage()
            return 0

        # parse process pid arguments
        if o in('-p','--pid'):
            args.process_pid=True

        if o in('-s','--src'):
            if args.process_pid:
                args.process_pid_src=p

        if o in('-d','--dst'):
            if args.process_pid:
                args.process_pid_dst=p

        # parse new process arguments...

    return args

def walkDir(top,**args):
    for root,dirs,files in os.walk(top,True):
        # for d in dirs:
        for f in files:
            args['hook_f'](root,f,args['hook_f_arg'])

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
def process_xxx_hook(root,file,arg):
    return 0

def process_xxx_proc(src,dst):
    return 0


def processMain(args):
    # process pid
    if args.process_pid:
        return process_pid_proc(args.process_pid_src,
                                args.process_pid_dst)
    # add new process ...
    # if args.process_pid:
    #     return process_pid_proc(args.process_pid_src,
    #                             args.process_pid_dst)

#--------------------------------------------------------------------------------------
# main
#--------------------------------------------------------------------------------------
def main(argv=None):
    if(argv is None):
        argv = sys.argv
    try:
        try:
            opts,args = getopt.getopt(sys.argv[1:],const_short_opt,const_long_opt)
        except getopt.error,msg:
            raise Usage(msg)

        args = parseCmd(opts)

        processMain(args)

        return 0

    except Usage,err:
        print >> sys.stderr,err.msg
        print >> sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())


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
                print e
    return 1