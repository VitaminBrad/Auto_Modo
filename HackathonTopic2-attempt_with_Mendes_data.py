
# coding: utf-8

# # Model-Ready Reformatting of Experimental Data  
# 
# 1. Request file from a URL (presumably published expiermental data)
# and do any of the following if necessary:
#   1. Extract them from a zipped file, 
#   2. Convert them from a excel formats (.xls, .xlsx) - needs 10 minute clean-up
# 2. Upload the file to OpenRefine via its API
# 3. Perform clean-up operations in Open Refine
# 4. Download the data
# 
# <font color=gray>
# Future Directions:
# 
# 5. Run the data on the model
# 6. Return model output and whether it agrees/disagrees with experiment (implicitly recommended a change in model or experiment)
# 7. Then either:
#     1. Recommend necessary conditions for similar results or for a particular (user-defined) output to occur
#     2. Allow for the observation of different model outputs with theoretically different inputs
#     </font>

# In[89]:


import requests
import sys
import json # Do https://developer.rhino3d.com/guides/rhinopython/python-xml-json/
from IPython.display import HTML
import zipfile
import urllib.request
import os
import pandas as pd
import time


# In[90]:


#Be sure to use the link ("copy link address") as the raw! Not "download"
URL = 'https://doi.org/10.1371/journal.pcbi.1006680.s004'
if not (sys.argv[0]): URL = sys.argv[0]
    
items = URL.split("/")
file_name_parts = items[-1].split("?")
file_name = file_name_parts[0] + ".zip" #req: control statment to check if zip or not


# In[107]:


#with urllib
urllib.request.urlretrieve(URL, file_name)
cwd = os.getcwd()

path_to_zip_file = cwd + '\\' + file_name 
#unzip zipped files
zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
#Create folder to download into based on name of download
if not(os.path.exists(zip_extract_dest)): os.mkdir(file_name+"_extract")
zip_extract_dest = cwd + '\\' +file_name + "_extract"
zip_ref.extractall(zip_extract_dest) #directory to extract to
zip_ref.close()


# In[92]:





# In[117]:


#Create Project
file_ext,i = "",0
API_URL = "http://127.0.0.1:3333/command/core/create-project-from-upload"

#Jimmy-rigged method to determine file extension:
file_name_back = file_name[::-1]
while True:
    file_ext += file_name_back[i]
    if file_name_back[i] == '.': break 
    i += 1
file_ext = file_ext[::-1] #flip file extension to read in correct direction


#iterate through extracted zip folder to experimental data
for currentFile in os.listdir(zip_extract_dest):
    total_file_path = zip_extract_dest+'\\'+currentFile
    if currentFile.endswith(".txt"): 
        df = pd.read_csv(total_file_path, sep='\t', lineterminator='\n')
        csv = df.to_csv(sep='\t', float_format='%.3f')
        tsv = csv.replace(',','\t')
        upload_file_name = total_file_path[0:-len(file_ext)] + '.tsv'
        continue
    elif currentFile.endswith(".xls") or currentFile.endswith(".xlsx"):
        df = pd.read_excel(os.cwd)
        csv = df.to_csv()
        tsv = csv.replace(',','\t')
        continue
print(upload_file_name)
with open(upload_file_name, 'w') as wf:
    wf.write("" + tsv)
#tsv, put it in below 
data = {'project-file':(upload_file_name, open(upload_file_name, 'r'), 'application/vnd.ms-excel', {'Expires': '0'}), 
       }

# sending post request and saving response as response object 
r = requests.post(url = API_URL, files = data)


# In[ ]:


#Get Project

getURL = "http://127.0.0.1:3333/command/core/get-models"
getData = {'project': '2432443441126'}
g = requests.get(url = getURL, params = getData)
json_obj = g.json()
-    json.dump(json_obj, outfile)
g.text
    +++


# In[ ]:


#Apply Operations (Remove Column 'time')
project_id_remove = '1659010586174'
ops_url = "http://127.0.0.1:3333/command/core/apply-operations?" 
json_ops = [
  {
    "op": "core/column-removal",
    "description": "Remove column time",
    "columnName": "time"
  }
]

opsData = {'project': project_id_remove,
          'operations': json.dumps(json_ops)}

op = requests.post(url = ops_url,  data = opsData)
op.status_code
HTML(op.text)


# In[ ]:


#Delete Project
#Apply Operations - Remove
project_id_delete = '2432443441126'
ops_url = "http://127.0.0.1:3333/command/core/delete-project" 

op = requests.post(url = ops_url, data = opsData)
op.status_code
HTML()
op.text

