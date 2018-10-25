'''
Python code that needs a list of images and updates it full description on dockerhub with static disclaimer.

Prerequisites:
    1. Selenium, requests and tkinter library installed in python windows
    2. Image list stored in imagenames.txt file one per line in same folder as push.py script
    3. chromedriver.exe present in same folder as push.py script


Run command:
    python3 push.py on cmd
    or
    Open script in idle editor and Run it.
'''



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk, Label, Entry, Button
import time
import script
import os


# username and password for  dockehub account
usernameStr = 'username'
passwordStr = 'password'

# username and password for  github account
usernameStrGithub = 'username'
passwordStrGithub = 'password'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# path to chromedriver for selenium to use
browser = webdriver.Chrome('lib/chromedriver.exe',chrome_options=options)

def get_dockerhub_login_box():
    root = Tk()
    root.title("Dockerhub credentials")

    #username entry
    username_label = Label(root, text=" Username: ")
    username_label.grid( row=0, column=0, padx=(20,20), pady=(10,10))
    username_entry = Entry(root)
    #username_entry.pack()
    username_entry.grid( row=0, column=1, padx=(20,20), pady=(10,10))

    #password entry
    password_label = Label(root, text=" Password: ")
    password_label.grid( row=1, column=0, padx=(20,20), pady=(10,10))
    password_entry = Entry(root, show='*')
    #password_entry.pack()
    password_entry.grid( row=1, column=1, padx=(20,20), pady=(10,10))

    def trylogin(): 
        global usernameStr
        global passwordStr
        usernameStr = username_entry.get()
        passwordStr = password_entry.get()
        root.quit()
        root.destroy()

    
    #when you press this button, trylogin is called
    button = Button(root, text="submit", command = trylogin) 
    #button.pack()
    button.grid( row=2, column=1, padx=(50,50), pady=(10,10))

    #App starter
    root.mainloop()

def get_github_login_box():
    root = Tk()
    root.title("Github credentials")

    #username entry
    username_label = Label(root, text=" Username: ")
    username_label.grid( row=0, column=0, padx=(20,20), pady=(10,10))
    username_entry = Entry(root)
    #username_entry.pack()
    username_entry.grid( row=0, column=1, padx=(20,20), pady=(10,10))

    #password entry
    password_label = Label(root, text=" Password: ")
    password_label.grid( row=1, column=0, padx=(20,20), pady=(10,10))
    password_entry = Entry(root, show='*')
    #password_entry.pack()
    password_entry.grid( row=1, column=1, padx=(20,20), pady=(10,10))

    def trylogin(): 
        global usernameStrGithub
        global passwordStrGithub
        usernameStrGithub = username_entry.get()
        passwordStrGithub = password_entry.get()
        root.quit()
        root.destroy()

    
    #when you press this button, trylogin is called
    button = Button(root, text="submit", command = trylogin) 
    #button.pack()
    button.grid( row=2, column=1, padx=(50,50), pady=(10,10))

    #App starter
    root.mainloop()

def login_to_docker():

    # open this web[page
    browser.get('https://hub.docker.com/login/')


    # wait till the username xpath is found
    username = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="nw_username"]')))

    # type the username
    username.send_keys(usernameStr)

    # get the password input through xpath
    password = browser.find_element_by_xpath('//*[@id="nw_password"]')

    # type passowrd
    password.send_keys(passwordStr)

    # get the login button through xpath
    submitButton = browser.find_element_by_xpath('//*[@id="nw_submit"]')

    # click to login
    submitButton.click()

    # wait till seach box xpath is loaded
    #search = WebDriverWait(browser, 10).until(
        #EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/form/div/div[1]/input')))

    time.sleep(10)
    


def push_file(image_name, folder_name):

    with open('lib/readmefiles/'+image_name+'.md') as file:
        text = file.read()
        text = text.replace('\t', '    ')
        
    browser.get('https://hub.docker.com/r/ibmcom/'+image_name+'/')
    
    # Short description
    # wait for the edit tab to load 
    editButton = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/span[2]/i')))

    # click to use text area
    editButton.click()

    # wait till text area loads
    editText = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/form/div/div[1]/input')))
    # clear previous contents
    editText.clear()
    editText.send_keys("Docker image for "+ image_name)
    
    # get the save button through xpath
    submitButton = browser.find_element_by_xpath('//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/form/div/div[2]/ul/li[2]/button')

    # click to save
    submitButton.click()

    time.sleep(3)

    # Full description
    # wait for the edit tab to load 
    editButton = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[1]/span[2]')))

    # click to use text area
    editButton.click()

    # wait till text area loads
    editText = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[2]/form/div/textarea')))
    # clear previous contents
    editText.clear()

       
        
    # type the required text
    #editText.send_keys("\n# Disclaimer \n SUBJECT TO ANY STATUTORY WARRANTIES THAT CANNOT BE EXCLUDED, IBM MAKES NO WARRANTIES OR CONDITIONS, EXPRESS OR IMPLIED, REGARDING THE PROGRAM OR SUPPORT, IF ANY, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, AND ANY WARRANTY OR CONDITION OF NON-INFRINGEMENT.")
    editText.send_keys(text)
    #time.sleep(5)
        
    # get the save button through xpath
    submitButton = browser.find_element_by_xpath('//*[@id="app"]/main/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/div[2]/form/div/div/ul/li[2]/button')

    
    # click to save
    submitButton.click()

def _find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
    
if __name__ == '__main__':
    try:
        get_dockerhub_login_box()
        get_github_login_box()
        login_to_docker()

        if not os.path.exists('lib/readmefiles'):
            os.mkdir('lib/readmefiles')


        with open('input_list.csv') as file:
            lines = file.readlines()

        with open('input.txt','w') as file:
            for line in lines:
                #print(line)
                image_name, folder_name = line.strip().split(',')[0].strip() ,line.strip().split(',')[1].strip()
                file.write(image_name)
                        
                folder_name = _find_between(folder_name,'master/','/')
                file.write("," + folder_name + '\n')
        
        with open('input.txt') as file:
            lines = file.readlines()
            
        with open('UpdatedImageList.csv','w') as file:
            for line in lines:
                ret = script.main(line, usernameStrGithub, passwordStrGithub)   
                image_name, folder_name = line.strip().split(',')

                try:
                    push_file(image_name, folder_name)
                except Exception as e:
                    file.write(image_name + "," + "authentication error\n")
                    continue

                if ret == 'docker':
                    file.write(image_name + "," + "docker error\n")
                elif ret == 'github':
                    file.write(image_name + "," + "github error\n")
                else:
                    file.write(image_name + "," + "success\n")
                
        print("Done") 
    

        
    except Exception as e:
        print("Exception :")
        print(e)
    
