#!/usr/bin/env python                                                                                                                                                                                                                         

import argparse
import ConfigParser
import os
import shutil
import sys
import time
# to read results database (json file)
import json
from collections import OrderedDict
import string
import errno
# check if file exists
def sanityCheckFile(filepath, msg=""):
    if( not os.path.exists(filepath) ):
        if(msg != ""):
            print msg + "\nAborting ..."
        else:
            print "The file " + filepath + " was not found\nAborting ..."
        exit(1)

# make a directory (don't fail if it exists)                                                                                                                                                                                                 
def makedir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def sanityCheckFile(filepath, msg=""):
    if( not os.path.exists(filepath) ):
        if(msg != ""):
            print msg + "\nAborting ..."
        else:
            print "The file " + filepath + " was not found\nAborting ..."
        exit(1)

def main():
    
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', required=True, help='Path to the original database in json format')
    parser.add_argument('-o', required=False, default="", help='Desired output asciidoc file')
    args = parser.parse_args()
    # prepare i/o paths and filenames
    jsonFile = args.i # usually $RESULTS/resultsDataBase/results.json
    sanityCheckFile(jsonFile) # check file existence
    baseName, ext = os.path.splitext(os.path.basename(args.i)) # separate $RESULTS/resultsDataBase  and results.json
    if args.o=="":
        fileNoExt, ext = os.path.splitext(args.i)
        asciidocFile = fileNoExt + '.adoc' # usually -> #RESULTS/resultsDataBase/results.json 
        print 'createAsciidocDB.py: No output specified, using input file name with .adoc extention: ' + asciidocFile
    else:
        makedir(args.o) # create output directory if needed
        asciidocFile = args.o # usually -> #RESULTS/resultsDataBase/results.json

    # ------------ Results Database initialization -------------                                                                                                                                                                             
    # initialize database by reading existing file or creating one if needed.
    resultsDB = OrderedDict()
    try:
        dbFile = open(jsonFile,'r')
        resultsDB = json.load(dbFile, object_pairs_hook=OrderedDict)
        dbFile.close()
    except:
        print 'createAsciidocDB.py: the file ' + jsonFile + ' was not found'
    
    adocFile = open(asciidocFile, 'w')

    #print 'RESULTS DB:'
    #print json.dumps(resultsDB, indent=4)
    #print ''


    # write text before table
    adocFile.write("AngioTK results table:\n\n")
    # write table title
    adocFile.write(".Results table\n")
    # write columns titles (i.e. the top row)
    adocFile.write("[style=\"verse,asciidoc\",options=\"header,footer\"]\n")
    adocFile.write("|===\n")
    adocFile.write("|Dataset\Steps")
    pipelineSteps = next (iter(resultsDB.values()))
    for step in pipelineSteps:
        adocFile.write('|'+step)
    adocFile.write("\n")
    # write other rowsrows (
    for dataset, pipelineSteps in resultsDB.items():
        adocFile.write('|' + dataset)
        for stepName, step in pipelineSteps.items():
            adocFile.write('|')
            for metadataName, metadata in step.items():
                if metadataName=='Screenshot':
                    adocFile.write( 'image:' + str(metadata) + '[\"screenshot\",width=100,link=\"' + str(metadata) + '\"]\n')
                else:
                    adocFile.write( metadataName + ': ' + str(metadata) + '\n')
        adocFile.write("\n")
    adocFile.write("|===\n")
    
    adocFile.close()

# Only do this, if we do not import as a module                                                                                                                                                                                               
if __name__ == "__main__":
    main()
