#!/usr/bin/python
# -*- coding: utf8 -*-
#########################################################
# split a file into a set of portions; join.py puts them
# back together; this is a customizable version of the 
# standard unix split command-line utility; because it
# is written in Python, it also works on Windows and can
# be easily tweaked; because it exports a function, it 
# can also be imported and reused in other applications;
#########################################################

import sys, os
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)                   # default: roughly a floppy

def split(fromfile, todir, chunksize=chunksize):
    file_name = fromfile 
    #file_name = (file_name.split('/')[-1])
    #print (filename)
    if not os.path.exists(todir):                  # caller handles errors
        os.mkdir(todir)                            # make dir, read/write parts
    else:
        i=1
        while  1:
            todir = todir+str(i)
            if not os.path.exists(todir):
                os.mkdir(todir)
                break
            i=i+1
        #for fname in os.listdir(todir):            # delete any existing files
            #os.remove(os.path.join(todir, fname)) 
    partnum = 0
    #print (os.path.exists(fromfile))
    input = open(os.path.join(fromfile), 'rb')                   # use binary mode on Windows
    file_array=[]
    while 1:                                       # eof=empty string from read
        chunk = input.read(chunksize)              # get next part <= chunksize
        if not chunk: break
        partnum  = partnum+1
        filename = os.path.join(todir, ('.'+file_name+'_'+str(partnum)))
        file_array.append(filename)
        fileobj  = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()                            # or simply open(  ).write(  )
    input.close(  )
    #shutil.rmtree(os.path.join(todir))
    assert partnum <= 9999                         # join sort fails if 5 digits
    #return partnum
    back=[file_array,todir]
    return back
            
if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print 'Use: split.py [file-to-split target-dir [chunksize]]'
    else:
        if len(sys.argv) < 3:
            interactive = 1
            fromfile = raw_input('File to be split? ')       # input if clicked 
            todir    = raw_input('Directory to store part files? ')
        else:
            interactive = 0
            fromfile, todir = sys.argv[1:3]                  # args in cmdline
            if len(sys.argv) == 4: chunksize = int(sys.argv[3])
        absfrom, absto = map(os.path.abspath, [fromfile, todir])
        print 'Splitting', absfrom, 'to', absto, 'by', chunksize

        try:
            parts = split(fromfile, todir, chunksize)
        except:
            print 'Error during split:'
            print sys.exc_type, sys.exc_value
        else:
            print 'Split finished:', parts, 'parts are in', absto
        if interactive: raw_input('Press Enter key') # pause if clicked
