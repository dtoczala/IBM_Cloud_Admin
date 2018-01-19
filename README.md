# IBM_Cloud_Admin
A simple Python script to do some basic IBM Cloud administrative tasks

## Getting an API Key

Getting an API Key on IBM Cloud is easy.

* Log into the IBM Cloud, and navigate to your account settings in the upper right hand corner of the IBM Cloud in your web browser.  Select "**Manage > Security > Platform API Keys**"
![IBM Account API Key Selection](https://github.com/dtoczala/IBM_Cloud_Admin/blob/master/Account_API_Key.png "Generating an API Key")
* Click on the blue "**Create**" button
* In the resulting dialog, select a name for your API Key (something that you will see and know which IBM Cloud account the key is assocuated with), give a short description, and hit the blue "**Create**" button.
* You should now see a page indicating that your API Key has been successfully created.  If not, then start over again from the beginning.  If you have successfully created an API Key, download it to your machine, and store it somewhere secure.

**_Note:_** A quick note on API Keys. For security reasons, it is suggested that you periodically destroy API Keys and re-create them (commonly called rotating your API keys or access tokens). Then if someone had access to your data by having one of your API keys, they will lose this access.
