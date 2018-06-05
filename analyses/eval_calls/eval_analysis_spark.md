
### Eval and Function Analysis with Spark

This is a continuation of the analysis on the usage of Eval and the Function class to create Javascript functions for web pages in the webcrawl dataset. This analysis uses Spark to look at the entire dataset, as apposed to the other analysis which looked at random samples in the dataset. The primary purpose of this analysis is to compare an analysis of the entire dataset with the previous analysis of small samples. This is being done to check if the small sample was representative of the entire dataset.  

The previous Analysis can be found here: [eval_analysis.ipynb](eval_analysis.ipynb) and [eval_analysis.md](eval_analysis.md). An explanation for what eval is and a justification for why we are looking at eval usage can be found in the previous analysis.

Similairly to in the other analysis, we will refer to using eval, rather than both eval and new Function, for simplicity.

After looking at the entire dataset we found:
1. 3.72% of function calls are created using eval.
2. 8.76% of web pages have at least 1 function call created using eval.  This is very similar to the samples taken in the previous analysis, which was 8.92%.
3. 32.65% of scripts hosting functions created using eval are hosted on a different domain that the domain of the web page that uses them. This is roughly half of what was found in the earlier sample based analysis.


```python
## Python 2/3 compatibility.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from six import text_type

from pyspark.sql.functions import udf
import numpy as np
import tldextract
```


```python
#BUCKET = 'safe-ucosp-2017/safe_dataset/v1'

#ACCESS_KEY = "YOUR_KEY"
#SECRET_KEY = "YOUR_KEY"
#ENCODED_SECRET_KEY = SECRET_KEY.replace("/", "%2F")
#AWS_BUCKET_NAME = BUCKET

#S3_LOCATION = "s3a://{}:{}@{}".format(ACCESS_KEY, ENCODED_SECRET_KEY, AWS_BUCKET_NAME)
#MOUNT = "/mnt/{}".format(BUCKET.replace("/", "-"))

#mountPoints = lambda: np.array([m.mountPoint for m in dbutils.fs.mounts()])
#already_mounted = np.any(mountPoints() == MOUNT)
#if not already_mounted:
#    dbutils.fs.mount(S3_LOCATION, MOUNT)
#display(dbutils.fs.ls(MOUNT))
```


```python
BUCKET = 'safe-ucosp-2017/safe_dataset/v1'
MOUNT = "/mnt/{}".format(BUCKET.replace("/", "-"))
mountPoints = [m.mountPoint for m in dbutils.fs.mounts()]
already_mounted = MOUNT in mountPoints
if not already_mounted:
  dbutils.fs.mount("s3://" + BUCKET, MOUNT)
```


```python
df = spark.read.parquet("{}/{}".format(MOUNT, 'clean.parquet'))
```

Compute counts of:
  
- the number of unique URLs crawled
- the total number of function calls (rows) in the dataset


```python
unique_webpages = df.groupBy('location').count()
unique_webpage_count = unique_webpages.count()
unique_webpage_count
```


```python
function_count = df.count()
function_count
```

And now for `eval` calls:


```python
eval_calls = df[df.script_loc_eval.startswith('line')]
eval_call_count = eval_calls.count()
eval_call_count
```


```python
webpage_using_eval = eval_calls.groupBy('location').count()
webpage_using_eval_count = webpage_using_eval.count()
webpage_using_eval_count
```

How many of the scripts using `eval` calls are on a different domain from the original page?


```python
def check_if_different_domain(location, script_url):
  location_domain = tldextract.extract(location).domain
  script_domain = tldextract.extract(script_url).domain
  
  return location_domain != script_domain

is_different_domain = udf(check_if_different_domain)

different_domain_df = eval_calls.withColumn(
  'is_different_domain', is_different_domain(eval_calls.location, eval_calls.script_url)
)

different_domains = different_domain_df[different_domain_df.is_different_domain == True].groupBy('script_url').count()
different_domain_count = different_domains.count()
different_domain_count
```


```python
unique_script_urls = eval_calls.groupBy('script_url').count()
unique_script_urls_count = unique_script_urls.count()
unique_script_urls_count
```


```python
eval_call_percentage = eval_call_count / function_count * 100.0
print("{:.2f}% ({:,}/{:,}) of total function calls are created using eval.".format(
  eval_call_percentage, eval_call_count, function_count))
```


```python
webpage_using_eval_percentage = webpage_using_eval_count / unique_webpage_count * 100.0
print("{:.2f}% ({:,}/{:,}) of web pages have at least 1 function created using eval.".format(
  webpage_using_eval_percentage, webpage_using_eval_count, unique_webpage_count))
```


```python
different_domain_percentage = different_domain_count / unique_script_urls_count * 100.0
print("{:.2f}% ({:,}/{:,}) of scripts using eval are hosted on a different domain than the web page that called them.".format(
  different_domain_percentage, different_domain_count, unique_script_urls_count))
```
