import lib.ImageTagAutomation as ITA
import lib.ReadmeGeneration as RG
import argparse
import requests

def main(line, usernameStrGithub , passwordStrGithub):

    try:
        image_name, folder_name = line.strip().split(',')

        print("Getting image tags..")
        tag_list = ITA.get_image_tags_from_dockerhub(image_name, registry="ibmcom")

                
        if tag_list:
            print("Getting dockerfile links..")
            dict_tag_links_on_github, usage_text, remaining_tags, maintainer, source= ITA.get_tag_links_from_github(tag_list, folder_name, usernameStrGithub, passwordStrGithub)

            for key , value in dict_tag_links_on_github.items():
                print(" Key: ", key)
                print(" Value: ", value)

            print(remaining_tags)
            for tag in remaining_tags:
                dict_tag_links_on_github[tag] = "https://github.com/ppc64le/build-scripts/blob/master/"+folder_name+"/Dockerfiles"

            remaining_tags = []
            
            print("Generating readme file..")
            RG.set_file_name(image_name)
            RG.clear_file()
            RG.add_supported_tags_tab(dict_tag_links_on_github, remaining_tags)
            RG.add_maintainer_tab(maintainer)
            RG.add_source_tab(source)
            RG.add_usage_tab(usage_text)
            RG.add_disclaimer_tab()
                    
        else:
            print(" No tags found for the image.. Cannot create README.md file")
            return "docker"
    except TypeError as e:
        print(e)
        print("Github api access limit exceeded.. Try after one hour")
        return "github"
        
    except Exception as e:
        print(e)
        return "docker"

    
            

    

    
    
