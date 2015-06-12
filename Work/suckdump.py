##                   ##
#    SuckAndDump      #
#                     #
#   Cameron Stewart   #
#    Last Modified:   #
#     06-20-2007      #
##                   ## 

import os
import sys
import shutil
import exceptions
import time

class Error(exceptions.EnvironmentError):
    pass

DocbookBase = 'XXX'
DocbookDumpBase = 'XXX'
WikiBase = 'XXX'
ProgramDataBase = 'XXX'
IncludeDirs = (ProgramDataBase+"/include.txt")
LogFile = open(ProgramDataBase+"/sdlog.txt", 'a')
ExcludeList = []
ErrorFlag = 0
ApacheUserId = 48
ApacheGroupId = 48

#######################################################################
#
# This is the initializer function
#
def init():

    clearScreen()
        
    #
    # Initialize variables (delete old copies and create new blank ones)
    #
        
    mode = raw_input("Welcome to SuckDump!\n Would you like to:\n\n(s)uck ALL files from docbook to wiki\n(c)hoose a single directory tree to suck into the wiki\n(d)ump files from wiki back to docbook\n(e)xclude directory from suck\n(f)inish and exit program\n\n")
    if mode == 's' or mode == 'S':
        clearScreen()
        print "Sucking "+DocbookBase+" to wiki...\n"
        
        #
        # Grab locations and call the functions
        #
        output = open(IncludeDirs, 'w')
        dirDive(output, DocbookBase)
        output.close()
        input = open(IncludeDirs, 'r')
        include_lines = input.readlines()
        input.close()
        output = open(IncludeDirs, 'w')
        sorted_include_lines = removeRepeated(include_lines)
        output.writelines(sorted_include_lines)
        output.close()
        convertToWiki()
        init()
        return
    if mode == 'c' or mode == 'C':
        clearScreen()
        path = raw_input("Please enter the whole path of the directory you wish to \"suck\"\n")
        output = open(IncludeDirs, 'w')
        dirDive(output, path)
        output.close()
        input = open(IncludeDirs, 'r')
        include_lines = input.readlines()
        input.close()
        output = open(IncludeDirs, 'w')
        sorted_include_lines = removeRepeated(include_lines)
        output.writelines(sorted_include_lines)
        output.close()
        suckSingleDir(path)
        init()
    elif mode == 'd' or mode == 'D':
        clearScreen()
        print "Dumping Wiki to plain text repository, "+DocbookDumpBase+"....\n"
        dumpToDocbook()
        init()
    elif mode == 'e' or mode == 'E':
        clearScreen()
        exclude = raw_input("Enter string to exclude...\n\nNote: This feature isnt fully integrated yet, right now this removes any directory or file matching this string.\n I plan to have a seperate part that allows a specific path to be excluded\n\n")
        if not exclude == '': 
            ExcludeList.append(exclude)
        clearScreen()
        print "List of exclusions:\n"
        for i in ExcludeList:
            print i+"\n"
        raw_input("Press Enter to continue\n")
        init()
    elif mode == 'f' or mode == 'F':
        LogFile.close()
        print "\n\nTo view the logfile open "+ProgramDataBase+"/sdlog.txt\n"
        sys.exit(1)
    else:
        print mode+": This is not a valid selection, please try again."
        TRASH = raw_input("Press \'Enter\' to continue")
        init()
        return

#
#################### END INIT #########################################        

########################################################################
#
# Grab names of all files and dirs
# located under this dir
#
def dirDive(output, Cur):
    paths = os.listdir(Cur) 
    for i in paths:
        os.chdir(Cur)
        i = os.path.abspath(i)
        just_this_dir = getBasePath(i, '/')
        #
        # If current path is a file
        #
        if  os.path.isfile(i):
            if just_this_dir[0] == '.' or just_this_dir[-1] == '~' or just_this_dir[-1] == '#' or isExcluded(i):
                pass
            else:
                output.write(i+"\n")

        #
        # If current path is a directory
        #
        elif os.path.isdir(i):
            if just_this_dir[0] == '.' or just_this_dir[-1] == '~' or just_this_dir[-1] == '#' or isExcluded(i):
                pass
            else:
                output.write(i+"\n")
                dirDive(output, i)
           
        else:
            continue
        
#
#
#### END dirDive #########################################################


##########################################################################
#
# This function creates the Base Path
#
def getBasePath(path, symbol):
    index = path.rfind(symbol)
    return path[(index +1):]
#
#
#### END getBasePath ####################################################


#########################################################################
#
# This function returns the path to a childs parent,
# The difference between this and getBasePath is that
# this returns the opposite of what that returns
#
def getParentPath(path, symbol):
    index = path.rfind(symbol)
    return path[:index]
#
#
#### END getParentPath #################################################


########################################################################
#
# This function takes the current path and adds a link to the file it represents to
# its parents wiki page
#
def addLinkToParent(child_path, parent_path):
    try:
        output = file(parent_path+'/revisions/00000001', 'a')
        child_name = getBasePath(child_path, ')')
        output.write("   * [:/" + child_name + ": " + child_name + "]\n")
        output.close()
    except:
        raw_input("Cannot open "+parent_path+"/revisions/00000001 \n\nPress Enter to Continue")
        pass
        
#
#
#### END addLinkToParent ##############################################


########################################################################
#
# This function takes the file passed to it and uploads/links the file 
# to its appropriate spot in the wiki.
#
def addAttachmentToParent(child_path, parent_path):
    #
    # Copy the actual file into the appropriate directory on the wiki server
    #
    output = file(parent_path+'/revisions/00000001', 'a')
    shutil.copy(child_path, parent_path+"/attachments")
    child_name = getBasePath(child_path, '/')
    output.write("   * attachment:"+child_name+"\n")
    output.close()
#
#
#### END addLinkToParent ##############################################



######################################################################
#
# This is the function that takes the included directories (and files) then formats
# and copies them into the destination directory to be read by moinmoin.
#
def convertToWiki():

    #
    # DocbookBase: Where we are going to suck the files from
    # WikiBase: Where we are going to spit formatted files out for wiki.
    #
    
    input_include = open(IncludeDirs, 'r')
    lines_include = input_include.readlines()
    input_include.close()

    #
    # This "child_dir" is needed because the way directories in the wiki
    # are organized is quite different from standard linux behavior.
    # This gives the "child" of the base tree (say, for example, docbook
    # as opposed to /nfs/dsys/docbook) from which the tree will be converted to
    # wiki standards.
    #
    child_dir = getBasePath(DocbookBase, '/')
    destination_root = WikiBase+"/"+child_dir

    revisions = destination_root + '/revisions'
    current = destination_root+"/current"

    try:
        os.mkdir(destination_root)
    except:
        pass
        
    try:
        os.mkdir(revisions)
    except OSError:
        pass

    open(revisions+'/00000001', 'w').close()
    cur_in = open(current, 'w')
    cur_in.write("00000001")
    cur_in.close()
    
    
    #
    # Create the rest of the pages hanging off of the BasePage
    #
    for i in lines_include:
        j = i.replace('\n', '')
        #
        # Make appropriate directories and files for writing to
        #
        
        destination = j[((len(DocbookBase) - len(j)) + 1):]
        #
        # Various filters to keep pages "creatable" in moinmoin
        #
        destination = child_dir + "/" + destination
        destination = destination.replace('.', '_')
        destination = destination.replace('-', '_')
        destination = destination.replace('/', '(2f)')
        destination = WikiBase+"/"+destination
        
                
        parent_path = getParentPath(destination, '(')

        revisions = destination + '/revisions'
        
        #
        # If current path leads is a file then write data to this file
        #
        if os.path.isfile(j):

            #
            # Do a test which indicates whether this is a plain text file.
            # If not, then simply attach it as is (without creating a page for it
            #
            file_in_question = os.popen("file "+j, "r")
            line_in_question = file_in_question.readlines()
    
            if line_in_question[0].find("ASCII") == -1:
                try:
                    os.mkdir(parent_path + '/attachments')
                except OSError:
                    pass

                addAttachmentToParent(j, parent_path)
                file_in_question.close()

            
            
            else:
                createNeccesaryWikiDirs(destination, revisions)
                #
                # file_to_wiki_out: file to write info to for wiki
                # file_to_wiki_in: file from which info is read
                # file_to_wiki_lines: buffer to hold entire file_to_wiki_in data
                # current_out: file to write current revision of page (for wiki purposes)
                #
                file_to_wiki_out = open(revisions+'/00000001', 'w')
                file_to_wiki_in = open(j, 'r')
                current_out = open(destination + "/current", 'w')
                file_to_wiki_lines = file_to_wiki_in.readlines()
                
                #
                # Write data to this file
                #
                file_to_wiki_out.write('{{{\n')
                file_to_wiki_out.writelines(file_to_wiki_lines)
                file_to_wiki_out.write('}}}\n')
                
                #
                # Close files
                #
                file_to_wiki_in.close()
                file_to_wiki_out.close()
                
                
                current_out.write("00000001\n")
                current_out.close()
                
                
                
            #
            # If current path is a directory, make a file representing this and write data to it
            #
        elif os.path.isdir(j):
            createNeccesaryWikiDirs(destination, revisions)
            current_out = open(destination + "/current", 'w')
            current_out.write("00000001\n")
            current_out.close()
            

           

    #
    # This basically makes sure the links page doesnt get all kinds of
    # duplicate links everytime the script is run again.
    #
    link_page = open(parent_path+"/revisions/00000001", 'r')
    link_lines = link_page.readlines()
    unique_sorted_lines = removeRepeated(link_lines)
    link_page.close()
    link_page_out = open(parent_path+"/revisions/00000001", 'w')
    link_page_out.writelines(unique_sorted_lines)
    link_page_out.close()
            
    rchown(WikiBase, ApacheUserId, ApacheGroupId)
    rchmod(WikiBase, 0770, 0660)
    
#
#
#### END convertToWiki #############################################################


###################################################################################
#
#
#
def suckSingleDir(path):
    input_include = open(IncludeDirs, 'r')
    lines_include = input_include.readlines()
    input_include.close()
    child_dir = getBasePath(DocbookBase, '/')
    #
    # Create the rest of the pages hanging off of the BasePage
    #
    for i in lines_include:
        j = i.replace('\n', '')
        #
        # Make appropriate directories and files for writing to
        #
        
        destination = j[((len(DocbookBase) - len(j)) + 1):]
        #
        # Various filters to keep pages "creatable" in moinmoin
        #
        destination = child_dir + "/" + destination
        destination = destination.replace('.', '_')
        destination = destination.replace('-', '_')
        destination = destination.replace('/', '(2f)')
        destination = WikiBase+"/"+destination
        
        
        parent_path = getParentPath(destination, '(')
        
        revisions = destination + '/revisions'
        
        #
        # If current path leads is a file then write data to this file
        #
        if os.path.isfile(j):
            
            #
            # Do a test which indicates whether this is a plain text file.
            # If not, then simply attach it as is (without creating a page for it
            #
            file_in_question = os.popen("file "+j, "r")
            line_in_question = file_in_question.readlines()
            
            if line_in_question[0].find("ASCII") == -1:
                try:
                    os.mkdir(parent_path + '/attachments')
                except OSError:
                    pass
                
                addAttachmentToParent(j, parent_path)
                file_in_question.close()
                
                
                
            else:
                createNeccesaryWikiDirs(destination, revisions)
                #
                # file_to_wiki_out: file to write info to for wiki
                # file_to_wiki_in: file from which info is read
                # file_to_wiki_lines: buffer to hold entire file_to_wiki_in data
                # current_out: file to write current revision of page (for wiki purposes)
                #
                file_to_wiki_out = open(revisions+'/00000001', 'w')
                file_to_wiki_in = open(j, 'r')
                current_out = open(destination + "/current", 'w')
                file_to_wiki_lines = file_to_wiki_in.readlines()
                
                #
                # Write data to this file
                #
                file_to_wiki_out.write('{{{\n')
                file_to_wiki_out.writelines(file_to_wiki_lines)
                file_to_wiki_out.write('}}}\n')
                
                #
                # Close files
                #
                file_to_wiki_in.close()
                file_to_wiki_out.close()
                
                
                current_out.write("00000001\n")
                current_out.close()
                
                
                
        #
        # If current path is a directory, make a file representing this and write data to it
        #
        elif os.path.isdir(j):
            createNeccesaryWikiDirs(destination, revisions)
            current_out = open(destination + "/current", 'w')
            current_out.write("00000001\n")
            current_out.close()
                
                
                
                
    #
    # This basically makes sure the links page doesnt get all kinds of
    # duplicate links everytime the script is run again.
    #
    link_page = open(parent_path+"/revisions/00000001", 'r')
    link_lines = link_page.readlines()
    unique_sorted_lines = removeRepeated(link_lines)
    link_page.close()
    link_page_out = open(parent_path+"/revisions/00000001", 'w')
    link_page_out.writelines(unique_sorted_lines)
    link_page_out.close()
    
    rchown(WikiBase, ApacheUserId, ApacheGroupId)
    rchmod(WikiBase, 0770, 0660)
#
#
################### END suckSingleDir #############################################




####################################################################################
#
# This function really just saves a little space since it is the largest amount of repeated code
# that I could squeeze out of the for loop in convertToWiki
#
def createNeccesaryWikiDirs(destination, revisions):
    #
    # Make appropriate directories and files for writing to
    #
    try:
        os.mkdir(destination)
    except OSError:
        #raw_input("Cannot make "+destination) 
        pass
    
    try:
        os.mkdir(revisions)
    except OSError:
        #raw_input("Cannot make "+revisions)
        pass
        
    open(revisions+"/00000001", 'w').close()
    open(destination+"/current", 'w').close()
    parent_path = getParentPath(destination, '(')
    addLinkToParent(destination, parent_path)

#
#
################### END createNeccesaryWikiDirs ###################################

####################################################################################
# 
# This function sort of does the overlying work for a dump to wiki.
#
def dumpToDocbook():
    os.chdir(WikiBase)
    oldlines = os.listdir(WikiBase)
    newlines = convertWikiFormToFileForm(oldlines)
    #
    # I will sort the lists so that a parent and its child will be listed
    # adjacent to one another.  This allows me to test for leaf nodes since
    # I only want to copy their contents.
    #
    oldlines.sort()
    newlines.sort()

    cntr = 0

    for i in newlines:

        j = i.replace('\n', '')
        c = oldlines[cntr].replace('\n', '')
        
        try:
            os.makedirs(j)
        except OSError:
            pass
        

        try:
            k = newlines[cntr+1]
            k = k.replace('\n', '')
            try:
                copytree(WikiBase+"/"+c+"/attachments/", j)
            except OSError:
                pass

            if isLeaf(j, k):
                copyRevisions(WikiBase+"/"+c+"/revisions/", j)
            else:
                pass
            
        except IndexError:
            #
            # Last item in list, assume its a leaf node.
            #
            try:
                copytree(WikiBase+"/"+c+"/attachments/", j)
            except OSError:
                pass
            
            copyRevisions(WikiBase+"/"+c+"/revisions/", j)
        
        cntr += 1
#
#
##### END dumpToDocbook ###########################################################

###################################################################################
#
# This function does all the work of copying and formatting files from a source
# to a destination.  This will take the folder <wikipage>/revisions and copy the
# contents (in the form 00000001, 00000002, ...) to <filename>.1, <filename>.2, ...
#
def copyRevisions(source, destination):
    
    try:
        tail, head = os.path.split(destination)
        filelist = os.listdir(source)
        for f in filelist:
            ff = f.replace('0', '')
            shutil.copy(source+f, destination+"/"+head+"."+ff)
    except OSError:
        print >> LogFile, "Cant copy: "+source
        print >> LogFile, "Deleting folder: "+destination
        print >> LogFile, "This error is likely due to this being an unused (and therefore blank) page and in most cases can be ignored."
        print >> LogFile, "\n"
        os.rmdir(destination)
#
#
############## END copyRevisions ###################################################


###################################################################################
#
# This function takes the input in the 'lines' variable and converts the lines
# to a filesystem friendly format.
# (i.e. docbook(2f)Dell(2f)draccards -> docbook/Dell/draccards)
#
def convertWikiFormToFileForm(lines):
    l2 = []
    for i in lines:
        j = i.replace('(2f)', "/")
        j = j.replace('(2d)', '')
        j = j.replace('(2e)', '')
        l2.append(DocbookDumpBase+"/"+j)

    return l2

#
#
######### END convertWikiFormToFileForm ###########################################


###################################################################################
#
# This function is a modified version of pythons own shutil.copytree.
# I was quite dissatisfied with their version for several reasons, the main
# one being that if any directory that it was trying to copy to already existed,
# the function would simply fail.  I have changed this.
#
def copytree(src, dst, symlinks=False):
    """Recursively copy a directory tree using copy2().

    The destination directory must not already exist.
    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied.

    XXX Consider this example code rather than the ultimate tool.

    """
    names = os.listdir(src)
    try:
        os.mkdir(dst)
    except OSError:
        pass
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                shutil.copy2(srcname, dstname)
            #    
            # XXX What about devices, sockets etc.?
            #
        except (IOError, os.error), why:
            errors.append((srcname, dstname, why))
        #    
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        #
        except Error, err:
            errors.extend(err.args[0])
    if errors:
        raise Error, errors
#
#
#################### END copytree ##################################################


###################################################################################
#
# This function takes a path and a path lexicographically adjacent and determines
# if one is the parent of the other (if path 1 is the parent of path 2) to decide
# whether its file contents should be copied. This makes it so a bunch of "link"
# pages are not copied.
#
def isLeaf(path1, path2):

    tail2, head2 = os.path.split(path2)
    
    if tail2.find(path1) == -1:
        return True
    else:
        return False
#
#
################# END isLeaf ######################################################


##################################################################################
#
# This function returns the input list with only one copy of each element from the
# argument
def removeRepeated(list):
    l2 = []
    for item in list:
        if item not in l2:
            l2.append(item)
    l2.sort()
    return l2
#
#
############## END removeRepeated ###############################################



################################################################################
#
# This function is simply a recursive chmod since python doesnt have one !!!
# This is also has a set of distinct 'modes' file and directory.
# These are here because moin has specific permissions for files vs. dirs.
#
def rchmod(dir, dir_mode, file_mode):
    if os.path.isdir(dir):
        os.chmod(dir, dir_mode)
        paths = os.listdir(dir)
        for i in paths:
            os.chdir(dir)
            i = os.path.abspath(i)
            if os.path.isdir(i):
                rchmod(i, dir_mode, file_mode)
            else:
                os.chmod(i, file_mode)
    else:
        os.chmod(dir, file_mode)

#
#
################### END rchmod ##################################################


#################################################################################
#
# This function is a recursive version of chown since python does not have this feature.
#
def rchown(dir, user, group):
    if os.path.isdir(dir):
        os.chown(dir, user, group)
        paths = os.listdir(dir)
        for i in paths:
            os.chdir(dir)
            i = os.path.abspath(i)
            if os.path.isdir(i):
                rchown(i, user, group)
            else:
                os.chown(i, user, group)
    else:
        os.chmod(dir, user, group)
#
#
#################### END rchown ################################################


###############################################################################
#
# This is put into its own function to keep this code less messy
#
def clearScreen():
    #
    # My only line of non-python code
    #
    try:
        os.system("clear")
    except:
        pass
#
#
#################### END clearScreen ########################################

#############################################################################
#
#
# This function is here to allow users to designate certain strings which when encountered
# will have them and their children removed from the "Suck" proccess
def isExcluded(file):
    isolated_filename = getBasePath(file, '/')
    for i in ExcludeList:
        if i == isolated_filename:
            return True
        else:
            pass

    return False
#
#
###################### END isExcluded ########################################
        

print >> LogFile, "Time: "+time.asctime(time.localtime())
print >> LogFile, "#######################################\n\n"
init()
