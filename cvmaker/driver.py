import os
import subprocess

import texcompiler as tc

from cvmaker.parseCMDInput import getCmdArgs
from cvmaker.readYAML import readYAMLFile
from cvmaker.processData import dataHandler

# driver method for cvmaker 
def buildResume():
    
    # read command line input
    args = getCmdArgs()
    
    if not args.recompile:
        # read specified data from file
        data = readYAMLFile(args.resumeFile)
        ordering = None
        if args.orderFile is not None:
            ordering = readYAMLFile(args.orderFile)

        # process resume data and write to file
        processedData = dataHandler(data)

        if not args.noWrite:
            texFiles = processedData.writeToFile(
                fileName = args.resumeFile,
                ordering = ordering,
                build = args.buildType, 
                splitFiles = args.splitFiles
            )

    # run latex
    if not (args.noCompile or args.noWrite):
        tc.compileTeX(
            'resume.tex', 
            packages = ['forestResume'],
            texEngine = 'xelatex',
            bibTexEngine = 'biber'
    )
