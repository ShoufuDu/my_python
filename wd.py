import os
import re
import shutil
import subprocess
import sys


inc_file='.agm'
g_dst='C:\\mywork\\tasks\\NSW\\EntityGames\\maths'
g_src='C:\\mywork\\tasks\\NSW\\EntityGames\\Win'

def walkDir(top):
    global inc_file
    global g_dst

    for root,dirs,files in os.walk(top,True):
        files = [f for f in files if f.endswith(inc_file)]

        for fname in files:
            process_wd(root,fname,g_dst)

def process_wd(root,file,arg):
    winegPath = os.path.join(root,"GameCompiler.exe")
    inputFile = os.path.join(root,file)

    cmdline = winegPath,inputFile
    subprocess.call(cmdline,shell=True)
    outfile = os.path.join(root,"GameDef.dat.enc")

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

walkDir(g_src)