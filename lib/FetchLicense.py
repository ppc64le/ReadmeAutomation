import requests

def fetch_unique_licenses(text):
        #print(text)
        lines = text.split('\n')

        #print( len(lines))
        license_list = []

        for line in lines[1:]:
                try:
                        package_name, license_info = line.split('|')[0].strip() , line.split('|')[1].strip().lower()
                except:
                        continue

                if license_info not in license_list:
                        license_list.append(license_info)



        #print( len(license_list) )
        #print( license_list)

        return license_list


def fetch_license( github_url ) :

        try:
                r = requests.get( github_url )
        except:
                return False

        if r.status_code > 400:
                return False
        
        return fetch_unique_licenses( r.text )
        
        




