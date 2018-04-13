### code to remount data if necessary
This is the critical code for accessing
data from S3.

Mounting essentially creates a filesystem within the cluster
located at `/dbfs/mnt/$BUCKET_NAME`. You can view the files via sh, or in python
(See: "basic text file reitreval example" for python example and "Example of
shell file retrieval" for a shell example)

```python
# ACCESS_KEY = ""
# SECRET_KEY = ""
# ENCODED_SECRET_KEY = SECRET_KEY.replace("/", "%2F")
BUCKET_NAME = "safe-ucosp-2017"
MOUNT_NAME = "safe-browsing"

# dbutils.fs.mount("s3a://%s:%s@%s" % (ACCESS_KEY, ENCODED_SECRET_KEY, BUCKET_NAME), "/mnt/%s" % MOUNT_NAME)
# dbutils.fs.mounts()

```

### basic text file retrieval example in Python
myRDD.first() returns the first
file in the rdd, which in this case is the only file

```python
filename = "1_1c1303ea628d99c741eef0ec90714853e72b7718022f1463903fb367.json"

file =  "/mnt/%s/%s" % (MOUNT_NAME, filename)

myRDD = sc.textFile(file)
myRDD.first()

```

### Functions to load data

```python
import requests
import os
import json

from os import listdir
from os.path import isfile, join

project_root_directory = os.path.dirname("/")

def load_index_file():
  """Load the file containing all indexes of the bucket and return it as an array of indexes - will download the index file if it's not in local storage"""
  file_name = "file_index.txt"
  file_path = os.path.join(project_root_directory, file_name)
  if not os.path.isfile(file_path):
      fetch_file("http://www.arewedatayet.com/", file_name, 'wb+')

  with open(file_path, "r") as f:
      lines = f.readlines()
  return lines

  
def fetch_file(file_url, file_name, mode):
    """Fetch file from base_url and store it in the project root directory.
    Keyword arguments:
    file_url -- url of where the file is
    file_name -- name of the file to be saved as
    mode -- mode of the file to open it in (for example: wb+)     
    """
    file = requests.get(file_url + file_name)

    file_path = os.path.join(project_root_directory, file_name)
    with open(file_path, mode) as f:
        f.write(file.content)


def load_file_via_rdd(file_count, lines):
  """ 
  file_count: int or "all"
    indicating all files or a specific subset of files from the start of the data
  lines:
    an array containing the list of the json file names
    
  return: rdd file containing the data based on the parameters provided
  """
  if file_count == "all":
    file_count = len(lines)
  url_list = map(url, lines[0:file_count])
  return sc.textFile(','.join(url_list))

def url(filename):
  """ converts index file name into mount storage location file name """
  x = "/mnt/%s/%s" % (MOUNT_NAME, filename)
  return x.strip()

def prep_rdd(rdd):
  """ converts rdd of files into rdd of json """
  return rdd.map(prep_data).flatMap(lambda x: json.loads(x))

def prep_data(data):
  """ converts S3 data file into json """
  return "[" + data[1:-1] + "]"

def p(s):
  """ Quick and dirty file print function for a collected rdd """
  for p in s:
    print(p)

### Alternative attempts at Retrieving data
# "http://"+BUCKET_NAME+".s3.amazonaws.com/"+filename
# "s3a://%s:%s@%s/%s" % (ACCESS_ID, ENCODED_SECRET_KEY, BUCKET_NAME, filename)

```

### Load parquet file

```python
file =  "/mnt/%s/safe_dataset/v1/clean.parquet/*.snappy.parquet" % (MOUNT_NAME)

clean_parquet_df = sqlContext.read.parquet(file)
display(clean_parquet_df)
```

### Load Index File
Index file contains the names of all the files on S3. The
index file hosted on Martins server. I have tried to load in all the files via
the file system unsuccessfully. The index file is very large and is loaded over
the internet so it takes a while to load.

```python
index = load_index_file()

```

### Examples of file retrieval via shell

```python
%sh
cd /
cd dbfs/mnt/safe-browsing/
head 1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json


```

```python
%sh
cd /

cd dbfs/mnt/safe-browsing/safe_dataset/v1/clean.parquet
ls
# head -n5 'part-00000-dfb456b1-7820-4f5f-a380-3f8e7c566a60-c000.snappy.parquet'

```

### Prep and Cache Data

```python

rdd_files = load_file_via_rdd(20000, index)
rdd_files = prep_rdd(rdd_files)



```

## Attempt to search for Evercookies
Evercookie is a JavaScript-based
application created by Samy Kamkar which produces zombie cookies in a web
browser that are intentionally difficult to delete. The source code is found
here: [Evercookie
script](https://github.com/samyk/evercookie/blob/master/js/evercookie.js).
Additional information can be found at the website https://samy.pl/evercookie/
below is a list of candidate attributes that could be used a sign of an
evercookie is being used. 
A significant sign of an evercookie being used would
be that the same value is being passed multiple times to these API calls.

```
option_list = [
    "cookie", "name", "embedSWF",  # misc
    "createElement",
"getContext", # canvas
    "localStorage", "sessionStorage", "globalStorage",
"Storage" # storage
    "indexedDB", "mozIndexedDB", "openDatabase",
"IDBTransaction", "IDBKeyRange", # DB
  ]
```

The below script is to get a sense of candidate api calls

```python

uniqueSymbols = rdd_files.map(lambda x : x['symbol']).distinct().collect()
p(uniqueSymbols)
```

### list of helper functions for investigation into evercookies

```python
import time
import json
from urlparse import urlparse
from pandas.io.json import json_normalize

""" misc functions """
def quick_print(rdd):
  """ collection and print rdd """
  for p in rdd.collect():
    print(p)

def extract_domain_name(data):
  """ extracts the domain name from a url to track patterns across domains """
  parsed_uri = urlparse( data )
  return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

def unique_list(rdd_list):
  """ convert rdd list into a list of unique values """
  return list(set(rdd_list))

def get_cookie_info(data):
  """ generate tuple of domain name, symbol and arguments for the function call """
  location = extract_domain_name(data['location'])
  arguments = data.get('arguments', '')
  return (location, (data['symbol'],  arguments))

def get_cookie_info_list_args(data):
  """ generate tuples with json values as arguments, json values might contain overlap with other data API call args? """
  location = extract_domain_name(data['location'])
  arguments = extract_json_values(data.get('arguments', ''))
  return (location, (data['symbol'],  arguments))

""" functions to check if the api call is an evercookie """
ev_cookie_api = [
  "cookie", "name", "embedSWF",  #misc
  "createElement", "getContext", #canvas
  "localStorage", "sessionStorage", "globalStorage", "Storage" #storage
  "indexedDB", "mozIndexedDB", "openDatabase", "IDBTransaction", "IDBKeyRange", # DB
]

def ev_cookie_candidate(symbol_arr):
  """ check if the symbol is a possible API call that could be used in an evercookie """
  for symbol in symbol_arr[1]:
    for attr_name in symbol[0].split("."):
      if attr_name in ev_cookie_api:
        return True
  return False

def api_call_is_ev_cookie_candidate(api_call):
  """ check if api call is a possible evercookie api call """
  for attr_name in api_call.split("."):
      if attr_name in ev_cookie_api:
        return True
  return False

""" Json Extraction related """
def flatten_json(y):
  """ flattens json including arrays """
  out = {}
  def flatten(x, name=''):
    if type(x) is dict:
      for a in x:
        flatten(x[a], name + a + '_')
      elif type(x) is list:
        i = 0
        for a in x:
          flatten(a, name + str(i) + '_')
          i += 1
      else:
          out[name[:-1]] = x

  flatten(y)
  return out

def extract_json_values(arg):
  """ extract json values into a tuple or store the data into a tuple """
  try:
    json_obj = json.loads(arg)
    flat = flatten_json(json_obj) # flatten and normalize json to extract all values
    return tuple(json_normalize(flat).values()) # if arg is json return values, as values might contain overlap with other api calls
  except JSONDecodeError:          
    return tuple(arg)

""" Key related filtering funtions """
def hasNumbers(inputString):
  """ true if string contains a number """
  return any(char.isdigit() for char in inputString)

def is_possible_key(arg):
  """ is string and string length 5 or greater and has a number in the string. We are assuming that it is possibly an ID """
  return type(arg) is str and len(arg) >= 5 and hasNumbers(arg)

def site_has_possible_key(domain_data):
  """ dig through nested data to check if the domain has an API call with a possible ID """
  for api_call in domain_data[1]:
    for arg in api_call[1]:
      if is_possible_key(arg):
        return True
  return False

def has_overlap_arg(domain_data):
  """ dig through nested data to check if the domain has a candidate function with an argument that overlaps and its a key """
  arg_total_list = []
  for api_call in domain_data[1]:
    if api_call_is_ev_cookie_candidate(api_call[0]):
      arg_list = list(api_call[1])
      print(arg_total_list)
      for arg in arg_list:
        if arg in arg_total_list and is_possible_key(arg):
          return True
      arg_total_list.extend(arg_list)
  return False

```

### Below was a preliminary attempt to search for Evercookies
As a preliminary
step I have generate an rdd of tuples containing the domains and the associated
api calls with their arguments
Then I filter out all the domains that don't make
api calls to evercookie caching techniques.

```python
out = rdd_files.map(get_cookie_info).groupByKey().mapValues(unique_list)
out = out.filter(ev_cookie_candidate )

"""
current structure:
[
  (domain_name, [(api_call, arg_string), ...] )
]
"""
quick_print(out)

```

### Evercookie attempt 2
extract json values passed to the api as possible
duplicate values used by evercookies. Remove all domains that do no have
overlaping values in the args passed to the api calls.

The result is a lot of
false positives. Difficult to find any good candidates for further examination.
Ideas to narrow down include: searching for IDs (aphanumeric?), filter out
obvious values like True, False.

```python
rdd_files = load_file_via_rdd("all", index)
rdd_files = prep_rdd(rdd_files)
```

```python
pout = rdd_files.filter(lambda x : x.get('arguments', '') != '')

pout = pout.map(get_cookie_info_list_args).groupByKey().mapValues(unique_list)

"""
current structure:
[
  (domain_name, [(api_call, (arg1,arg2,...)), ...] )
]
"""

# filter domains that don't make calls to web apis used by evercookies
pout = pout.filter(ev_cookie_candidate )

pout = pout.filter(site_has_possible_key)
pout = pout.filter(has_overlap_arg)

quick_print(pout)

```

```python
all_files = load_file_via_rdd("all", index)
all_files = prep_rdd(all_files)
```

```python
def isthing(data):
  return "evercookie.js" in data['script_url']

all_files.filter(isthing).count()
```
