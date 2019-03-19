'''
This is a python script that just dumps all the data
passed to it in a README.md file generated in same folder
'''
_filename = "README.md"
def set_file_name(imagename):
    global _filename
    _filename = "lib/readmefiles/"+imagename+".md"


    
def clear_file():
    '''Function that creates a new file or truncates an existing file if any'''
    with open(_filename,'w') as file:
        pass


def add_supported_tags_tab(dict_tag_links_on_github, remaining_tags):
    ''' Function that accepts a dictionary of tag names as key and github links as value
    and a list of tags with no github lniks

    This information is then appended to the previous contents of README.md file
    '''
    with open(_filename,'a') as file:
        file.write("\n # Supported Tags and respective `Dockerfile` links\n")

        for key, value in dict_tag_links_on_github.items():
            file.write(" * " + key)
            file.write( "  [ ( " + key + "/Dockerfile ) ]" + "(" + value + ") \n")

        for tag in remaining_tags:
            file.write(" * " + tag + "\n")


def add_disclaimer_tab():
    ''' Function to append a static disclaimer to previous contents of README.md file'''
    with open(_filename,'a') as file:
        with open('static_content.txt') as rd:
            text = rd.read()
        file.write("\n\n"+text)
    
def add_source_repository_tab(reponame, repolink):
    ''' Function that takes source repository name and its github link as parameters
    and appends the infomration to previous contents of README.md file'''
    with open(_filename,'a') as file:
        file.write("\n# Source Repository \n")
        file.write( "  [ " + reponame + " ]" + "(" + repolink + ") \n")


def add_usage_tab( usage_text ):
    '''Function that takes usage_text and appends it to the README.md file'''
    if usage_text:
        with open(_filename, 'a') as file:
            file.write("\n# Usage Information \n")
            file.write( usage_text )

def add_maintainer_tab( maintainer_text ):
    '''Function that takes usage_text and appends it to the README.md file'''
    if maintainer_text:
        with open(_filename, 'a') as file:
            file.write("\n# Author \n")
            file.write( maintainer_text )

def add_source_tab( source_text ):
    '''Function that takes usage_text and appends it to the README.md file'''
    if source_text:
        with open(_filename, 'a') as file:
            file.write("\n# Based On \n")
            file.write( source_text )

            
def add_license_tag( license_list ) :
    '''Function that takes license list and appends it to the README.md file'''


    
    if len(license_list)!=0:
        with open(_filename,'a') as file:
            file.write("\n# License Information \n")
            file.write(" This image uses following licenses ")
            

            file.write(" [ ")
            for each_license in license_list[:-1]:
                if len(each_license)!=0:
                    try:
                        file.write( each_license.strip() + ", ")
                    except:
                        continue
            
            file.write(" ] ")

    

