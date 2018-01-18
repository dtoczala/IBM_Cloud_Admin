# IBM_Cloud_Admin
A simple Python script to do some basic IBM Cloud administrative tasks

## Getting an API Key

Getting an API Key on IBM Cloud is easy.

* Log into the IBM Cloud, and navigate to your account settings in the upper right hand corner of the IBM Cloud in your web browser.  Select "
GitHub home (https://git.ng.bluemix.net/).
In the upper right hand corner of the screen, click on your picture or avatar, and select "Settings" from the drop down menu.
On the left hand nav bar of the Settings screen, select "Access Tokens"
Now create a new token with API access, and copy the contents of the token somewhere. This is the character string that you will insert into the GITHUB_TOKEN constant.
A quick note on access tokens. For security reasons, it is suggested that you periodically destroy tokens and re-create them (commonly called rotating your access tokens). Then if someone had access to your data by having one of your tokens, they will lose this access.
