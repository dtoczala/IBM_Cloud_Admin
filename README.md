# IBM_Cloud_Admin
A simple Python script to do some basic IBM Cloud administrative tasks.

This current script supports version 0.6.5. of the IBM Cloud CLI tool.

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
