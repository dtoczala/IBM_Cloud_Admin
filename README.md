# IBM_Cloud_Admin
**Author: [D. Toczala](https://github.com/dtoczala)**

A simple Python script to do some basic IBM Cloud administrative tasks.

This current script supports version 0.10.0. of the IBM Cloud CLI tool.  If you have 0.9.0. it will work with that as well, but you will need to disable the CLI version check in the code.

## Installation Guide

This is a guide to getting this tool properly installed on your system.  I have a Macbook (iOS) system, so I have tested this out on iOS systems, but not on Wondows or Linux platforms.  The concepts and steps should be the same, but the paths and some syntax may change on those platforms.

### Install the IBM Cloud CLI

In order to run this tool, you will need the latest version of the [IBM Cloud CLI](https://console.bluemix.net/docs/home/tools) installed on the system running this script.  If you want to, you can [install the CLI as a stand-alone install](https://console.bluemix.net/docs/cli/reference/ibmcloud/download_cli.html#install_use).

This CLI is updated on a relatively frequent basis, and the [author of this script](https://github.com/dtoczala) will attempt to maintain the script with the current version of the CLI.  **If you have not updated the CLI on your system, this script WILL HANG**.  The CLI will be prompting you to ask if you would like to update the CLI, and it is awaiting a response.  You will need to go and update the CLI from the command line.  To do this, just log into the IBM Cloud with the CLI by issuing an IBM Cloud target command like this:

> ibmcloud target -cf

### Install Anaconda

Most of the early users of this tool became frustrated when attemping to use it because it has some unique dependencies.  I use an [Anaconda](https://anaconda.org/) python development environment to manage these dependencies.  To get started, you will need to install [Anaconda](https://anaconda.org/).

You can find the main [Anaconda](https://anaconda.org/) page and navigate from there - but it confuses me me lately.  So instead I'll point you at the [Anaconda downloads page](https://www.anaconda.com/download).  Go to the [Anaconda downloads page](https://www.anaconda.com/download) and select the Anaconda download package for your particular platform.  Once you have downloaded it, install it onto your system.

While you are at it, you should probably go and grab a copy of the [Anaconda Cheat Sheet](https://conda.io/docs/_downloads/conda-cheatsheet.pdf).  This will help you understand your Anaconda environments, and help you in using the tool.

### Create IBM Cloud Admin Python Environment

Once [Anaconda](https://anaconda.org/) is installed on your system, you will want to set up a proper Python environment for the IBM Cloud Admin tool to use.  Download the [IBM_Cloud_admin.env](https://github.com/dtoczala/IBM_Cloud_Admin/blob/master/IBM_Cloud_Admin.env) file from this project area to your local machine.  Once this is done, you will open up a command line window (a "Terminal" on iOS, a command prompt on Windows) and enter the following command:

> conda create -n IBM_Cloud_Admin --file IBM_Cloud_Admin.env

This creates a new environment, which you will need to switch to before trying to run the IBM_CLoud_Admin tool.  This environment should have all of the proper Python packages downloaded and installed.  You MIGHT need to do the following command to make sure that the proper unicodecsv package is installed.

> conda install unicodecsv

To run the IBM_Cloud_Admin tool, make sure that you first do the following:

> source activate IBM_Cloud_Admin

> conda info -e

## How to Use the Script

To run the script, you can just type in:

> python IBM_Cloud_Admin.py -t apiKey.json -b -s

The script has a few different modes it can run in.

* If you use the -t flag, it will use an API Key file, which you can get from your IBM Cloud account, to log into the IBM Cloud.  This is the way that I like to use it.
* If you don’t use the -t flag, you’ll need to supply a username and password for your IBM Cloud account using the -u and -p flags.
* If you use the -b flag (for billing information), then you will run in batch mode.  This will get billing information for the account being logged into, and then quit.  You can use this mode in a script, since it does not require any user input.
* If you use the -s flag (for security information), then you will run in batch mode.  This will get security information for the account being logged into, and then quit.  You can use this mode in a script, since it does not require any user input.
* If you don’t use the -b flag or the -s flag, then you will run in interactive mode.  This will display menus on the command line that you can choose from.

When running in an interactive mode, you can use the tool to process CSV files with lists of users, and add these users to particular accounts, organizations and spaces.  This user administrative capability is still being developed and refined.

There are a number of output files from this tool.  There is the IBM_Cloud_Admin.output.log file, which contains a log of your session and will show you the IBM Cloud command line commands issued by the tool, and the responses that were returned.  This is a good way to get familiar with the IBM Cloud command line commands, so you can include into custom scripts for your own use. 

You may also see files with names like, MyProj_billing_summary.csv and MyProj_billing_by_org.json.  These are billing reports that you generated from the tool.  Here is a list of the reports, and what they contain.

* **MyProj_billing _summary.csv** – this CSV file contains billing summary data for your account for the current month.
* **MyProj_billing _summary.json** – this JSON file contains billing summary data for your account for the current month.  It shows the raw JSON output from the IBM Cloud CLI.
* **MyProj_billing _by_org.csv** – this CSV file contains billing details data for your account, split out by org and space, for the current month.
* **MyProj_billing _by_org.json** – this JSON file contains billing details data for your account, split out by org and space, for the current month.  It shows the raw JSON output from the IBM Cloud CLI.
* **MyProj_annual_billing _summary.csv** – this CSV file contains billing summary data for your account for the past year.
* **MyProj_annual_billing _summary.json** – this JSON file contains billing summary data for your account for the past year.  It shows the raw JSON output from the IBM Cloud CLI.
* **MyProj_annual_billing _by_org.csv** – this CSV file contains billing details data for your account, split out by org and space, for the past year.
* **MyProj_annual_billing _by_org.json** – this JSON file contains billing details data for your account, split out by org and space, for the past year.  It shows the raw JSON output from the IBM Cloud CLI.
* **MyProj_account_security.csv** – this CSV file contains account user access and role details for your account, split out by account, org and space.

Use the JSON output files as inputs to further processing that you might want to do of your IBM Cloud usage data.  The CSV files can be used as inputs to spreadsheets and pivot tables that you can build that will show you details on usage from an account perspective, as well as from an organization and space perspective.

## Getting an API Key

Getting an API Key on IBM Cloud is easy.

* Log into the IBM Cloud, and navigate to your account settings in the upper right hand corner of the IBM Cloud in your web browser.  Select "**Manage > Security > Platform API Keys**"
![IBM Account API Key Selection](https://github.com/dtoczala/IBM_Cloud_Admin/blob/master/Account_API_Key.png "Generating an API Key")
* Click on the blue "**Create**" button
* In the resulting dialog, select a name for your API Key (something that you will see and know which IBM Cloud account the key is assocuated with), give a short description, and hit the blue "**Create**" button.
* You should now see a page indicating that your API Key has been successfully created.  If not, then start over again from the beginning.  If you have successfully created an API Key, download it to your machine, and store it somewhere secure.

**_Note:_** A quick note on API Keys. For security reasons, it is suggested that you periodically destroy API Keys and re-create them (commonly called rotating your API keys or access tokens). Then if someone had access to your data by having one of your API keys, they will lose this access.
