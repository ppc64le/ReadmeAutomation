# ReadmeAutomation
Automate creation of READMEs for containers

# Prerequisites
* Python2/Python3 installed and in system path in Windows Os
* tkinter, requests, future and selenium packages for python installed using pip 
* [Google Chrome Driver](https://chromedriver.storage.googleapis.com/2.42/chromedriver_win32.zip) Place the downloaded chromedriver.exe file under ReadmeAutomation/lib/ directory.

```
pip install selenium
pip install tkinter
pip install requests
pip install future
```

# How to use ?

Input is given through a file named ```input_list.csv``` in the same folder as the push.py script.
The file should contain image names on dockerhub, corresponding dockerfile links on github ppc64le/buildscripts repo and the licenses used by the image.
The script will generate ```input.txt``` containing image names and corresponding folder names from github repo. 

If the script encounters any error during generation of readmefiles, the script will be terminated and list of updated entries will be stored in ```UpdatedImageList.csv```.

The Publication Statement and Community Support is added statically from file named static_content.txt.

**Note :** Images should always be on ibmcom registry and corresponding folders should always be in build-scripts repo on github under ppc64le.
