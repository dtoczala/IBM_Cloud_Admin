#!/usr/bin/python
# uses python 2.7
#
import os
import sys
import subprocess
import argparse
import json
import codecs
import unicodecsv as csv
import pandas as pd
import string
import datetime
import re

#################################################################
#
# Setup constants
#
LOGFILE = "IBM_Cloud_Admin.output.log"
BILLING_FILE = ""
DBLQUOTE = '"'

DEBUG = True
#DEBUG = False

API_ENDPOINT = "https://api.ng.bluemix.net"

REGION_LIST = ["us-south", "us-east", "eu-gb", "eu-de", "au-syd" ]

#################################################################
#
# Setup global variables
#

textFileName = ""
textFile = {}

# Main definition
menu_actions  = {}

#
# Setup input values
#
inpUserName = ""
inpPwd = ""
inpToken = ""
#inpOutputFilename = ""
#inpFilter = ""
#inpLabel = ""

#
# Setup environment values
#
envSpace = ""
envOrg = ""
envAccount = ""
envRegion = ""
envUser = ""
envResourceGroup = ""
envAPIEndpoint = API_ENDPOINT


#################################################################
#
# Check for proper version of python
#
outputLog = open(LOGFILE, "w")
req_version_major = 2
req_version_minor = 7
cur_version_major = sys.version_info.major
cur_version_minor = sys.version_info.minor
if ((cur_version_major != req_version_major) or (cur_version_minor != req_version_minor)):
    outputLog.write("This program runs with Python version " + str(req_version_major) + "." + str(req_version_minor) + ", and you are running version " + str(cur_version_major) + "." + str(cur_version_minor))
    outputLog.write(" \n\n")
#################################################################
#
# Parse command line arguments
#
cloudBilling = False
cloudSecurity = False

parser = argparse.ArgumentParser()

parser.add_argument("-u","--userID",required=False,help="User IBM Cloud ID")
parser.add_argument("-p","--pwd",required=False,help="User IBM Cloud password")
parser.add_argument("-t","--token",required=False,help="IBM Cloud Token")
parser.add_argument("-b","--billing",action="store_true",default=False,dest="billing_flag",help="Dump billing data")
parser.add_argument("-s","--security",action="store_true",default=False,dest="security_flag",help="Dump security data")
#
# Grab the arguments off the command line
#
errorFound = False
args = parser.parse_args()
cloudUser = args.userID
cloudPwd = args.pwd
cloudToken = args.token
if args.billing_flag:
    cloudBilling = True
if args.security_flag:
    cloudSecurity = True
#
# Calculate the current date
#
now = datetime.datetime.now()
todaystr = str(now.strftime("%Y")) + "-" + str(now.strftime("%m"))

#
# Output debugging data
#
if (DEBUG):
    outputLog.write("User ID is - " + str(cloudUser) + "\n")
    outputLog.write("User password is - " + str(cloudPwd) + "\n")
    outputLog.write("Tokens is - " + str(cloudToken) + "\n")
    outputLog.write("Billing flag is - " + str(cloudBilling) + "\n" )
    outputLog.write("Current date is - " + str(now.strftime("%Y")) + "-" + str(now.strftime("%m")) + "\n\n")
#
#################################################################
#  ROUTINES
#################################################################
#
# My Logging
#
def MyLogging (cmd):
    #
    # Set return status
    #
    stat = ""
    #
    # Check if DEBUG flag is set, if it is, then log it
    #
    if (DEBUG):
        outputLog.write(cmd + "\n")
    #
    return stat

#
# ExecCommand
#
def ExecCommand (cmd):
    #
    # Set return status
    #
    stat = ""
    #
    # Run command
    #
    try:
        #os.system(cmd)
        MyLogging("COMMAND -> " + cmd)
        subprocess.call(cmd,shell=True)
        MyLogging("OUTPUT  -> redirected to user terminal session....")
    except:
        stat = "ERROR (ExecCommand)- on call -> " + str(cmd) + "\n"
        outputLog.write(stat)
    #
    return stat

#
# ExecCommand
#
def ExecCmd_Output (cmd):
    #
    # Set return status
    #
    tmpout = ""
    cmdout = ""
    errout = ""
    #
    # Run command
    #
    try:
        #os.system(cmd)
        MyLogging("COMMAND -> " + cmd)
        cmdout = subprocess.check_output(cmd,shell=True)
        MyLogging("OUTPUT  -> " + cmdout)
    except:
        tmpout = "ERROR (ExecCmd_Output) - on call -> " + str(cmd) + "\n"
        outputLog.write(tmpout)
        errout = str(tmpout) + " "
    #
    if (errout != ""):
        tmpout = "ERROR (ExecCmd_Output) - on call -> " + str(cmd) + "\n"
        outputLog.write(tmpout)
        tmpout = "                      error code -> " + str(errout) + "\n"
        outputLog.write(tmpout)
        tmpout = "                      returned   -> " + str(cmdout) + "\n"
        outputLog.write(tmpout)
    return cmdout

#################################################################
#
# Open a text file
#
def openTextFile(filename):
    #
    # Set the global name and filehandle
    #
    textFile = open(filename, "w")
    return textFile

#################################################################
#
# Write a line out to a text file
#
def writeTextFile(textfile,txtline):
    #
    # Set the global name and filehandle
    #
    stat = textfile.write(txtline)
    return stat

#################################################################
#
# Close a text file
#
def closeTextFile(textfile):
    #
    # Set the global name and filehandle
    #
    stat = textfile.close()
    return stat

#################################################################
#
# Open a text file
#
def openCsvFile(filename):
    #
    # Set the global name and filehandle
    #
    csvFile = csv.writer(open(filename, "w"))
    return csvFile

#################################################################
#
# writeCSVSummaryRecord - Dump a row of account summary data into
#                           output CSV file
#
def writeCSVSummaryRecord(csvFile, inp_1, inp_2, inp_3, inp_4, inp_5, inp_6, inp_7, inp_8, inp_9):
    #
    # fileCSV.writerow(('Account ID','Date','Billable','Type','Resource ID','Name','Units','Quantity','Cost'))
    errout = ""
    try:
        col_1 = str(inp_1)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 1 " + str(inp_1) + "\n"
    try:
        col_2 = str(inp_2)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 2 " + str(inp_2) + "\n"
    try:
        col_3 = str(inp_3)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 3 " + str(inp_3) + "\n"
    try:
        col_4 = str(inp_4)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 4 " + str(inp_4) + "\n"
    try:
        col_5 = str(inp_5)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 5 " + str(inp_5) + "\n"
    try:
        col_6 = str(inp_6)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 6 " + str(inp_6) + "\n"
    try:
        col_7 = str(inp_7)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 7 " + str(inp_7) + "\n"
    try:
        col_8 = str(inp_8)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 8 " + str(inp_8) + "\n"
    try:
        col_9 = str(inp_9)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 9 " + str(inp_9) + "\n"
    #
    # Write it out
    #
    try:
        csvFile.writerow([col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9])
    except UnicodeDecodeError:
        errout = "ERROR - Unicode OUTPUT error \n"
    #
    # If error, return some error text, otherwise return a null string
    #
    return errout

#################################################################
#
# writeCSVDetailRecord - Dump a row of account summary data into
#                           output CSV file
#
def writeCSVDetailRecord(csvFile, inp_1, inp_2, inp_3, inp_4, inp_5, inp_6, inp_7, inp_8, inp_9, inp_10, inp_11, inp_12):
    #
    # writeCSVDetailRecord (csvoutfile,tmpAcctId,tmpDate,tmpRegion,tmpOrg,tmpSpace,Billable,tmpType,tmpResourceID,tmpName,tmpUnits,tmpQuantity, tmpCost)
    errout = ""
    try:
        col_1 = str(inp_1)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 1 " + str(inp_1) + "\n"
    try:
        col_2 = str(inp_2)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 2 " + str(inp_2) + "\n"
    try:
        col_3 = str(inp_3)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 3 " + str(inp_3) + "\n"
    try:
        col_4 = str(inp_4)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 4 " + str(inp_4) + "\n"
    try:
        col_5 = str(inp_5)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 5 " + str(inp_5) + "\n"
    try:
        col_6 = str(inp_6)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 6 " + str(inp_6) + "\n"
    try:
        col_7 = str(inp_7)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 7 " + str(inp_7) + "\n"
    try:
        col_8 = str(inp_8)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 8 " + str(inp_8) + "\n"
    try:
        col_9 = str(inp_9)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 9 " + str(inp_9) + "\n"
    try:
        col_10 = str(inp_10)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 10 " + str(inp_10) + "\n"
    try:
        col_11 = str(inp_11)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 11 " + str(inp_11) + "\n"
    try:
        col_12 = str(inp_12)
    except UnicodeDecodeError:
        errout = "ERROR - Unicode decode error on column 12 " + str(inp_12) + "\n"
    #
    # Write it out
    #
    try:
        csvFile.writerow([col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9, col_10, col_11, col_12])
    except UnicodeDecodeError:
        errout = "ERROR - Unicode OUTPUT error \n"
    #
    # If error, return some error text, otherwise return a null string
    #
    return errout

#################################################################
#
# Close csv file
#
def closeCsvFile(csvFile):
    #
    # Set the global name and filehandle
    #
    stat = csvFile.close()
    return stat

#################################################################
#
# Get user list from a csv file
#
def getUserCsvFile():
    #
    # Get the input filename and filehandle
    #
    userList = []
    print ("Enter name of file with accounts to be added")
    choice = raw_input(" >>  ")
    #
    # See if the file exists
    #

    try:
        with open(choice) as csvfile:
            for row in csvfile:
                tempList = []
                tempList = string.split(row,",")
                #
                # if you have entries, add them to your user ID list
                #
                if (tempList != []):
                    userList.extend(tempList)
    except:
        MyLogging("ERROR = Unable to open input user ID file " + str(choice))
    #
    # Get rid of any quote characters, and any newlines
    #
    userList = [i.replace('"','') for i in userList]
    userList = [i.replace('\n','') for i in userList]
    #
    # normal return
    #
    return userList

#################################################################
#
# Get date in YYYY-MM format, and return the previous month in
# the same YYYY-MM format
#
def getPrevMonth(datestr):
    #
    # Pull out the numeric year and month
    #
    thisMonth = int(datestr[5:7])
    thisYear = int(datestr[0:4])
    #
    # Subtract one from the month
    #
    thisMonth = thisMonth - 1
    if (thisMonth == 0 ):
        thisMonth = 12
        thisYear = thisYear -1
    #
    # Now convert those values back to string in the proper format
    #
    if (thisMonth < 10):
        #
        # Have to zero pad the month
        #
        newdatestr = str(thisYear) + "-0" + str(thisMonth)
    else:
        #
        # No need to zero pad
        #
        newdatestr = str(thisYear) + "-" + str(thisMonth)
    #
    return newdatestr

#################################################################
#
# Find Defaults - take the output from a BX target comand and populate the default
#                 settings for the IBM Cloud
#
def findDefaults():
    #
    # Define global variables
    #
    global envAPIEndpoint,envRegion,envUser,envAccount,envResourceGroup,envOrg,envSpace
    #
    # Execute the bx target command to get current default values
    #
    cmd = "bx target"
    errout = ExecCmd_Output(cmd)
    #
    # Take input string - parse it and find the values
    #
    myList = string.split(errout, "\n")
    for myLine in myList:
        #
        # Check each line for a colon, and split into a label and a value (label:value)
        #
        if (string.find(myLine,":") != -1):
            thisPair = string.split(myLine,":")
            myLabel = thisPair[0]
            myValue = thisPair[1].rstrip()
            #
            # Check for matching labels
            #
            if (myLabel == "Region"):
                envRegion = myValue.strip()
            if (myLabel == "User"):
                envUser = myValue.strip()
            if (myLabel == "Account"):
                envAccount = myValue.strip()
            if (myLabel == "Resource group"):
                envResourceGroup = myValue.strip()
            if (myLabel == "Org"):
                envOrg = myValue.strip()
            if (myLabel == "Space"):
                envSpace = myValue.strip()
    #
    # If error, return some error text, otherwise return a null string
    #
    return

#################################################################
#
# shortAcctName - return a short (6 charcters or less) version of
#                 the current account name
#
def shortAcctName():
    #
    # Define global variables
    #
    global envAccount
    #
    # Execute the bx target command to get current default values
    #
    if (len(envAccount) > 10):
        shortName = str(envAccount[0:9])
    else:
        shortName = str(envAccount)
    #
    # Change any whitespace to underscores
    #
    retName = re.sub('\s+', '_', shortName)
    #
    # Change any non-alphanumeric to underscores
    #
    retName = re.sub('\W+', '_', shortName)
    #
    # If error, return some error text, otherwise return a null string
    #
    return retName

#################################################################
#
# Parse Bx Version - get a list of account names, with potential
#                       account names to choose from
#
def parseBxVersion(bxVersion):
    #
    # initialize return values
    #
    sversion = ""
    smajor = ""
    sminor = ""
    version = 0
    major = 0
    minor = 0
    #
    # Take input text stream - and parse it via regex
    #
    # Looking to parse like this : bx version <version>.<major>.<minor>+other text
    #
    metaVersion = re.search(r'version\s*([\d.]+)',bxVersion).group(1)
    (sversion, smajor, sminor) = metaVersion.split('.')
    #
    # Convert to integers
    #
    version = int(sversion)
    major = int(smajor)
    minor = int(sminor)
    #
    # Return list of version major and minor release codes
    #
    return (version, major, minor)


#################################################################
#
# IBMCloudLogin - Log into the IBM Cloud
#
def IBMCloudLogin(user,pw,token):
    flag = True
    badVersion = "This script supports IBM Cloud CLI version 0.6.5 only."
    #
    # See if the Bluemix CLI is installed
    #
    cmd = "bx --version"
    errout = ExecCmd_Output(cmd)
    #
    # Check version of IBM Cloud CLI
    #
    (version,major,minor) = parseBxVersion(errout)
    #
    # Error message and flag if not supported version
    #
    if ((version != 0) or (major != 6) or (minor != 5)):
        print ("ERROR - " + str(badVersion))
        MyLogging("ERROR - " + str(badVersion) + "\n Current version is - " + str(version) + "." + str(major) + "." + str(minor))
        flag = False
    #
    # Log into the IBM Cloud - First set API endpoint
    #
    cmd = "bx api $API_ENDPOINT"
    errout = ExecCmd_Output(cmd)
    #
    # Log into IBM Cloud with either token or username/pw
    #
    if (cloudToken == ""):
        cmd = "bx login -u " + str(cloudUser) + " -p " + str(cloudPwd)
    else:
        cmd = "bx login --apikey @" + str(cloudToken)
    #
    errout = ExecCmd_Output(cmd)
    #
    # Check login success
    #
    if (("ERROR (ExecCmd_Output)" in errout) or (errout == "")):
        flag = False
    else:
        #
        # Set current env values
        #
        findDefaults()
    #
    return flag

#################################################################
#
# buildDataFrame - Read an input CSV file, return a dataframe of the CSV file
#
def buildDataFrame(inpCSVFile):
    #
    # See https://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html#pandas.read_csv
    # for details on the Pandas read_csv function
    #
    df = pd.read_csv(inpCSVFile)
    #
    # If debug flag is on, show first row of data frame in the output logfile
    #
    if (DEBUG):
        for r in df.itertuples():
            if (r.Index == 0):
                outputLog.write("\n** For " + str(inpCSVFile) + "\n** First Frame Record => " + str(r) + "\n\n")
    #
    return df

#################################################################
#
# Get User Options - take a list of potential options, and ask the user
#                   to select one.  Return the value of the selected option,
#                   or an empty string if no valid selection is made
#
def getUserOptions(myList, myTitle):
    #
    # If title prompt exists, print it
    #
    if (myTitle != ""):
        thisLine = myTitle + "\n"
        print (thisLine)
    #
    # Take input list - and present it as options
    #
    idx = 0
    for eachOption in myList:
        #
        # print an option number and value for each option
        #
        idx = idx + 1
        thisLine = str(idx) + ") " + str(eachOption)
        print (thisLine)
    #
    # Have user choose one
    #
    choice = raw_input("Please make a choice -> ")
    #
    # Convert user input - if you get an exception due to input out of range or non-numeric
    # then exception will get raised and we'll catch it and return a null string
    #
    try:
        tmpValue = int(choice)
        retValue = myList[tmpValue-1]
    except:
        retValue = ""
    #
    # Return list element chosen, otherwise return a null string
    #
    return retValue

#################################################################
#
# Set Region - set the CF region of the IBM Cloud session
#
def setRegion(newRegion):
    #
    # Run the IBM Cloud command to set the region
    #
    cmd = "bx target -r " + newRegion
    errout = ExecCmd_Output(cmd)
    #
    # Repopulate current settings
    #
    findDefaults()
    #
    return


#################################################################
#
# Parse Account Names - get a list of account names, with potential
#                       account names to choose from
#
def parseAccountNames(myList):
    #
    # initialize return array
    #
    retValue = []
    lineNum = 0
    #
    # Take input text stream - and process it line by line
    #
    for eachLine in myList.split('\n'):
        lineNum = lineNum + 1
        #
        # Skip the first three lines
        #
        if (lineNum > 3):
            #
            # Check the first array element - see if it is 33 consectutive characters long
            #
            candidateGUID = eachLine[0:32]
            if (candidateGUID != ""):
                #
                # If we have a GUID, get the associated "screen name" for the account
                #
                candidateName = str(eachLine[35:62]) + "(" + str(candidateGUID) + ")"
                #
                # Store as the next entry in your list
                #
                retValue = retValue + [candidateName]
    #
    # Return list of valid GUID's and account names
    #
    return retValue

#################################################################
#
# Parse Account Orgs -  get a list of account org names, with potential
#                       aorg names to choose from
#
def parseAccountOrgs(myList):
    #
    # initialize return array
    #
    retValue = []
    lineNum = 0
    #
    # Take input text stream - and process it line by line
    #
    for eachLine in myList.split('\n'):
        lineNum = lineNum + 1
        #
        # Skip the first three lines
        #
        if (lineNum > 5):
            #
            # Check the first array element - see if it is 33 consectutive characters long
            #
            candidateList = eachLine.split()
            if (candidateList != []):
                #
                # If we have an org, store as the next entry in your list
                #
                candidateOrg = candidateList[0]
                retValue = retValue + [candidateOrg]
    #
    # Return list of valid GUID's and account names
    #
    return retValue

#################################################################
#
# Parse Account Spaces -  get a list of account space names, with potential
#                       space names to choose from
#
def parseAccountSpaces(myList):
    #
    # initialize return array
    #
    retValue = []
    lineNum = 0
    #
    # Take input text stream - and process it line by line
    #
    for eachLine in myList.split('\n'):
        lineNum = lineNum + 1
        #
        # Skip the first three lines
        #
        if (lineNum > 4):
            #
            # Check the first array element - see if it is 33 consectutive characters long
            #
            candidateList = eachLine.split()
            if (candidateList != []):
                #
                # If we have an org, store as the next entry in your list
                #
                candidateSpace = candidateList[0]
                retValue = retValue + [candidateSpace]
    #
    # Return list of valid space names
    #
    return retValue

#################################################################
#
# Parse Group Spaces -  get a list of account resource group names,
#                       with potential group names to choose from
#
def parseGroupSpaces(myList):
    #
    # initialize return array
    #
    retValue = []
    lineNum = 0
    #
    # Take input text stream - and process it line by line
    #
    for eachLine in myList.split('\n'):
        lineNum = lineNum + 1
        #
        # Skip the first three lines
        #
        if (lineNum > 3):
            #
            # Check the first array element - see if it is 33 consectutive characters long
            #
            candidateList = eachLine.split()
            if (candidateList != []):
                #
                # If we have an org, store as the next entry in your list
                #
                candidateSpace = candidateList[0]
                retValue = retValue + [candidateSpace]
    #
    # Return list of valid space names
    #
    return retValue

#################################################################
#
# ProcessAccountUsers -  process the text account user summary info, and
#                       dump a series of CSV file rows to a data file
#
def processAcctUsers(csvoutfile,txtout):
    #writeCSVDetailRecord(csvoutfile, 'Account ID','User ID','Acct. State','Acct. Role','Organization','Space','Org Manager','Org Billing Manager','Org Auditor','Space Manager','Space Developer','Space Auditor')
    #
    # initialize
    #
    stat = ""
    linenum = 1
    tmpAcctId = ""
    tmpUserID = ""
    tmpAcctState = ""
    tmpAcctRole = ""
    tmpOrg = ""
    tmpSpace = ""
    tmpOrgMgr = ""
    tmpOrgBillMgr = ""
    tmpOrgAuditor = ""
    tmpSpaceMgr = ""
    tmpSpaceDev = ""
    tmpSpaceAud = ""
    #
    # Take input text - and process it line by line
    #
    for lines in txtout.splitlines():
        #
        # If first line - then grab the account ID
        #
        if (linenum == 1):
            #
            # Account ID is characters 29 thru 60
            #
            tmpAcctId = lines[28:60]
        #
        # If second line or third line then skip it
        #
        # If fourth line or more, then we have user information
        #
        if (linenum > 3):
            #
            # Grab user ID, Accoutn state and Account role, all split by whitespace
            #
            (tmpUserID,tmpAcctState,tmpAcctRole) = lines.split()
            #
            # Dump entry to CSV file
            #
            stat = writeCSVDetailRecord(csvoutfile,tmpAcctId,tmpUserID,tmpAcctState,tmpAcctRole,tmpOrg,tmpSpace,tmpOrgMgr,tmpOrgBillMgr, tmpOrgAuditor,tmpSpaceMgr,tmpSpaceDev,tmpSpaceAud)
        #
        # Get next line
        #
        linenum = linenum + 1
    #
    # Return status
    #
    return stat

#################################################################
#
# ProcessAccountOrgs -  process the text org user summary info, and
#                       dump a series of CSV file rows to a data file
#
def processAcctOrgs(csvoutfile,org):
    #writeCSVDetailRecord(csvoutfile, 'Account ID','User ID','Acct. State','Acct. Role','Organization','Space','Org Manager','Org Billing Manager','Org Auditor','Space Manager','Space Developer','Space Auditor')
    global envAccount
    #
    # initialize
    #
    stat = ""
    linenum = 1
    tmpAcctId = envAccount
    tmpUserID = ""
    tmpAcctState = ""
    tmpAcctRole = ""
    tmpOrg = org
    tmpSpace = ""
    tmpOrgMgr = ""
    tmpOrgBillMgr = ""
    tmpOrgAuditor = ""
    tmpSpaceMgr = ""
    tmpSpaceDev = ""
    tmpSpaceAud = ""
    #
    # Set up user array and roles array
    #
    tmpOrgMgrDict = {}
    tmpOrgBillMgrDict = {}
    tmpOrgAuditorDict = {}
    #
    #
    #
    orgMgrFlag = False
    orgBillMgrFlag = False
    orgAuditorFlag = False
    #
    # Run the command to show all orgs
    #
    cmd = "bx account org-users " + str(org)
    txtout = ExecCmd_Output(cmd)
    #
    # Parse the returned data
    #
    # Take input text - and process it line by line
    #
    for lines in txtout.splitlines():
        #
        # Strip all whitespace at end of line
        #
        thisLine = lines.rstrip()
        #
        # If line has "MANAGERS" title, flip flag for Org Managers
        #
        if (thisLine.startswith("MANAGERS")):
            #
            # Flip flag for Org Managers
            #
            orgMgrFlag = True
        #
        # If line has "MANAGERS" title, flip flag for Org Billing Managers
        #
        if (thisLine.startswith("BILLING MANAGERS")):
            #
            # Flip flag for Org Managers, and Billing Managers
            #
            orgMgrFlag = False
            orgBillMgrFlag = True
        #
        # If line has "AUDITORS" title, flip flag for Org Auditor
        #
        if (thisLine.startswith("AUDITOR")):
            #
            # Flip flag for Org Managers, and Billing Managers
            #
            orgBillMgrFlag = False
            orgAuditorFlag = True
        #
        # If not a title line, and not a blank line, then we have a user ID
        #
        if ((not (thisLine.startswith("MANAGERS"))) and (not (thisLine.startswith("BILLING MANAGERS"))) and (not (thisLine.startswith("AUDITOR"))) and (not (thisLine == ""))):
            #
            # We have a user ID, store it in the hash
            #
            tmpUserID = thisLine
            #
            # If we're on managers, save TRUE for Org Manager role, and save empty slots
            #
            if (orgMgrFlag):
                tmpOrgMgrDict[tmpUserID] = True
                if (not (tmpUserID in tmpOrgBillMgrDict)):
                    tmpOrgBillMgrDict[tmpUserID] = False
                if (not (tmpUserID in tmpOrgAuditorDict)):
                    tmpOrgAuditorDict[tmpUserID] = False
            #
            # If we're on billing managers, save TRUE for Org Billing Manager role, and save empty slots
            #
            if (orgBillMgrFlag):
                tmpOrgBillMgrDict[tmpUserID] = True
                if (not (tmpUserID in tmpOrgMgrDict)):
                    tmpOrgMgrDict[tmpUserID] = False
                if (not (tmpUserID in tmpOrgAuditorDict)):
                    tmpOrgAuditorDict[tmpUserID] = False
            #
            # If we're on auditors, save TRUE for Org Auditor role, and save empty slots
            #
            if (orgAuditorFlag):
                tmpOrgAuditorDict[tmpUserID] = True
                if (not (tmpUserID in tmpOrgMgrDict)):
                    tmpOrgMgrDict[tmpUserID] = False
                if (not (tmpUserID in tmpOrgBillMgrDict)):
                    tmpOrgBillMgrDict[tmpUserID] = False

    #
    # Cycle through dictionaries and dump data to CSV
    #
    for tmpUserID in tmpOrgMgrDict:
        #
        # Assign values
        #
        tmpOrgMgr = str(tmpOrgMgrDict[tmpUserID])
        tmpOrgBillMgr = str(tmpOrgBillMgrDict[tmpUserID])
        tmpOrgAuditor = str(tmpOrgAuditorDict[tmpUserID])
        #
        # Dump entry to CSV file
        #
        stat = writeCSVDetailRecord(csvoutfile,tmpAcctId,tmpUserID,tmpAcctState,tmpAcctRole,tmpOrg,tmpSpace,tmpOrgMgr,tmpOrgBillMgr, tmpOrgAuditor,tmpSpaceMgr,tmpSpaceDev,tmpSpaceAud)

    #
    # Return status
    #
    return stat

#################################################################
#
# ProcessAccountSpaces -  process the text space user summary info, and
#                         dump a series of CSV file rows to a data file
#
def processAcctSpaces(csvoutfile,org,space):
    #writeCSVDetailRecord(csvoutfile, 'Account ID','User ID','Acct. State','Acct. Role','Organization','Space','Org Manager','Org Billing Manager','Org Auditor','Space Manager','Space Developer','Space Auditor')
    global envAccount
    #
    # initialize
    #
    stat = ""
    linenum = 1
    tmpAcctId = envAccount
    tmpUserID = ""
    tmpAcctState = ""
    tmpAcctRole = ""
    tmpOrg = org
    tmpSpace = space
    tmpOrgMgr = ""
    tmpOrgBillMgr = ""
    tmpOrgAuditor = ""
    tmpSpaceMgr = ""
    tmpSpaceDev = ""
    tmpSpaceAud = ""
    #
    # Set up user array and roles array
    #
    tmpSpaceMgrDict = {}
    tmpSpaceDevDict = {}
    tmpSpaceAuditorDict = {}
    #
    #
    #
    spaceMgrFlag = False
    spaceDevFlag = False
    spaceAuditorFlag = False
    #
    # Run the command to show all orgs
    #
    cmd = "bx account space-users " + str(org) + " " + str(space)
    txtout = ExecCmd_Output(cmd)
    #
    # Parse the returned data
    #
    # Take input text - and process it line by line
    #
    for lines in txtout.splitlines():
        #
        # Strip all whitespace at end of line
        #
        thisLine = lines.rstrip()
        #
        # If line has "SPACE MANAGERS" title, flip flag for Org Managers
        #
        if (thisLine.startswith("SPACE MANAGERS")):
            #
            # Flip flag for Org Managers
            #
            spaceMgrFlag = True
        #
        # If line has "SPACE DEVELOPER" title, flip flag for Space Developers
        #
        if (thisLine.startswith("SPACE DEVELOPER")):
            #
            # Flip flag for Org Managers, and Billing Managers
            #
            spaceMgrFlag = False
            spaceDevFlag = True
        #
        # If line has "SPACE AUDITORS" title, flip flag for Org Auditor
        #
        if (thisLine.startswith("SPACE AUDITORS")):
            #
            # Flip flag for Org Managers, and Billing Managers
            #
            spaceDevFlag = False
            spaceAuditorFlag = True
        #
        # If not a title line, and not a blank line, then we have a user ID
        #
        if ((not (thisLine.startswith("SPACE MANAGERS"))) and (not (thisLine.startswith("SPACE DEVELOPER"))) and (not (thisLine.startswith("SPACE AUDITORS"))) and (not (thisLine == ""))):
            #
            # We have a user ID, store it in the hash
            #
            tmpUserID = thisLine
            #
            # If we're on managers, save TRUE for Org Manager role, and save empty slots
            #
            if (spaceMgrFlag):
                tmpSpaceMgrDict[tmpUserID] = True
                if (not (tmpUserID in tmpSpaceDevDict)):
                    tmpSpaceDevDict[tmpUserID] = False
                if (not (tmpUserID in tmpSpaceAuditorDict)):
                    tmpSpaceAuditorDict[tmpUserID] = False
            #
            # If we're on billing managers, save TRUE for Org Billing Manager role, and save empty slots
            #
            if (spaceDevFlag):
                tmpSpaceDevDict[tmpUserID] = True
                if (not (tmpUserID in tmpSpaceMgrDict)):
                    tmpSpaceMgrDict[tmpUserID] = False
                if (not (tmpUserID in tmpSpaceAuditorDict)):
                    tmpSpaceAuditorDict[tmpUserID] = False
            #
            # If we're on auditors, save TRUE for Org Auditor role, and save empty slots
            #
            if (spaceAuditorFlag):
                tmpSpaceAuditorDict[tmpUserID] = True
                if (not (tmpUserID in tmpSpaceMgrDict)):
                    tmpSpaceMgrDict[tmpUserID] = False
                if (not (tmpUserID in tmpSpaceDevDict)):
                    tmpSpaceDevDict[tmpUserID] = False

    #
    # Cycle through dictionaries and dump data to CSV
    #
    for tmpUserID in tmpSpaceMgrDict:
        #
        # Assign values
        #
        tmpSpaceMgr = str(tmpSpaceMgrDict[tmpUserID])
        tmpSpaceDev = str(tmpSpaceDevDict[tmpUserID])
        tmpSpaceAud = str(tmpSpaceAuditorDict[tmpUserID])
        #
        # Dump entry to CSV file
        #
        stat = writeCSVDetailRecord(csvoutfile,tmpAcctId,tmpUserID,tmpAcctState,tmpAcctRole,tmpOrg,tmpSpace,tmpOrgMgr,tmpOrgBillMgr, tmpOrgAuditor,tmpSpaceMgr,tmpSpaceDev,tmpSpaceAud)
    
    #
    # Return status
    #
    return stat

#################################################################
#
# ProcessJsonSummary -  process the JSON account summary info, and
#                       dump a series of CSV file rows to a data file
#                       reflecting usage indicated in the JSON account
#                       summary information.
#
def processJsonSummary(jsonout, csvoutfile):
    #
    # initialize
    #
    stat = ""
    tmpAcctId = str(jsonout['Summary']['account_id'].encode('utf-8','ignore'))
    tmpDate = str(jsonout['Usage']['month'].encode('utf-8','ignore'))
    tmpBillable = ""
    tmpType = ""
    tmpResourceID = ""
    tmpName = ""
    tmpUnits = ""
    tmpQuantity = ""
    tmpCost = ""
    #
    # Take input JSON - and process it structure by structure
    #
    #
    # Loop thru all entries
    #
    for resource in jsonout['Usage']['resources']:
        tmpType = ""
        tmpName = str(resource['resource_name'].encode('utf-8','ignore'))
        tmpResourceID = str(resource['resource_id'].encode('utf-8','ignore'))
        #
        for plans in resource['plans']:
            tmpBillable = str(plans['billable'])
            #
            for usagefld in plans['usage']:
                tmpUnits = str(usagefld['unit'].encode('utf-8','ignore'))
                tmpQuantity = str(usagefld['quantity'])
                tmpCost = str(usagefld['cost'])
                #
                # Dump entry to CSV file
                #
                stat = writeCSVSummaryRecord(csvoutfile,tmpAcctId,tmpDate,tmpBillable,tmpType,tmpResourceID,tmpName,tmpUnits,tmpQuantity, tmpCost)
    #
    # Return
    #
    return stat

#################################################################
#
# ProcessJsonDetails -  process the JSON account org details info, and
#                       dump a series of CSV file rows to a data file
#                       reflecting usage indicated in the JSON account
#                       org detail information.
#
def processJsonDetails(jsonout, csvoutfile):
    #
    # initialize
    #
    stat = ""
    tmpAcctId = ""
    tmpDate = str(jsonout['date'].encode('utf-8','ignore'))
    tmpRegion = ""
    tmpOrg = str(jsonout['org'].encode('utf-8','ignore'))
    tmpSpace = ""
    tmpBillable = ""
    tmpType = ""
    tmpResourceID = ""
    tmpName = ""
    tmpUnits = ""
    tmpQuantity = ""
    tmpCost = ""
    # writeCSVDetailRecord (csvoutfile,tmpAcctId,tmpDate,tmpRegion,tmpOrg,tmpSpace,Billable,tmpType,tmpResourceID,tmpName,tmpUnits,tmpQuantity, tmpCost)
    #
    # Take input JSON - and process it structure by structure
    #
    # Loop thru all resources entries
    #
    for myrecs in jsonout['records']:
        tmpAcctId = str(myrecs['account_id'].encode('utf-8','ignore'))
        thisRegion = str(myrecs['organization_id'].encode('utf-8','ignore'))
        (tmpRegion, junk) = thisRegion.split(":")
        #
        # CLI is returning "blanK" entries for details records, and these
        # have null values for spaces.  Jump out when this happens.
        #
        if (myrecs['resources'] is None):
            continue
        #
        for resource in myrecs['resources']:
            tmpResourceID = str(resource['resource_id'].encode('utf-8','ignore'))
            tmpName = str(resource['resource_name'].encode('utf-8','ignore'))
            #
            for plan in resource['plans']:
                tmpBillable = str(plan['billable'])
                tmpSpace = str(plan['plan_name'].encode('utf-8','ignore'))
                tmpType = " "
                #
                for usagefld in plan['usage']:
                    tmpUnits = str(usagefld['metric'].encode('utf-8','ignore'))
                    tmpQuantity = str(usagefld['quantity'])
                    tmpCost = str(usagefld['cost'])
                    #
                    # Dump entry to CSV file
                    #
                    stat = writeCSVDetailRecord(csvoutfile,tmpAcctId,tmpDate,tmpRegion,tmpOrg,tmpSpace,tmpBillable,tmpType,tmpResourceID,tmpName,tmpUnits,tmpQuantity, tmpCost)
    #
    # Return list of valid space names
    #
    return stat


#
# Check choice and make changes based on choice
#
#if ((choice == "w") or (choice =="W") ):
#    bx_add_users_to_acct(userList)
#if ((choice == "x") or (choice =="X") ):
#    bx_add_users_to_acctorg(userList,acctRole)
#if ((choice == "y") or (choice =="Y") ):
#    bx_add_users_to_acct_space(userList,acctRole)
#if ((choice == "z") or (choice =="Z") ):
#    bx_add_users_to_all_spaces(userList,acctRole)

#################################################################
#
# bx_add_users_to_acct -  add each of the input users in list to account with
#                           the general role specified
#
def bx_add_users_to_acct(userList):
    #
    # initialize
    #
    stat = ""
    #
    # Loop thru user list
    #
    for userId in userList:
        #
        # Build command to et access for this user
        #
        cmd = "bx account user-invite " + str(userId)
        errout = ExecCmd_Output(cmd)
        #
        # See if we had an error
        #
        if ((errout == "") or ("FAILED" in errout)):
            #
            # Notify the user of the error condition
            #
            print ("User " + str(userId) + " was not added to account.  Error when adding to account.")
            MyLogging ("User " + str(userId) + " was not added to account.  Error when adding to account.")
    #
    # Return status
    #
    return stat

#################################################################
#
# bx_add_users_to_acct_space -  add each of the input users in list to a specific
#                               org and space with the general role specified
#
def bx_add_users_to_acct_space(userList,acctRole):
    #
    # initialize
    #
    stat = ""
    #
    # Set roles for these users - (either "Admin", "Dev", or "Audit")
    #
    # If "Admin" selected, give full access
    #
    if (acctRole == "Admin"):
        orgRole = "OrgManager"
        spaceRole = "SpaceManager"
    #
    # if "Dev" selected, give developer access (which is BillingManager for org, SpaceDeveloper for Space)
    #
    if (acctRole == "Dev"):
        orgRole = "BillingManager"
        spaceRole = "SpaceDeveloper"
    #
    # if "Audit" selected, give auditor access
    #
    if (acctRole == "Audit"):
        orgRole = "OrgAuditor"
        spaceRole = "SpaceAuditor"
    #
    # Identify the proper org
    #
    #
    # Run the command to show current orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    if (errout != ""):
        #
        # Log the error - unable to hit API endpoint
        #
        MyLogging("ERROR - Unable to run bluemix account orgs command")
    #
    # Parse the accounts provided, returns a list of tuples in (id option) format
    #
    optionList = parseAccountOrgs(errout)
    #
    # Give user options, find out what they want
    #
    newOrg = getUserOptions(optionList,"Select org to assign users to...")
    #
    # Set to the new org
    #
    cmd = "bx target -o " + str(newOrg)
    errout = ExecCmd_Output(cmd)
    #
    # Run the command to show current spaces
    #
    cmd = "bx account spaces"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        MyLogging("ERROR - Unable to run bluemix account spaces command")
    #
    # Parse the spaces provided, returns a list of spaces
    #
    optionList = parseAccountSpaces(errout)
    #
    # Give user options, find out what they want
    #
    if (optionList == []):
        print ("No valid spaces available")
        MyLogging("ERROR - No valid spaces available")
    else:
        newSpace = getUserOptions(optionList,"Select space to assign users to...")
    #
    # Loop thru user list
    #
    for userId in userList:
        #
        # Build command to set org access for this user
        #
        cmd = "bx account org-user-add " + str(userId) + " " + str(newOrg)
        errout = ExecCmd_Output(cmd)
        #
        # Build command to set org role for this user
        #
        cmd = "bx account org-role-set " + str(userId) + " " + str(newOrg) + " " + str(orgRole)
        errout = ExecCmd_Output(cmd)
        #
        # Build command to set space role for this user
        #
        cmd = "bx account space-role-set " + str(userId) + " " + str(newOrg) + " " + str(newSpace) + " " + str(spaceRole)
        errout = ExecCmd_Output(cmd)

    #
    # Return status
    #
    return stat

#################################################################
#
# bx_add_users_to_acctorg -  add each of the input users in list to a specific
#                            org with the general role specified
#
def bx_add_users_to_acctorg(userList,acctRole):
    #
    # initialize
    #
    stat = ""
    #
    # Set roles for these users - (either "Admin", "Dev", or "Audit")
    #
    # If "Admin" selected, give full access
    #
    if (acctRole == "Admin"):
        orgRole = "OrgManager"
    #
    # if "Dev" selected, give developer access (which is BillingManager for org, SpaceDeveloper for Space)
    #
    if (acctRole == "Dev"):
        orgRole = "BillingManager"
    #
    # if "Audit" selected, give auditor access
    #
    if (acctRole == "Audit"):
        orgRole = "OrgAuditor"
    #
    # Identify the proper org
    #
    #
    # Run the command to show current orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        MyLogging("ERROR - Unable to run bluemix account orgs command")
    #
    # Parse the accounts provided, returns a list of tuples in (id option) format
    #
    optionList = parseAccountOrgs(errout)
    #
    # Give user options, find out what they want
    #
    newOrg = getUserOptions(optionList,"Select org to assign users to...")
    #
    # Set to the new org
    #
    cmd = "bx target -o " + str(newOrg)
    errout = ExecCmd_Output(cmd)
    #
    # Loop thru user list
    #
    for userId in userList:
        #
        # Build command to set org access for this user
        #
        cmd = "bx account org-user-add " + str(userId) + " " + str(newOrg)
        errout = ExecCmd_Output(cmd)
        #
        # Build command to set org role for this user
        #
        cmd = "bx account org-role-set " + str(userId) + " " + str(newOrg) + " " + str(orgRole)
        errout = ExecCmd_Output(cmd)
    #
    # Return status
    #
    return stat

#################################################################
#
# bx_add_users_to_all_spaces -  add each of the input users in list to a specific
#                               org and ALL spaces under that org, with the general
#                               role specified
#
def bx_add_users_to_all_spaces(userList,acctRole):
    #
    # initialize
    #
    stat = ""
    #
    # Set roles for these users - (either "Admin", "Dev", or "Audit")
    #
    # If "Admin" selected, give full access
    #
    if (acctRole == "Admin"):
        orgRole = "OrgManager"
        spaceRole = "SpaceManager"
    #
    # if "Dev" selected, give developer access (which is BillingManager for org, SpaceDeveloper for Space)
    #
    if (acctRole == "Dev"):
        orgRole = "BillingManager"
        spaceRole = "SpaceDeveloper"
    #
    # if "Audit" selected, give auditor access
    #
    if (acctRole == "Audit"):
        orgRole = "OrgAuditor"
        spaceRole = "SpaceAuditor"
    #
    # Identify the proper org
    #
    #
    # Run the command to show current orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        MyLogging("ERROR - Unable to run bluemix account orgs command")
    #
    # Parse the accounts provided, returns a list of tuples in (id option) format
    #
    optionList = parseAccountOrgs(errout)
    #
    # Give user options, find out what they want
    #
    newOrg = getUserOptions(optionList,"Select org to assign users to...")
    #
    # Set to the new org
    #
    cmd = "bx target -o " + str(newOrg)
    errout = ExecCmd_Output(cmd)
    #
    # Run the command to show current spaces
    #
    cmd = "bx account spaces"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        MyLogging("ERROR - Unable to run bluemix account spaces command")
    #
    # Parse the spaces provided, returns a list of spaces
    #
    optionList = parseAccountSpaces(errout)
    #
    # Loop thru user list
    #
    for userId in userList:
        #
        # Build command to set org access for this user
        #
        cmd = "bx account org-user-add " + str(userId) + " " + str(newOrg)
        errout = ExecCmd_Output(cmd)
        #
        # Build command to set org role for this user
        #
        cmd = "bx account org-role-set " + str(userId) + " " + str(newOrg) + " " + str(orgRole)
        errout = ExecCmd_Output(cmd)
        #
        # Loop thru every space under this org
        #
        for thisSpace in optionList:
            #
            # Build command to set space role for this user
            #
            cmd = "bx account space-role-set " + str(userId) + " " + str(newOrg) + " " + str(thisSpace) + " " + str(spaceRole)
            errout = ExecCmd_Output(cmd)
    
    #
    # Return status
    #
    return stat


# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu
def main_menu():
    os.system('clear')
    
    print ("Welcome to the BM Cloud Admin tool,")
    print ("Please choose the menu you want to execute:")
    print ("1. Show IBM Cloud context and default settings")
    print ("2. Show All account Orgs")
    print ("3. Show Billing Summary for this month")
    print ("4. Show Billing Detail by Org for this month")
    print ("5. Show Billing Summary for past 12 months")
    print ("6. Show Billing Detail by Org for past 12 months")
    print ("7. Show Account Security Settings for Users")
    print ("8. Add users to Account")
    print ("\n0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    
    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        ch = ""
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
    return

# Show default settings
def show_default():
    print ("Current IBM Cloud Default Settings \n")
    #
    # Show current context
    #
    print ("User:              " + str(envUser))
    print ("Account:           " + str(envAccount))
    print ("API Endpoint:      " + str(envAPIEndpoint))
    print (" ")
    print ("Region:            " + str(envRegion))
    print ("Resource Group:    " + str(envResourceGroup))
    print ("Org:               " + str(envOrg))
    print ("Space:             " + str(envSpace))
    #
    # Print menu bottom
    #
    print (" ")
    print ("D. Modify Defaults")
    print ("9. Back")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Show all account orgs
def bx_account_orgs():
    print ("Showing all account orgs \n")
    #
    # Run the command to show all orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    #
    # Parse the accounts provided, returns a list of orgs
    #
    optionList = parseAccountOrgs(errout)
    #
    # Loop thru entries in org list
    #
    for eachOption in optionList:
        #
        # print an option number and value for each option
        #
        print (str(eachOption))
    print ("\n")
    #
    # Print menu bottom
    #
    print ("9. Back")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Get billing summary
def bx_billing_summary(datestr,jsonflag):
    #
    # Run the command to show all orgs
    #
    if jsonflag:
        cmd = "bx billing account-usage -d " + str(datestr) + " --json"
    else:
        cmd = "bx billing account-usage -d " + str(datestr)
    #
    # Execute command
    #
    errout = ExecCmd_Output(cmd)
    #
    # Just return results
    #
    return errout

# Get account users
def bx_account_users():
    #
    # Run the command to show all users
    #
    cmd = "bx  account users"
    #
    # Execute command
    #
    errout = ExecCmd_Output(cmd)
    #
    # Just return results
    #
    return errout

# Show all account orgs
def bx_billing_detail(orgname,datestr,jsonflag):
    #
    # Run the command to show all orgs
    #
    if jsonflag:
        cmd = "bx billing org-usage " + str(orgname) + " -d " + str(datestr) + " --json"
    else:
        cmd = "bx billing org-usage " + str(orgname) + " -d " + str(datestr)
    #
    # Execute command
    #
    errout = ExecCmd_Output(cmd)
    #
    # Just return results
    #
    return errout

# Show billing summary
def show_billing_summary():
    print ("Building current billing summary \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_billing_summary.txt"
    outfile = openTextFile(filename)
    #
    # Run the command to show all orgs
    #
    errout = bx_billing_summary(todaystr,False)
    #
    # Just dump output
    #
    writeTextFile(outfile,"")
    writeTextFile(outfile,errout)
    writeTextFile(outfile,"")
    #
    closeTextFile(outfile)
    #
    # Tell user where to find the file
    #
    print ("")
    print ("Current billing summary in file -> " + str(filename))
    print ("")
    #
    # Print menu bottom
    #
    print ("9. Back")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Show billing summary - output in json
def show_billing_summary_json():
    print ("Building current billing summary (in JSON) \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_billing_summary.json"
    outfile = openTextFile(filename)
    #
    # Open CSV file and Write CSV file column headeings
    #
    csvfilename = str(shortAcctName()) + "_billing_summary.csv"
    csvoutfile = openCsvFile(csvfilename)
    writeCSVSummaryRecord(csvoutfile, 'Account ID','Date','Billable','Type','Resource ID','Name','Units','Quantity','Cost')
    #
    # Run the command to show all orgs
    #
    errout = bx_billing_summary(todaystr,True)
    #
    # Just dump output to json file
    #
    writeTextFile(outfile,errout)
    #
    # Store json in a data structure - we'll dig into it later
    #
    jsonout = json.loads(errout)
    #
    # Add in a date field
    #
    jsonout['date'] = str(todaystr)
    #
    # Process JSON account summary data
    #
    processJsonSummary(jsonout, csvoutfile)
    #
    closeTextFile(outfile)
    #
    # Tell user where to find the file
    #
    print ("")
    print ("Current billing summary in file -> " + str(filename))
    print ("Current billing summary in file -> " + str(csvfilename))
    print ("")
    #
    # See if this is a batch session
    #
    if cloudBilling:
        #
        # Batch session, just return
        #
        return
    else:
        #
        # Interactive session, print menu bottom
        #
        print ("9. Back")
        print ("0. Quit")
        choice = raw_input(" >>  ")
        exec_menu(choice)
        return

# Show all account orgs
def show_billing_detail():
    print ("Building current billing details by org \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_billing_by_org.txt"
    outfile = openTextFile(filename)
    #
    # Run the command to show all orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    #
    # Parse the accounts provided, returns a list of orgs
    #
    optionList = parseAccountOrgs(errout)
    #
    # Loop thru entries in org list
    #
    for eachOption in optionList:
        #
        # Run the command to show org usage
        #
        errout = bx_billing_detail(str(eachOption),todaystr,False)
        #
        # Just dump output
        #
        writeTextFile(outfile,"\n")
        writeTextFile(outfile,"======================================================================\n")
        writeTextFile(outfile,"======================================================================\n")
        writeTextFile(outfile,"= Billing details for " + str(eachOption) + "\n")
        writeTextFile(outfile,"======================================================================\n")
        writeTextFile(outfile,errout)
        writeTextFile(outfile,"\n")
    #
    # Tell user where to find the file
    #
    closeTextFile(outfile)
    print ("")
    print ("Current billing details in file -> " + str(filename))
    print ("")
    #
    # Print menu bottom
    #
    print ("9. Back")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Show billing details - output in json
def show_billing_detail_json():
    global todaystr
    print ("Building current billing details by org (in JSON) \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_billing_by_org.json"
    outfile = openTextFile(filename)
    #
    # Open CSV file and Write CSV file column headeings
    #
    csvfilename = str(shortAcctName()) + "_billing_by_org.csv"
    csvoutfile = openCsvFile(csvfilename)
    writeCSVDetailRecord(csvoutfile, 'Account ID','Date','Region','Org','Space','Billable','Type','Resource ID','Name','Units','Quantity','Cost')
    #
    # Run the command to show all orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    #
    # Parse the accounts provided, returns a list of orgs
    #
    optionList = parseAccountOrgs(errout)
    firstLine = True
    #
    # Loop thru entries in org list
    #
    for eachOption in optionList:
        #
        # Run the command to show org usage
        #
        fixout = bx_billing_detail(str(eachOption),todaystr,True)
        #
        # Add org name and date
        #
        errout = "{ \"org\": \"" + str(eachOption) + "\",\n  \"date\": \"" + str(todaystr) + "\",\n  \"records\": " + fixout + "} \n"
        #
        # Just dump output to json file
        #
        if firstLine:
            writeTextFile(outfile,errout)
            firstLine = False
        else:
            #
            # Need to split up the JSON elements with commas
            #
            fixedout = ",\n" + errout
            writeTextFile(outfile,fixedout)
        #
        # Store json in a data structure - we'll dig into it later
        #
        jsonout = json.loads(errout)
        #
        # Process JSON account details data
        #
        processJsonDetails(jsonout, csvoutfile)
    #
    # Close the output
    #
    closeTextFile(outfile)
    #
    # Tell user where to find the file
    #
    print ("")
    print ("Current billing details in file -> " + str(filename))
    print ("Current billing details in file -> " + str(csvfilename))
    print ("")
    #
    return

# Show billing summary - output in json
def show_annual_billing_detail_json():
    global todaystr
    print ("Building current ANNUAL billing details by org (in JSON) \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_annual_billing_by_org.json"
    outfile = openTextFile(filename)
    #
    # Open CSV file and Write CSV file column headeings
    #
    csvfilename = str(shortAcctName()) + "_annual_billing_by_org.csv"
    csvoutfile = openCsvFile(csvfilename)
    writeCSVDetailRecord(csvoutfile, 'Account ID','Date','Region','Org','Space','Billable','Type','Resource ID','Name','Units','Quantity','Cost')
    #
    # Run the command to show all orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    #
    # Parse the accounts provided, returns a list of orgs
    #
    optionList = parseAccountOrgs(errout)
    firstLine = True
    #
    # Loop thru entries in org list
    #
    for eachOption in optionList:
        #
        # Loop thru past 12 months
        #
        currdate = todaystr
        for months in range(12):
            #
            # Run the command to show org usage
            #
            fixout = bx_billing_detail(str(eachOption),currdate,True)
            #
            # Check for error messages (happens when looking for history that doesn't exist)
            #
            if ((fixout == "") or ("FAILED" in fixout)):
                #
                # Notify the user of the potential error condition
                #
                MyLogging ("Error pulling billing data for " + str(currdate) + ".")
                continue
            #
            # Add org name and date
            #
            errout = "{ \"org\": \"" + str(eachOption) + "\",\n  \"date\": \"" + str(currdate) + "\",\n  \"records\": " + fixout + "} \n"
            #
            # Just dump output to json file
            #
            if firstLine:
                writeTextFile(outfile,errout)
                firstLine = False
                #
                fixedout = ""
            else:
                #
                # Need to split up the JSON elements with commas
                #
                fixedout = ",\n" + errout
                writeTextFile(outfile,fixedout)
            #
            # Store json in a data structure - we'll dig into it later
            #
            jsonout = json.loads(errout)
            #
            # Process JSON account details data
            #
            processJsonDetails(jsonout, csvoutfile)
            #
            # Change date to previous month
            #
            currdate = getPrevMonth(currdate)
            # End loop thru months
        # end loop thru account orgs
    #
    # Close the output
    #
    closeTextFile(outfile)
    #
    # Tell user where to find the file
    #
    print ("")
    print ("Current annual billing details in file -> " + str(filename))
    print ("Current annual billing details in file -> " + str(csvfilename))
    print ("")
    #
    # See if this is a batch session
    #
    return

# Show billing summary - output in json and csv
def show_account_security():
    print ("Building current account security report \n")
    #
    # Open CSV file and Write CSV file column headeings
    #
    csvfilename = str(shortAcctName()) + "_account_security.csv"
    csvoutfile = openCsvFile(csvfilename)
    writeCSVDetailRecord(csvoutfile, 'Account ID','User ID','Acct. State','Acct. Role','Organization','Space','Org Manager','Org Billing Manager','Org Auditor','Space Manager','Space Developer','Space Auditor')
    #
    # Get overall account settings
    #
    errout = bx_account_users()
    if ("ERROR" not in errout):
        processAcctUsers(csvoutfile,errout)
    #
    # Run the command to show all orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    #
    # Parse the accounts provided, returns a list of orgs
    #
    orgList = parseAccountOrgs(errout)
    #
    # Loop thru entries in org list
    #
    for eachOrg in orgList:
        #
        # Process the users and roles for this org
        #
        stat = processAcctOrgs(csvoutfile,eachOrg)
        #
        # Loop through each space in the org, get a list of them
        #
        cmd = "bx account spaces -o " + str(eachOrg)
        errout = ExecCmd_Output(cmd)
        #
        # Parse the accounts provided, returns a list of spaces
        #
        spaceList = parseAccountSpaces(errout)
        #
        # Loop through each space in the list
        #
        for eachSpace in spaceList:
            #
            # Process the users and roles for this space
            #
            stat = processAcctSpaces(csvoutfile,eachOrg,eachSpace)
    #
    # End loop thru spaces , and end loop through orgs
    #
    # Tell user where to find the file
    #
    print ("")
    print ("Current account security in file -> " + str(csvfilename))
    print ("")
    #
    # See if this is a batch session
    #
    return

# Show billing summary - output in json and csv
def show_annual_billing_summary_json():
    global todaystr
    print ("Building current ANNUAL billing summary (in JSON) \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_annual_billing_summary.json"
    outfile = openTextFile(filename)
    #
    # Open CSV file and Write CSV file column headeings
    #
    csvfilename = str(shortAcctName()) + "_annual_billing_summary.csv"
    csvoutfile = openCsvFile(csvfilename)
    writeCSVSummaryRecord(csvoutfile, 'Account ID','Date','Billable','Type','Resource ID','Name','Units','Quantity','Cost')
    #
    # Loop thru past 12 months
    #
    currdate = todaystr
    for months in range(12):
        #
        # Run for current date
        #
        errout = bx_billing_summary(currdate,True)
        #
        # Just dump output to json file
        #
        writeTextFile(outfile,errout)
        #
        # Store json in a data structure - we'll dig into it next
        #
        jsonout = json.loads(errout)
        #
        # Add in a date field
        #
        jsonout['date'] = str(currdate)
        #
        # Process JSON account summary data
        #
        processJsonSummary(jsonout, csvoutfile)
        #
        # Change date to previous month
        #
        currdate = getPrevMonth(currdate)
    # End loop thru months
    #
    closeTextFile(outfile)
    #
    # Tell user where to find the file
    #
    print ("")
    print ("Current billing summary in file -> " + str(filename))
    print ("Current billing summary in file -> " + str(csvfilename))
    print ("")
    #
    # See if this is a batch session
    #
    return

def bx_modify_group():
    print ("Current IBM Cloud Resource Groups \n")
    #
    # Run the command to show current accounts
    #
    cmd = "bx resource groups"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        outputLog.write("ERROR - Unable to run bluemix account spaces command")
    #
    # Parse the spaces provided, returns a list of spaces
    #
    optionList = parseGroupSpaces(errout)
    #
    # Give user options, find out what they want
    #
    if (optionList == []):
        print ("No valid resource groups available")
        outputLog.write("ERROR - No valid resource groups available")
    else:
        newGroup = getUserOptions(optionList,"Select a resource group to associate with...")
        #
        # Update account
        #
        cmd = "bx target -g " + str(newGroup)
        errout = ExecCmd_Output(cmd)
    #
    # Set current env values
    #
    findDefaults()
    #
    return

#
# Modify account users
#
def add_users_to_account():
    print ("Current IBM Cloud Default Settings \n")
    #
    # Show current context
    #
    print ("User:              " + str(envUser))
    print ("Account:           " + str(envAccount))
    print ("API Endpoint:      " + str(envAPIEndpoint))
    print (" ")
    print ("Region:            " + str(envRegion))
    print ("Resource Group:    " + str(envResourceGroup))
    print ("Org:               " + str(envOrg))
    print ("Space:             " + str(envSpace))
    #
    # Get input CSV file of users
    #
    userList = getUserCsvFile()
    if (userList == []):
        #
        # Give an error message
        #
        print ("")
        print ("ERROR - Unable to process CSV file")
        print ("")
        choice = raw_input("Hit return to continue....")
        MyLogging("ERROR - Unable to process CSV file - Empty user list\n")
        return
    MyLogging("USER LIST is -" + str(userList) + "-\n")
    #
    # Ask for the right context to add users
    #
    noGoodInput = True
    acctRole = ""
    while (noGoodInput):
        os.system('clear')
        print ("Modifying user access and permissions on the IBM Cloud\n")
        print ("Please choose the action that you want to execute:")
        print ("W. Add users to the account")
        print ("X. Add users to the account and a specific Org")
        print ("Y. Add users to the account and a specific space under a specific Org")
        print ("Z. Add users to the account under ALL spaces under a specific Org")
        print ("\n9. Back to Main Menu")
        choice = raw_input(" >>  ")
        if (choice == "9"):
            # Fall through - go back to main menu
            noGoodInput = False
        if (choice in ("x","X","y","Y","z","Z")):
            #
            # Ask for the right context to add users
            #
            print ("\nWhat type of role would you like assigned?\n")
            print ("Please choose the general role that you want to assign:")
            print ("J. Add users in Superuser or Admin role")
            print ("K. Add users in Developer or Contributor role")
            print ("L. Add users in an audit or monitor role")
            perms = raw_input(" >>  ")
            #
            if (perms in ("j","J")):
                noGoodInput = False
                acctRole = "Admin"
            if (perms in ("k","K")):
                noGoodInput = False
                acctRole = "Dev"
            if (perms in ("l","L")):
                noGoodInput = False
                acctRole = "Audit"
            # end if
        if (choice in ("w","W")):
            noGoodInput = False
        # end while - get inputs again
    #
    # Check choice and make changes based on choice
    #
    if ((choice == "w") or (choice =="W") ):
        bx_add_users_to_acct(userList)
    if ((choice == "x") or (choice =="X") ):
        bx_add_users_to_acct(userList)
        bx_add_users_to_acctorg(userList,acctRole)
    if ((choice == "y") or (choice =="Y") ):
        bx_add_users_to_acct(userList)
        bx_add_users_to_acct_space(userList,acctRole)
    if ((choice == "z") or (choice =="Z") ):
        bx_add_users_to_acct(userList)
        bx_add_users_to_all_spaces(userList,acctRole)
    #
    return

def bx_modify_account():
    print ("Current IBM Cloud Accounts \n")
    #
    # Run the command to show current accounts
    #
    cmd = "bx account list"
    errout = ExecCmd_Output(cmd)
    #
    # Parse the accounts provided, returns a list of tuples in (id option) format
    #
    optionList = parseAccountNames(errout)
    #
    # Give user options, find out what they want
    #
    newAcct = getUserOptions(optionList,"Select account to associate with...")
    newGUID = str(newAcct[28:60])
    #
    # Check if login was via APIKEY, if so, then we cannot switch context
    #
    if (cloudToken == ""):
        #
        # Update account
        #
        cmd = "bx target -c " + str(newGUID)
        errout = ExecCmd_Output(cmd)
    else:
        #
        # Give an error message
        #
        print ("")
        print ("You cannot switch accounts when using an API token to log into the IBM Cloud")
        print ("")
        choice = raw_input("Hit return to continue....")
    #
    # Set current env values
    #
    findDefaults()
    #
    # Print menu
    #
    choice = ""
    exec_menu(choice)
    return

def bx_modify_org():
    print ("Current IBM Cloud Orgs \n")
    #
    # Run the command to show current orgs
    #
    cmd = "bx account orgs"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        outputLog.write("ERROR - Unable to run bluemix account orgs command")
    #
    # Parse the accounts provided, returns a list of tuples in (id option) format
    #
    optionList = parseAccountOrgs(errout)
    #
    # Give user options, find out what they want
    #
    newOrg = getUserOptions(optionList,"Select org to associate with...")
    #
    # Update account
    #
    cmd = "bx target -o " + str(newOrg)
    errout = ExecCmd_Output(cmd)
    #
    # Set current env values
    #
    findDefaults()
    #
    # Print menu
    #
    choice = ""
    exec_menu(choice)
    return

def bx_modify_region():
    print ("Current IBM Cloud Regions \n")
    #
    # Give user options, find out what they want
    #
    newRegion = getUserOptions(REGION_LIST,"Select region to associate with...")
    #
    # Update account
    #
    cmd = "bx target -r " + str(newRegion)
    errout = ExecCmd_Output(cmd)
    #
    # Set current env values
    #
    findDefaults()
    #
    # Print menu
    #
    choice = ""
    exec_menu(choice)
    return

def bx_modify_space():
    print ("Current IBM Cloud Spaces \n")
    #
    # Run the command to show current accounts
    #
    cmd = "bx account spaces"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        outputLog.write("ERROR - Unable to run bluemix account spaces command")
    #
    # Parse the spaces provided, returns a list of spaces
    #
    optionList = parseAccountSpaces(errout)
    #
    # Give user options, find out what they want
    #
    if (optionList == []):
        print ("No valid spaces available")
        outputLog.write("ERROR - No valid spaces available")
    else:
        newSpace = getUserOptions(optionList,"Select space to associate with...")
        #
        # Update account
        #
        cmd = "bx target -s " + str(newSpace)
        errout = ExecCmd_Output(cmd)
    #
    # Set current env values
    #
    findDefaults()
    #
    # Print menu
    #
    choice = ""
    exec_menu(choice)
    return

def bx_modify_group():
    print ("Current IBM Cloud Resource Groups \n")
    #
    # Run the command to show current accounts
    #
    cmd = "bx resource groups"
    errout = ExecCmd_Output(cmd)
    if (errout == ""):
        #
        # Log the error - unable to hit API endpoint
        #
        outputLog.write("ERROR - Unable to run bluemix account spaces command")
    #
    # Parse the spaces provided, returns a list of spaces
    #
    optionList = parseGroupSpaces(errout)
    #
    # Give user options, find out what they want
    #
    if (optionList == []):
        print ("No valid resource groups available")
        outputLog.write("ERROR - No valid resource groups available")
    else:
        newGroup = getUserOptions(optionList,"Select a resource group to associate with...")
        #
        # Update account
        #
        cmd = "bx target -g " + str(newGroup)
        errout = ExecCmd_Output(cmd)
    #
    # Set current env values
    #
    findDefaults()
    #
    # Print menu
    #
    choice = ""
    exec_menu(choice)
    return

def bx_modify_defaults():
    print ("Current IBM Cloud Default Settings \n")
    #
    # Show current context
    #
    print ("User:              " + str(envUser))
    print ("Account:           " + str(envAccount))
    print ("API Endpoint:      " + str(envAPIEndpoint))
    print (" ")
    print ("Region:            " + str(envRegion))
    print ("Resource Group:    " + str(envResourceGroup))
    print ("Org:               " + str(envOrg))
    print ("Space:             " + str(envSpace))
    #
    # Print menu bottom
    #
    print (" ")
    print ("A. Modify Default Account")
    print ("R. Modify Default Region")
    print ("O. Modify Default Org")
    print ("S. Modify Default Space")
    print ("G. Modify Resource Group")
    print ("9. Back")
    print ("0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return

# Back to main menu
def back():
    UserExit = False

# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    '1': show_default,
    '2': bx_account_orgs,
    '3': show_billing_summary_json,
    '4': show_billing_detail_json,
    '5': show_annual_billing_summary_json,
    '6': show_annual_billing_detail_json,
    '7': show_account_security,
    '8': add_users_to_account,
    'A': bx_modify_account,
    'D': bx_modify_defaults,
    'G': bx_modify_group,
    'O': bx_modify_org,
    'R': bx_modify_region,
    'S': bx_modify_space,
    'a': bx_modify_account,
    'd': bx_modify_defaults,
    'g': bx_modify_group,
    'o': bx_modify_org,
    'r': bx_modify_region,
    's': bx_modify_space,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    #
    # Log into the IBM Cloud
    #
    stat = IBMCloudLogin(cloudUser,cloudPwd,cloudToken)
    UserExit = False
    #
    # Check login status
    #
    if (stat):
        #
        # Launch main menu
        #
        if cloudBilling:
            #
            # Run non-interactive, do billing
            #
            show_annual_billing_detail_json()
        if cloudSecurity:
            #
            # Run non-interactive, do security
            #
            show_account_security()
        if (not (cloudBilling or cloudSecurity)):
            #
            # Run an interactive session
            #
            while (not UserExit):
                main_menu()
    else:
        print ("ERROR - Invalid login - Error during IBM Cloud login")
        outputLog.write("ERROR - Invalid login - Error during IBM Cloud login")

