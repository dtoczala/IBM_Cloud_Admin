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

parser = argparse.ArgumentParser()

parser.add_argument("-u","--userID",required=False,help="User IBM Cloud ID")
parser.add_argument("-p","--pwd",required=False,help="User IBM Cloud password")
parser.add_argument("-t","--token",required=False,help="IBM Cloud Token")
#
# Grab the arguments off the command line
#
errorFound = False
args = parser.parse_args()
cloudUser = args.userID
cloudPwd = args.pwd
cloudToken = args.token

#
# Output debugging data
#
if (DEBUG):
    outputLog.write("User ID is - " + str(cloudUser) + "\n")
    outputLog.write("User password is - " + str(cloudPwd) + "\n")
    outputLog.write("Tokens is - " + str(cloudToken) + "\n\n")
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
        subprocess.call(cmd,shell=True)
        MyLogging("COMMAND -> " + cmd)
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
        cmdout = subprocess.check_output(cmd,shell=True)
        MyLogging("COMMAND -> " + cmd)
        MyLogging("OUTPUT  -> " + cmdout)
    except:
        tmpout = "ERROR (ExecCmd_Output) - on call -> " + str(cmd) + "\n"
        outputLog.write(tmpout)
        errout = str(errout) + " "
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
# Check for proper version of python
#
def openTextFile(filename):
    #
    # Set the global name and filehandle
    #
    textFile = open(filename, "w")
    return textFile

#################################################################
#
# Check for proper version of python
#
def writeTextFile(textfile,txtline):
    #
    # Set the global name and filehandle
    #
    stat = textfile.write(txtline)
    return stat

#################################################################
#
# Check for proper version of python
#
def closeTextFile(textfile):
    #
    # Set the global name and filehandle
    #
    stat = textfile.close()
    return stat

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
    if (len(envAccount) > 6):
        shortName = str(envAccount[0:5])
    else:
        shortName = str(envAccount)
    #
    # If error, return some error text, otherwise return a null string
    #
    return shortName

#################################################################
#
# IBMCloudLogin - Log into the IBM Cloud
#
def IBMCloudLogin(user,pw,token):
    #
    # See if the Bluemix CLI is installed
    #
    cmd = "bx --version"
    errout = ExecCmd_Output(cmd)
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
    # Set current env values
    #
    findDefaults()
    
    return errout

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
# writeCSVRecord - Dump a row of data into output CSV file
#
def writeCSVRecord(csvFile, inp_1, inp_2, inp_3, inp_4, inp_5):
    #
    # fileCSV.writerow(('Account Name','UserGUID','USEREmail','Acct Email','Usage'))
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
    #
    # Write it out
    #
    try:
        csvFile.writerow([col_1, col_2, col_3, col_4, col_5])
    except UnicodeDecodeError:
            errout = "ERROR - Unicode OUTPUT error \n"
    #
    # If error, return some error text, otherwise return a null string
    #
    return errout

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
    print ("\n0. Quit")
    choice = raw_input(" >>  ")
    exec_menu(choice)
    
    return

# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print ("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
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

# Show billing summary
def bx_billing_summary():
    print ("Building current billing summary \n")
    #
    # Open an output file for this
    #
    filename = str(shortAcctName()) + "_billing_summary.txt"
    outfile = openTextFile(filename)
    #
    # Run the command to show all orgs
    #
    cmd = "bx billing account-usage"
    errout = ExecCmd_Output(cmd)
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

# Show all account orgs
def bx_billing_detail():
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
        cmd = "bx billing org-usage " + str(eachOption)
        errout = ExecCmd_Output(cmd)
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

# Modify default settings
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
    if (errout != ""):
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


# Back to main menu
def back():
    menu_actions['main_menu']()

# Exit program
def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': show_default,
    '2': bx_account_orgs,
    '3': bx_billing_summary,
    '4': bx_billing_detail,
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
    # Log into the IBM Cloud
    IBMCloudLogin(cloudUser,cloudPwd,cloudToken)
    # Launch main menu
    main_menu()
