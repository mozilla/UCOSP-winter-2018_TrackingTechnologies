
**This analysis aim to look at known sites which calls known session replay sites to see if we can find signs of session replay activity.**

Session replay providers are services that offer websites a way to track their users - from how they interact with the site to what searches they performed and input they provided. Some session replay providers may even record personal information such as personal addresses and credit card information.

The list of session replay sites comes from the  [**Princeton WebTAP project**](https://webtransparency.cs.princeton.edu/no_boundaries/session_replay_sites.html), which listed sites within the Alexa top 10,000 that show signs of session replay scripts.


### Based on previous analysis on a sample:

With a sample size of 2494 base sites: 90 were found to use session replay calls.
However when we boil it down to the base url the sample size reduced to 1136 unique base urls and 62 of which uses session replay. And an overall 3.15% of all calls were to a session_replay provider.

**Of the sites that were found to be using session replay calls, 35.5% had a .ru suffix. Which is significantly higher than it's distribution in the overall urls captured, 4.0%. Additionally, 27/45 of the .ru sites were using a session replay site. That is 60% of all .ru sites tracked uses session replay scripts compared to the overall 62/1136, 5.5% of all domains using session replay scripts. With the .ru sites we track, it has a 20x more probability of using session replay_scripts versus non .ru sites.**

**When considering http vs https distributions: sites that uses session replay calls has a higher 53.3% http distribution vs the overall 31.3% http distribution**

Sites that uses session_replay scripts:

 '24smi.org',
 '>B:@KBK9C@>:.@D',
 'base.garant.ru',
 'dnevnik.ru',
 'dugtor.ru',
 'football.ua',
 'getcourse.ru',
 'hdrezka.ag',
 'hh.ru',
 'ibizlife.com',
 'lady.nur.kz',
 'mp3party.net',
 'my-shop.ru',
 'netbarg.com',
 'nl.justporno.tv',
 'out.pladform.ru',
 'pagseguro.uol.com.br',
 'porn555.com',
 'povar.ru',
 'rutube.ru',
 'seasonvar.ru',
 'serienstream.to',
 'sprashivai.ru',
 'steam.softonic.com',
 'studfiles.net',
 'tap.az',
 'top.mail.ru',
 'torrent-filmi.net',
 'trinixy.ru',
 'www.autodesk.com',
 'www.avito.ru',
 'www.azet.sk',
 'www.bamilo.com',
 'www.banggood.com',
 'www.bbcgoodfood.com',
 'www.cardinalcommerce.com',
 'www.casadellibro.com',
 'www.eleman.net',
 'www.eurosport.fr',
 'www.fastweb.it',
 'www.fotocasa.es',
 'www.geekbuying.com',
 'www.gl5.ru',
 'www.jbhifi.com.au',
 'www.kommersant.ru',
 'www.labirint.ru',
 'www.maam.ru',
 'www.maxcdn.com',
 'www.msu.ru',
 'www.net-a-porter.com',
 'www.newchic.com',
 'www.rbcplus.ru',
 'www.sports.ru',
 'www.stackoverflowbusiness.com',
 'www.stranamam.ru',
 'www.templatemonster.com',
 'www.the-star.co.ke',
 'www.thermofisher.com',
 'www.twirpx.com',
 'www.universal.org',
 'www.vseinstrumenti.ru',
 'xhamster.com'

Correlation between call symbols and wheter or not the call is a session replay call is also attempted, however the correlation weren't very strong - with the highest being **window.navigator.plugins[Shockwave Flash].version** at 0.105229

## Overall stats
- Total unique `(page, script)` calls in the dataset: 6,064,923
- Total unique base locations (netloc): 87,325

### `.ru` site stats
- Total .ru base locations: 2,492
- % of .ru sites(base url): 2.9% (2,492/87,325)

## Among sites that use session replay:
- Total unique calls to SR providers: 95,570
- Total unique base locations using SR: 4,857
- % of calls that are to a session replay provider: 1.6% (95,570/6,064,923)
- % of sites(base url) that uses a session replay provider: 5.6% (4,857/87,325)

### `.ru` sites
- Total .ru sites using SR (unique base locations): 1,634
- given a .ru site, % using a session replay provider: 65.6% (1,634/2,492)
- given a site that uses a session replay provider, % it is .ru: 33.6% (1,634/4,857)

### Http vs Https:
- script_https + location_http = 24,662
- script_https + location_https = 47,716
- script_http + location_http = 23,192
- surprising there are no script_https + location_http
- Among script URLs:
  + http: 23,192
  + https: 24,662 + 47,716 = 72378
  + http % on a session replay call: 24.3% (23,192 / (23,192 + 72378))
- Among location URLs:
  + http: 24,662 + 23,192 = 47,854
  + https: 47,716
  + http % on a session replay calls location: 50.0% (47,854 / (47,854 + 47,716))


```python
## Python 2/3 compatibility.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future import standard_library
standard_library.install_aliases()
from six import text_type

import pandas as pd
import numpy as np
import json
from urllib.parse import urlparse
import requests
from io import StringIO
from pyspark.sql.functions import udf
from pyspark.sql.types import *
```

First, get the list of known session replay providers.


```python
def get_replay_sites():
    """Loads a list of session replay providers from the Princeton WebTAP project,
    which listed sites within the Alexa top 10,000 that show signs of session replay scripts.
    """
    sr_csv_raw = requests.get("https://raw.githubusercontent.com/mozilla/UCOSP-winter-2018_TrackingTechnologies/master/data/sr_site_list.csv")
    sr_csv = pd.read_csv(StringIO(sr_csv_raw.text))
    return list(sr_csv.third_party.unique())
```


```python
replay_sites = get_replay_sites()
```

How many unique domains are there?


```python
len(replay_sites)
```


```python
replay_sites
```

Next, we find instances in the full dataset where the `script_url` is one of the known session replay providers.

First load the dataset from the S3 bucket, and extract the main page URLs and script URLs.


```python
BUCKET = 'safe-ucosp-2017/safe_dataset/v1'
MOUNT = "/mnt/{}".format(BUCKET.replace("/", "-"))
mountPoints = [m.mountPoint for m in dbutils.fs.mounts()]
already_mounted = MOUNT in mountPoints
if not already_mounted:
  dbutils.fs.mount("s3://" + BUCKET, MOUNT)
```


```python
#BUCKET = 'safe-ucosp-2017/safe_dataset/v1'

#ACCESS_KEY = "YOUR-ACCESS-KEY"
#SECRET_KEY = "YOUR-SERCRET-KEY"
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
df = spark.read.parquet("{}/{}".format(MOUNT, 'clean.parquet'))
```

How many distinct script calls are there in the full dataset?


```python
df_urls = df.select("location", "script_url").distinct().cache()
n_rows = df_urls.count()
n_rows
```

Add additional colums for extracted components of the URLs that we will use in the analysis.


```python
def parse_base_url(url):
  """ Extract the base part of a URL (netloc, up until the first '/'). """
  return urlparse(url).netloc
udf_parse_base_url = udf(parse_base_url, StringType())

def parse_url_scheme(url):
  """ Extract the scheme (protocol) from a URL. """
  return urlparse(url).scheme
udf_parse_url_scheme = udf(parse_url_scheme, StringType())

def parse_suffix(url):
  """ Extract the suffix (TLD) from a URL. """
  return url.split(".")[-1]
udf_parse_suffix = udf(parse_suffix, StringType())
```


```python
df_urls = df_urls.withColumn("base_location_url", udf_parse_base_url(df.location))\
  .withColumn("base_script_url", udf_parse_base_url(df.script_url))\
  .withColumn("location_scheme", udf_parse_url_scheme(df.location))\
  .withColumn("script_scheme", udf_parse_url_scheme(df.script_url))
df_urls = df_urls.withColumn("location_suffix", udf_parse_suffix(df_urls.base_location_url))
```


```python
df_urls.show(10)
```

### Session replay scripts

Find the subset that correspond to session replay scripts.


```python
SR_REGEX = "|".join(replay_sites)
```


```python
sites_using_session_replay =  df_urls.filter(df_urls.base_script_url.rlike(SR_REGEX))
```

Overall, how many calls are made to session replay scripts?


```python
sites_using_session_replay.count()
```

How many distinct base URLs are there among the sites in the dataset?


```python
df_urls.dropDuplicates(['base_location_url']).count()
```

And of those using session replay?


```python
sites_using_session_replay.dropDuplicates(['base_location_url']).count()
```

### URL schemes (`http` vs. `https`)

Next, look into which URL schemes are used across main pages and script URLs.


```python
df_urls.groupBy("script_scheme", "location_scheme").count()\
  .orderBy("script_scheme", "location_scheme")\
  .show(n_rows)
```

What is the distribution restricted to sites using session replay?


```python
sites_using_session_replay.groupBy("script_scheme", "location_scheme").count()\
  .orderBy("script_scheme", "location_scheme")\
  .show(n_rows)
```

### URL suffixes (TLDs)

Also, we check the distribution of the URL suffixes (TLDs) for the main pages crawled in the dataset, according to whether or not they use session replay.

Among sites with session replay:


```python
suffixes_session_replay_unique = sites_using_session_replay.dropDuplicates(['base_location_url'])\
  .groupBy("location_suffix").count()
suffixes_session_replay_unique.orderBy(suffixes_session_replay_unique["count"].desc()).show(20)
```

And across the full dataset:


```python
suffixes_unique = df_urls.dropDuplicates(['base_location_url']).groupBy("location_suffix").count()
suffixes_unique.orderBy(suffixes_unique["count"].desc()).show(20)
```


```python
pd_suffixes_session_replay = suffixes_session_replay_unique.withColumnRenamed("count", "count_with_sr").toPandas()
pd_suffixes = suffixes_unique.withColumnRenamed("count", "count_overall").toPandas()
```


```python
pd_suffixes_all = pd_suffixes.join(pd_suffixes_session_replay.set_index("location_suffix"), on="location_suffix")
pd_suffixes_all.fillna(0, inplace=True)
pd_suffixes_all["pct_with_sr"] = pd_suffixes_all["count_with_sr"] / pd_suffixes_all["count_overall"] * 100.0
```


```python
pd_suffixes_all.sort_values("count_overall", ascending=False)[:20]
```
