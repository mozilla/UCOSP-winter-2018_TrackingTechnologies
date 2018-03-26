
# HTTPS and Mixed Content Vulnerability Analysis

This notebook looks at 2 things from the crawl dataset:
1. What percentage of websites use https.
2. How many websites are using mixed content. 

Mixed content is when a HTTPS webpage loads resouces, such as javascript files, over an insecure HTTP connection.


```python
import sys
sys.path.append('..')
from utils import load_data_util
```


```python
files_to_analyze = 10000
```

#### Download webcrawl data from S3 and build a dictionary with webpage urls as keys and HTTP / HTTPS information as values.


```python
data = load_data_util.load_random_data(files_to_analyze, False, 42, False)

result = {}
for index, row in data.iterrows():
    # get the url of the webpage that was being crawled and use that as a unique key.
    key = row['location']
    
    if key not in result:
        # check if the webpage is using https.
        is_https = False
        if key.split(":")[0] == "https":
            is_https = True

        result[key] = {
            "is_https": is_https,
            "http_script_urls": 0,
            "https_script_urls": 0
        }

    # record the number of javascript function calls for the webpage 
    # whose script url is fetched using http or https.
    url_protocol = row["script_url"].split("://")[0]
    if url_protocol == "http":
        result[key]['http_script_urls'] += 1
    elif url_protocol == "https":
        result[key]['https_script_urls'] += 1
```

### Analyze the collected data to get:
* A count of the number of websites that use https.
* A list of websites that have mixed content.


```python
urls_of_websites_with_mixed_content_vulnerability = []
number_of_https_websites = 0
x = 0
for key in result:
    if result[key]['is_https']:
        if result[key]['http_script_urls'] > 0:
            urls_of_websites_with_mixed_content_vulnerability.append(key)
        number_of_https_websites += 1
```

### Print out information for the total number of webpages that use HTTPS.


```python
percent_of_websites_using_https = round(number_of_https_websites / files_to_analyze * 100, 4)
print(
    str(percent_of_websites_using_https) + "% (" + 
    str(number_of_https_websites) + "/" + str(files_to_analyze) + 
    ") of websites use https."
)
```

    69.79% (6979/10000) of websites use https.
    

### Print out information collected for the number of webpages that have mixed content.


```python
number_of_websites_vulnerable = len(urls_of_websites_with_mixed_content_vulnerability)
percent_of_websites_vulnerable = number_of_websites_vulnerable / files_to_analyze * 100
print(
    str(percent_of_websites_vulnerable) + "% (" + 
    str(number_of_websites_vulnerable) + "/" + str(files_to_analyze) + 
    ") of websites have mixed content."
)

if number_of_websites_vulnerable > 0:
    print("The following websites have mixed content:")
for url in urls_of_websites_with_mixed_content_vulnerability:
    print(url)
```

    0.0% (0/10000) of websites have mixed content.
    
