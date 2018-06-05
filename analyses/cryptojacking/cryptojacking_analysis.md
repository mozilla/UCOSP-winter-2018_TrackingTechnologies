
# Cryptojacking Analysis Notebook

**Cryptojacking is defined as the unauthorized use of a user's computer or mobile device to mine cryptocurrency.**  
More and more websites are using browser-based cryptojacking scripts as cryptocurrencies rise in popularity. It is an easy way to make revenue and a viable alternative to bloating a website with advertising.  
The most popular (original) script is a JavaScript-based Monero miner that comes from CoinHive. American TV network Showtime sites, PirateBay, Politifact, Cristiano Ronaldo's personal website and the Ultimate Fighting Championship’s pay-per-view site are among some of the more notable websites that have experimented with usage of CoinHive mining scripts [[1]](https://www.makeuseof.com/tag/what-is-cryptojacking/ ). In 2017, cryptojacking scripts were found on 2496 e-commerce stores; some plainly visible, and others stealthily hidden in an iframe [[2]](https://gwillem.gitlab.io/2017/11/07/cryptojacking-found-on-2496-stores/). 
Adguard reported in November 2017 that in-browser cryptojacking had a growth rate of 31%; other research from November 2017 found 33,000 websites running crypto mining scripts, with a billion combined monthly visitors [[3]](https://www.wired.com/story/cryptojacking-cryptocurrency-mining-browser/). Site owners may not even know that their site is infected, as a hacker may inject the script without the site owner's knowledge.  

Many are touting adoption of cryptojacking as a positive thing, because users may tolerate giving up some CPU processing resources and enduring slower computer performance to avoid being bombarded with ads [[4]](https://www.wired.com/story/cryptojacking-cryptocurrency-mining-browser/). Although cryptojacking is a rising security threat, it is not considered illegal as no damage is done to victims' computers or data, no code is stored on the victims’ computers, and scripts stop executing when the user closes the browser tab running the script [[1]](https://www.makeuseof.com/tag/what-is-cryptojacking/ ). 

CoinHive is attempting to legitimize cryptojacking by offering a version of the script called AuthedMine, which only runs if users give explicit permission (in order to avoid facing regular ads) [[1]](https://www.makeuseof.com/tag/what-is-cryptojacking/ ). Malwarebytes researchers have found that AuthedMine is barely used, though CoinHive has disputed this, saying that ~35% of their clients use AuthedMine. Most script blockers also include AuthedMine in their blocklists [[5]](https://www.theregister.co.uk/2018/02/27/ethical_coinhive/). 

There are ways to prevent cryptojacking: 
1. Use anti-mining browser extensions
2. Use script blockers - Mozilla has one called NoScript.  
Read [[1]](https://www.makeuseof.com/tag/what-is-cryptojacking/ ) and [[3]](https://www.csoonline.com/article/3253572/internet/what-is-cryptojacking-how-to-prevent-detect-and-recover-from-it.html) for more details.

**The purpose of this notebook is to investigate the prevalence of cryptojacking by analysing script calls obtained from a web crawl of Alexa's top 10K sites in November 2017.**   
Detection algorithm: for each script call, check if any of cryptojacking hosts are pattern matched to script names in script tags. 
The list of potential cryptojacking hosts (212 sites total) was obtained from the [adblock-nocoin-list GitHub repo.](https://github.com/hoshsadiq/adblock-nocoin-list/blob/master/hosts.txt)  
Aspects of analysis:
1. How many script calls were detected with cryptojacking?
2. How many unique domains used cryptojacking scripts?
3. Which domains were the "worst" in terms of number of scripts used?
4. How many of the 212 cryptojacking hosts were used? 
5. Which cryptojacking scripts were used the most? 
   
The findings will potentially inspire future research and analysis on cryptojacking usage, and influence blocking lists implemented by browsers such as Mozilla Firefox.

Sources:  
[[1]](https://www.makeuseof.com/tag/what-is-cryptojacking/ ) https://www.makeuseof.com/tag/what-is-cryptojacking/  
[[2]](https://gwillem.gitlab.io/2017/11/07/cryptojacking-found-on-2496-stores/) https://gwillem.gitlab.io/2017/11/07/cryptojacking-found-on-2496-stores/  
[[3]](https://www.csoonline.com/article/3253572/internet/what-is-cryptojacking-how-to-prevent-detect-and-recover-from-it.html) https://www.csoonline.com/article/3253572/internet/what-is-cryptojacking-how-to-prevent-detect-and-recover-from-it.html  
[[4]](https://www.wired.com/story/cryptojacking-cryptocurrency-mining-browser/) https://www.wired.com/story/cryptojacking-cryptocurrency-mining-browser/  
[[5]](https://www.theregister.co.uk/2018/02/27/ethical_coinhive/) https://www.theregister.co.uk/2018/02/27/ethical_coinhive/

### Results: Summary

Less than 0.02% of script calls are detected with cryptojacking.  
However, it is important to note that cryptojacking code can be executed in other ways than by including the host .js script in a script tag. It can be disguised, stealthily executed in iframes,  or directly used in a function of a first party script. Users may also face redirect loops that eventually lead to a page with a mining script. Another reason for the low detection rate could be that the prominence/popularity of the analysed sites from the web crawl is enough to dissuade site owners from implementing obvious cryptojacking script usage.  
It is likely that the actual rate of cryptojacking is higher. 

The majority of domains that were detected with cryptojacking are streaming sites. This is unsurprising as users will have streaming sites open for longer as they are watching shows/movies, and mining scripts can be executed longer. 
The "worst" domain is a Chinese variety site called 52pk.com, with a count of 207. 

The majority of scripts used were from CoinHive, the original script developer. Only one use of AuthedMine was found. 

Note: Changing the stringency of site matching will alter results. For example, matching by domain rather than matching by full site name with subdomain, domain, and suffix gives many more results (and many more false positives).

Estimated time to run notebook: 1h

### Results: Statistics
number of distinct calls by script_url and location: 6069243  
number of distinct calls that use cryptojacking script: 945  
% of calls that use cryptojacking: 0.015%  

number of distinct domains: 29483  
number of distinct domains that used cryptojacking: 49  
% of domains that use cryptojacking:  0.166%

number of total cryptojacking hosts (from github repo): 212  
number of cryptojacking hosts used: 11  
% of cryptojacking hosts used: 5.19%  
% of CoinHive scripts: 53.65% (507/945)

#### Code to mount S3 bucket on dbfs


```
## Python 2/3 compatibility.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from six import text_type

from pyspark import StorageLevel
import numpy as np
import urllib.request
import tldextract 
```


```
BUCKET = 'safe-ucosp-2017/safe_dataset/v1'
MOUNT = "/mnt/{}".format(BUCKET.replace("/", "-"))
mountPoints = [m.mountPoint for m in dbutils.fs.mounts()]
already_mounted = MOUNT in mountPoints
if not already_mounted:
  dbutils.fs.mount("s3://" + BUCKET, MOUNT)
```


```
#import numpy as np
#BUCKET = 'safe-ucosp-2017/safe_dataset/v1'

#ACCESS_KEY = "MY_ACCESS_KEY"
#SECRET_KEY = "MY_SECRET_KEY"
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

Note: Analysis was done on union of clean and invalid parquet files but no cryptojacking was detected in invalid files - can avoid reading invalid files to save computation time.


```
clean_parquet_df = spark.read.parquet("{}/{}".format(MOUNT, 'clean.parquet'))
invalid_parquet_df = spark.read.parquet("{}/{}".format(MOUNT, 'invalid.parquet'))
```

Restrict to the list of unique `(page URL, script URL)` pairs in the dataset.

We get 6,064,923 distinct script calls from the clean dataset alone, and 6,069,243 distinct script calls from union of clean and invalid files.


```
distinct_clean = clean_parquet_df[['location', 'script_url']]
distinct_invalid = invalid_parquet_df[['location', 'script_url']]
distinct_all = distinct_clean.union(distinct_invalid)\
  .distinct()\
  .persist(StorageLevel.MEMORY_AND_DISK)
distinct_all.count()


```

Parse the external list of known cryptojacking hosts.


```
def get_cryptojacking_sites():
    data = urllib.request.urlopen("https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/hosts.txt")
    sites = []
    site_domains = []
    
    #Remove these skipped subdomains and suffixes from site names in final list
    skipped_subdomains = ["www", "www2", ""]
    skipped_suffixes = ["com", ""]
    
    for line in data: 
        line = text_type(line).strip()
        if line.startswith("0.0.0.0"):
            sites.append(line[8:])
    print("Unmodified list: " + text_type(sites))
            
    for site in sites:
      site_str = ""
      site_extr = tldextract.extract(site)
      if site_extr.subdomain not in skipped_subdomains:
        site_str = site_extr.subdomain + "." + site_extr.domain
      else:
        site_str = site_extr.domain
        
      if site_extr.suffix not in skipped_suffixes:
        site_str = site_str + "." + site_extr.suffix
      site_domains.append(site_str)
    return site_domains[:-10] # Hardcoding: remove last 10 sites in list; they are obfuscated.

cryptojacking_sites = get_cryptojacking_sites()
print("\nModified list: " + text_type(cryptojacking_sites))
print("\nNumber of sites: " + text_type(len(cryptojacking_sites)))
```

Check for script URLs that belong to the cryptojacking list.

- Count is 945 (with suffixes/prefixes)
- Count is 4,588 (when "wsp" subdomain is skipped - lots of calls to jsc.marketgid but none to wsp.marketgid (which is a known cryptojacking host))
- Count is 368,902 when matching domain only (removed prefixes/suffixes) -> problem, "analytics" domain matches all Google Analytics uses.


```
def detect_cryptojacking(row):
  for site in cryptojacking_sites:
      if site in row.script_url:
        return site, row.script_url, tldextract.extract(row.location).domain 

cryptoRDD = distinct_all.rdd.map(detect_cryptojacking)\
  .filter(lambda x: x is not None)\
  .persist(StorageLevel.MEMORY_AND_DISK)
cols = ['cryptojacking_TLD', 'script_url', 'location']
cryptoDF = spark.createDataFrame(cryptoRDD, cols)

cryptoDF_count = cryptoDF.count()
cryptoDF_count
```


```
cryptoDF.show(50, False)
```

How many distinct domains are there among the sites in the full dataset?


```
#Total number of distinct domains 
distinct_domains_count = distinct_all.rdd.map(lambda x: tldextract.extract(x.location).domain).distinct().count()
distinct_domains_count
```

How many domains have at least 1 detection of crypto-jacking?

- 14,523 (with prefixes/suffixes)
- 49 (without prefixes/suffixes)


```
domains = cryptoDF.select('location').rdd.distinct()
domains_count = domains.count()
domains_count
```

Which domains are the "worst" for crypto-jacking? This counts all the domains where crypto-jacking was detecting, ordered by the number of crypto-jacking scripts observed on them. However, since we have stripped prefixed and suffixes, this counts instances of crpyto-jacking scripts across all pages in the dataset sharing this domain.

Note that many of these are streaming sites


```
domain_with_counts = cryptoDF.groupby("location").count()
ordered_domains_with_counts = domain_with_counts.orderBy("count", ascending=False).show(100)
```

How many crypto-jacking TLDs are "active" - i.e., how many crypto-jacking TLDs were detected at least 1 time?


```
distinct_tlds = cryptoDF.select("cryptojacking_TLD").distinct().count()
distinct_tlds
```

Which crypto-jacking TLDs are the most used?


```
tlds_with_count = cryptoDF.groupby("cryptojacking_TLD").count()
ordered_tlds_with_count = tlds_with_count.orderBy("count", ascending=False).show(20)
```
