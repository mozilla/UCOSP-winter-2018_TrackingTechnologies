# Databricks notebook source
# MAGIC %md 
# MAGIC ### Eval and Function Analysis with Spark
# MAGIC 
# MAGIC This is a continuation of the analysis on the usage of Eval and the Function class to create Javascript functions for web pages in the webcrawl dataset. This analysis uses Spark to look at the entire dataset, as apposed to the other analysis which looked at random samples in the dataset. The primary purpose of this analysis is to compare an analysis of the entire dataset with the previous analysis of small samples. This is being done to check if the small sample was representative of the entire dataset.  
# MAGIC 
# MAGIC The previous Analysis can be found here: [eval_analysis.ipynb](eval_analysis.ipynb) and [eval_analysis.md](eval_analysis.md). An explanation for what eval is and a justification for why we are looking at eval usage can be found in the previous analysis.
# MAGIC 
# MAGIC Similairly to in the other analysis, we will refer to using eval, rather than both eval and new Function, for simplicity.
# MAGIC 
# MAGIC After looking at the entire dataset we found:
# MAGIC 1. 3.72% of function calls are created using eval.
# MAGIC 2. 8.76% of web pages have atleast 1 function call created using eval.  This is very similair to the samples taken in the previous analysis which was 8.92%.
# MAGIC 3. 32.65% of scripts hosting functions created using eval are hosted on a different domain that the domain of the web page that uses them. This is rounghly half of what was found in the earlier sample based analysis.

# COMMAND ----------

from __future__ import division
from pyspark.sql.functions import udf

import numpy as np
import tldextract

# COMMAND ----------

BUCKET = 'safe-ucosp-2017/safe_dataset/v1'

ACCESS_KEY = "YOUR_KEY"
SECRET_KEY = "YOUR_KEY"
ENCODED_SECRET_KEY = SECRET_KEY.replace("/", "%2F")
AWS_BUCKET_NAME = BUCKET

S3_LOCATION = "s3a://{}:{}@{}".format(ACCESS_KEY, ENCODED_SECRET_KEY, AWS_BUCKET_NAME)
MOUNT = "/mnt/{}".format(BUCKET.replace("/", "-"))

mountPoints = lambda: np.array([m.mountPoint for m in dbutils.fs.mounts()])
already_mounted = np.any(mountPoints() == MOUNT)
if not already_mounted:
    dbutils.fs.mount(S3_LOCATION, MOUNT)
display(dbutils.fs.ls(MOUNT))

# COMMAND ----------

df = spark.read.parquet("{}/{}".format(MOUNT, 'clean.parquet'))

# COMMAND ----------

unique_webpages = df.groupBy('location').count()
unique_webpage_count = unique_webpages.count()

# COMMAND ----------

function_count = df.count()

# COMMAND ----------

eval_calls = df[df.script_loc_eval.startswith('line')]
eval_call_count = eval_calls.count()

# COMMAND ----------

webpage_using_eval = eval_calls.groupBy('location').count()
webpage_using_eval_count = webpage_using_eval.count()

# COMMAND ----------

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

# COMMAND ----------

unique_script_urls = eval_calls.groupBy('script_url').count()
unique_script_urls_count = unique_script_urls.count()

# COMMAND ----------

eval_call_percentage = round(eval_call_count / function_count * 100, 2)
print(str(eval_call_percentage) + "% (" + str(eval_call_count) + "/" + str(function_count) + ") of total function calls are created using eval.")

# COMMAND ----------

webpage_using_eval_percentage = round(webpage_using_eval_count / unique_webpage_count * 100 , 2)
print(str(webpage_using_eval_percentage) + "% (" + str(webpage_using_eval_count) + "/" + str(unique_webpage_count) + ") of web pages have atleast 1 function created using eval.")

# COMMAND ----------

different_domain_percentage = round(different_domain_count / unique_script_urls_count * 100, 2)
print(str(different_domain_percentage) + "% (" + str(different_domain_count) + "/" + str(unique_script_urls_count) + ") of scripts are hosted on a different domain than the web page that called them.")
