'''
Python module to fetch image tags and required github repo links
'''
from __future__ import print_function
from builtins import input

from future.standard_library import install_aliases
install_aliases()

import requests
import argparse
from urllib.request import urlopen
from urllib.error import HTTPError
import json
from requests.auth import HTTPBasicAuth


# github creds
_username = 'username'
_password = 'password'

#helper functions
def _find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def _get_www_authenticate_header(api_url):
    try:
        resp = urlopen(api_url)
        response = resp.read()
    except HTTPError as error:
        response = error.info()['Www-Authenticate']
    return response 


def _get_token(user, password, service, scope, realm):
    data = {"scope":scope+',push', "service":service, "account":user}

    #r = requests.get(realm, auth=HTTPBasicAuth(user, password), data=data)

    url = realm + '?service=' + service + '&scope=' + scope
    r = requests.get(url)
        
    token = _find_between(str(r.content), '"token": "', '"')
    #print (token)
    
    return token


def _get_result(api_url, token):
    #print(len(token))
    r = requests.get(api_url, headers={'Authorization':'Bearer ' + token})
    return r


def _create_parser():
    # Creating a parser for getting command line arguments
    parser = argparse.ArgumentParser(description="Tool for making api call to docker hub registry for getting image tags")

    parser.add_argument('--user', required=False, help='Username of the account used to make the request', default='')
    parser.add_argument('--password', required=False, help='Password of the account used to make the request', default='')
    parser.add_argument('--api_url_start', required=False, help='The API url that you want to access', default='https://registry.hub.docker.com/v2/')
    parser.add_argument('--api_url_end', required=False, help='The API url that you want to access', default='/tags/list/')
    parser.add_argument('--image_name', required=False, help='The name of the image for which you want to fetch all the tags.', default='tensorflow-ppc64le')
    parser.add_argument('--registry_name', required=False, help='The name of the registry which contains the image', default='ibmcom')

    args = parser.parse_args()
    return args

def get_image_tags_from_dockerhub(image_name="kafka-ppc64le",registry="ibmcom"):
    try:
        args = _create_parser()
        
        args.image_name = image_name
        args.registry_name = registry

        # First we will need to authenticate user credentials on the dockerhub website
        # This verification will return a token for further communication
        api_url = args.api_url_start + args.registry_name + "/" + args.image_name + args.api_url_end
        #print(api_url)
        
        #get the Www-Authenticate header
        params = _get_www_authenticate_header(api_url)
        #print(params)

        #parse the params required for the token
        if params:
            realm = _find_between(params, 'realm="', '"')
            service = _find_between(params, 'service="', '"')
            scope = _find_between(params, 'scope="', '"')

            #print(realm)
            #print(service)
            #print(scope)
            
            # retrieve token
            token = _get_token(args.user, args.password, service, scope, realm)

            # Do the API call as an authenticated user
            #print("Response:")
            response = _get_result(api_url, token)

            # Format the json data for printing
            json_data = json.loads(response.text)

            #print(" Image name: ", json_data['name'])
            #print(" Tags: ")
            #for tag in json_data['tags']:
            #   print( tag )

            return json_data['tags']
        else:
            #print("404 Not Found")
            return None
    except Exception as e:
        print (e)
        return None


def _get_directory_contents(dirname):
    '''Function to get the list of all files in a directory on ppc64le/build-scripts repository'''

    # http get request url for fetching directory info
    url = "https://api.github.com/repos/ppc64le/build-scripts/contents/" + dirname
    #print(url)
    r = requests.get(url,auth=HTTPBasicAuth(_username, _password))

    # convert the response in json format
    json_data = json.loads(r.text)

    return json_data

def _search_tags_in_directory(tag_list, json_data):
    '''Function that takes list of tags and json data of a directory and check is respective
    dockerfiles exits
    Returns a dictionary of key as tags and values as dockerfile folder github links and a list of tags
    with no corresponding links found'''

    # creating a deep copy of tag list
    temp_tag_list = tag_list[:]
    dict_folder_links = {}

    json_data = json_data
    
    for obj in json_data:
        
        # check if name of file in folder is latest, then get the converted tag through symlink 
        if obj['name']=="latest":
            download_url = obj['download_url']
            r = requests.get(download_url,auth=HTTPBasicAuth(_username, _password))
            converted_tag = r.text.split()[0].strip()[2:] # to remove "./" from "./x.x.x"
            dict_folder_links["latest"] = obj['path']
            temp_tag_list.remove("latest")
            continue  

        for tag in temp_tag_list:
            #print(obj['name'])
            #print(tag)

            if obj['name']==tag :     # check if name of file contains the tag
                #print("tag found")
                #print( obj['name'], obj['path'])
                dict_folder_links[tag] = obj['path']
                #print(obj['path'], end='\n\n')
                temp_tag_list.remove(tag)

    if "latest" in dict_folder_links.keys():
        dict_folder_links["latest"] = dict_folder_links[converted_tag]
                
    return dict_folder_links, temp_tag_list

def _search_dockerfiles_in_folder(dict_folder_links):
    '''Function that takes dictionary of key as tags and value as dockerfile folder github links

    Returns a dictionary of key as tags and values as dockerfile github links and usage text'''
    
    dict_tag_links_on_github = {}
    usage_text = ""
    check = True
    maintainer = ''
    source = ''

    for key, value in dict_folder_links.items():

        json_data = _get_directory_contents(value)
        
        
        for data in json_data:
            #print(data, end='\n\n')
            if data['name'] == 'Dockerfile':
                #print(data['html_url'])        
                dict_tag_links_on_github[key] = data['html_url']
                
                dockerfile_url = data['download_url']
                #print(dockerfile_url)
                dockerfile_text = requests.get( dockerfile_url ).text
                lines = dockerfile_text.split('\n')
                for line in lines:
                    if 'MAINTAINER' in line:
                        #print(line)
                        maintainer = line.replace('MAINTAINER ',"")
                    elif 'clone' in line :
                        #print(line)
                        source = _find_between(line, "clone ", " ")
            elif data['name'] == 'README.md' and check:
                readme_url = data['download_url']
                usage_text = requests.get( readme_url ).text
                check = False

    if '/' not in source:
        source = ''
    return dict_tag_links_on_github, usage_text, maintainer, source

def get_tag_links_from_github(tag_list, dirname, usernameStrGithub, passwordStrGithub):
    '''Function that takes tag list and a folder name on github and searches respective dockerfile link in the folder'''

    # setting authentication creds
    global _username
    global _password  
    _username = usernameStrGithub
    _password = passwordStrGithub
    
    json_data = _get_directory_contents(dirname+"/Dockerfiles" )
    #print(json_data)
    
    dict_folder_links, remaining_tags = _search_tags_in_directory(tag_list, json_data)
    #print(dict_folder_links)
    
    dict_tag_links_on_github, usage_text, maintainer, source = _search_dockerfiles_in_folder(dict_folder_links)
    #print(dict_tag_links_on_github)

    return dict_tag_links_on_github, usage_text, remaining_tags, maintainer, source

