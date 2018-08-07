#!/usr/bin/env python

#test push code
try:
   import requests
except ImportError:
    print ("Error: requests is not installed")
    print ("Installing Requests is simple with pip:\n  pip install requests")
    print ("More info: http://docs.python-requests.org/en/latest/")
    exit(1)
import json
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
def ensure_str(s):
    try:
        if isinstance(s, unicode):
            s = s.encode('utf-8')
    except:
        pass
    return s

#Get a list of all artifacts in a repository
url = "http://146.148.82.42:8093/artifactory/api/search/aql"
payload = "items.find(\n    {\n        \"repo\":{\"$eq\":\"docker\"}\n    }\n)\n" # Add body to the POST request
headers = {
    'Authorization': "Basic YWRtaW46TjR3cGlJMlJZaw==",
    } # Basic Authorization
response = requests.request("POST", url, data=payload, headers=headers)
results = response.json()["results"] #convert results to json
querystring = {"stats":""}
headers = {
    'Authorization': "Basic YWRtaW46TjR3cGlJMlJZaw==",
    } # Basic Authorization

#Create a list to keep track of downloaded files
file_downloads = []

#Get file stats that includes the download count
for r in results:
    url = "http://146.148.82.42:8093/artifactory/api/storage/" + r["repo"] + "/" + r["path"] + "/" + r["name"] + "?stats"
    response = requests.request("GET", url, headers=headers, params=querystring)
    fileobj = response.json()
    file_downloads.append({'name':r["name"], 'uri':fileobj['uri'], 'downloads': fileobj['downloadCount']})

#sort the list of dowloaded files according by most number of downloads
file_downloads.sort(key=lambda x: x['downloads'], reverse=True)
#print the most downloaded file
print('Most dowloaded file name:', file_downloads[0]['name'], ' uri: ', file_downloads[0]['uri'], ' num of downloads: ', file_downloads[0]['downloads'])
#print the 2nd most downloaded file
print('2nd most downloaded file name:', file_downloads[1]['name'], ' uri: ', file_downloads[1]['uri'], ' num of downloads: ', file_downloads[1]['downloads'])
