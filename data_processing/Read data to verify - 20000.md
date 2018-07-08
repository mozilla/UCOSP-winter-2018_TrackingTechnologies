

```python
from __future__ import unicode_literals
from __future__ import division

import json
import pandas as pd
import requests

from ast import literal_eval
from jinja2 import Template
from jsonschema import Draft4Validator
from pyspark.sql.types import TimestampType

pd.options.display.max_columns = None

ORIGINAL_BUCKET_NAME = 'safe-ucosp-2017'
TEST_BUCKET = 'telemetry-test-bucket/birdsarah-test'

N_FILES = 20000
```


```python
bad_location_2 = "s3a://{}/bad_{}.parquet".format(TEST_BUCKET, N_FILES)
good_location_2 = "s3a://{}/good_{}.parquet".format(TEST_BUCKET, N_FILES)
```


```python
bad_data = spark.read.parquet(bad_location_2).toPandas()
```


```python
good_data = spark.read.parquet(good_location_2)
```


```python
for val in bad_data.errors:
    print(val)
```

    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //adv.khan.co.kr/RealMedia/ads/adstream_sx.ads/www.khan.co.kr/newspage not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/react-dom not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/react-dom not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //static.parastorage.com/unpkg/santa-core-utils not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=video not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513417079141?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462530296?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513418103857?... not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //common.qunarzz.com/hf_qzz/prd/scripts/default/header_main not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //execution-use.ci360.sas.com/t/s/c/681cceba2200012815576dcc/1513462724613?... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //cdn.jsdelivr.net/g/jquery not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //cdn.jsdelivr.net/g/jquery not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //cdn.jsdelivr.net/g/jquery not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //cdn.jsdelivr.net/g/jquery not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //cdn.jsdelivr.net/g/jquery not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    time_stamp: 2017-12-16T07:04:56+0000 not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: http not valid ||
    script_col: //hdjs.hiido.com/hiido_internal.js?siteid=cr not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line: webpack not valid ||
    script_col: ///./node_modules/ not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    time_stamp: 2017-12-15T22:22:38+0000 not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //enterprise.api-maps.yandex.ru/2.1.56/combine.js?load=5q5j.;. not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //secure.img1-ag.wfcdn.com/lazy_bundler/eng_us/0000000001513380090/init_pag... not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //secure.img1-ag.wfcdn.com/lazy_bundler/eng_us/0000000001513380090/init_pag... not valid ||
    
    script_line: //obj.adman.gr/talos/2017/ledra/13360/index.html?click=http not valid ||
    script_col: //talos.adman.gr/click/ not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //cdn.jsdelivr.net/npm/lazysizes not valid ||
    
    script_url:  not valid ||
    script_line: https not valid ||
    script_col: //unpkg.com/vue not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    



```python
bad_count = len(bad_data)
good_count = good_data.count()
print('{:.4%}'.format(bad_count / good_count))
```

    0.0603%



```python
good_data.agg({"call_id": "min"}).collect()
```




    [Row(min(call_id)=u'1_0003cdd91a5b81c4d58654ca6c8e18b1c60ed6191c3cb849e37a51af.json__0')]




```python
good_data.agg({"call_id": "max"}).collect()
```




    [Row(max(call_id)=u'1_fffc766461372954c01be39f51c0ce49b9370e4d07bc892f296a87c9.json__6')]




```python
http_location = good_data[good_data.location.startswith('http:')]
http_location_count = http_location.count()
https_location = good_data[good_data.location.startswith('https:')]
https_location_count = https_location.count()
```


```python
print('{:,} rows'.format(good_count))
print('{:,} http rows'.format(http_location_count))
print('{:,} https rows'.format(https_location_count))
print('Missing: {}'.format(good_count - https_location_count - http_location_count))
print('Proportion https: {:.2%}'.format((https_location_count / good_count)))
```

    1,138,232 rows
    400,022 http rows
    738,210 https rows
    Missing: 0
    Proportion https: 64.86%



```python
mixed_content = https_location[~https_location.script_url.startswith('https')]
```


```python
initial_char = mixed_content.script_url.substr(0, 1)
mixed_content.withColumn('initial_char', initial_char).groupBy('initial_char').count().show()
```

    +------------+-----+
    |initial_char|count|
    +------------+-----+
    |           l|    3|
    |           0|   18|
    |           m|   12|
    |           f|   45|
    |           _|  246|
    |           e|   20|
    |           C|    1|
    |           /|  478|
    |           w|   48|
    |           i|   53|
    |           r|  836|
    |           t|   52|
    |           s|   67|
    +------------+-----+
    



```python
good_data.groupBy('operation').count().show()
```

    +---------+------+
    |operation| count|
    +---------+------+
    |      set|145683|
    |     call|264675|
    |      get|727874|
    +---------+------+
    



```python
good_data.dtypes
```




    [('argument_0', 'string'),
     ('argument_1', 'string'),
     ('argument_2', 'string'),
     ('argument_3', 'string'),
     ('argument_4', 'string'),
     ('argument_5', 'string'),
     ('argument_6', 'string'),
     ('argument_7', 'string'),
     ('argument_8', 'string'),
     ('arguments', 'string'),
     ('arguments_n_keys', 'bigint'),
     ('call_id', 'string'),
     ('call_stack', 'string'),
     ('crawl_id', 'bigint'),
     ('file_name', 'string'),
     ('func_name', 'string'),
     ('in_iframe', 'boolean'),
     ('location', 'string'),
     ('operation', 'string'),
     ('script_col', 'string'),
     ('script_line', 'string'),
     ('script_loc_eval', 'string'),
     ('script_url', 'string'),
     ('symbol', 'string'),
     ('time_stamp', 'timestamp'),
     ('value', 'string'),
     ('value_1000', 'string'),
     ('value_len', 'int'),
     ('valid', 'boolean'),
     ('errors', 'string')]




```python
good_data.agg({"time_stamp": "min"}).show(1, False)
```

    +-----------------------+
    |min(time_stamp)        |
    +-----------------------+
    |2017-12-15 22:03:00.695|
    +-----------------------+
    



```python
good_data.agg({"time_stamp": "max"}).show(1, False)
```

    +-----------------------+
    |max(time_stamp)        |
    +-----------------------+
    |2017-12-17 01:26:50.584|
    +-----------------------+
    


### Turns out there are some acceptable timestamps that we've rejected


```python
time_stamp_rejects = bad_data[bad_data.errors.str.contains("time_stamp")]
time_stamp_rejects.head(2)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>argument_0</th>
      <th>argument_1</th>
      <th>argument_2</th>
      <th>argument_3</th>
      <th>argument_4</th>
      <th>argument_5</th>
      <th>argument_6</th>
      <th>argument_7</th>
      <th>argument_8</th>
      <th>arguments</th>
      <th>arguments_n_keys</th>
      <th>call_id</th>
      <th>call_stack</th>
      <th>crawl_id</th>
      <th>file_name</th>
      <th>func_name</th>
      <th>in_iframe</th>
      <th>location</th>
      <th>operation</th>
      <th>script_col</th>
      <th>script_line</th>
      <th>script_loc_eval</th>
      <th>script_url</th>
      <th>symbol</th>
      <th>time_stamp</th>
      <th>value</th>
      <th>value_1000</th>
      <th>value_len</th>
      <th>valid</th>
      <th>errors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>528</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>None</td>
      <td>1_81c7ac09151998d58700669645e2dd69891532b068dd...</td>
      <td></td>
      <td>1</td>
      <td>1_81c7ac09151998d58700669645e2dd69891532b068dd...</td>
      <td></td>
      <td>False</td>
      <td>https://www.tripadvisor.co.uk/BusinessAdvantage</td>
      <td>get</td>
      <td>77</td>
      <td>16</td>
      <td></td>
      <td>https://static.tacdn.com/js3/tripadvisor-c-v23...</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T07:04:56+0000</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td></td>
      <td></td>
      <td>False</td>
      <td>time_stamp: 2017-12-16T07:04:56+0000 not valid...</td>
    </tr>
    <tr>
      <th>529</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>None</td>
      <td>1_81c7ac09151998d58700669645e2dd69891532b068dd...</td>
      <td></td>
      <td>1</td>
      <td>1_81c7ac09151998d58700669645e2dd69891532b068dd...</td>
      <td></td>
      <td>False</td>
      <td>https://www.tripadvisor.co.uk/BusinessAdvantage</td>
      <td>get</td>
      <td>140</td>
      <td>16</td>
      <td></td>
      <td>https://static.tacdn.com/js3/tripadvisor-c-v23...</td>
      <td>window.navigator.platform</td>
      <td>2017-12-16T07:04:56+0000</td>
      <td>Linux x86_64</td>
      <td></td>
      <td></td>
      <td>False</td>
      <td>time_stamp: 2017-12-16T07:04:56+0000 not valid...</td>
    </tr>
  </tbody>
</table>
</div>




```python
time_stamp_rejects.file_name.unique()
```




    array([u'1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json',
           u'1_678ed8d87c1e36a2fa5f429400a62161761658737c49bb3765ad7d50.json'], dtype=object)




```python
symbol_counts = pd.read_csv('symbol_counts.csv', names=['symbol', 'count'])
with open('raw_data_schema.template', 'r') as f:
    schema_template = Template(f.read())
schema = literal_eval(
    schema_template.render(
        list_of_symbols=list(symbol_counts.symbol.values)
    )
)

def get_rows_from_s3(file_name):
    file_url = 'https://s3.amazonaws.com/{}/{}'.format(ORIGINAL_BUCKET_NAME, file_name)
    response = requests.get(file_url)
    assert response.status_code == 200
    fix_data = lambda x:  "[" + x[1:-1] + "]"
    data = fix_data(response.content)
    rows = json.loads(data)
    return rows

def validate_and_process_file(file_name):
    validator = Draft4Validator(schema)
    rows = get_rows_from_s3(file_name)

    for i, row in enumerate(rows):
        errors = ''
        valid = validator.is_valid(row)
        
        # If data was not valid, get the error information
        if valid is False:
            for error in validator.iter_errors(row):
                bad_value_truncated = error.instance[:75] + (error.instance[75:] and '...')
                errors += '{}: {} not valid ||\n'.format(
                    error.path[0], bad_value_truncated
                )
        
        row['file_name'] = '{}'.format(file_name)
        row['call_id'] = '{}__{}'.format(file_name, i)
        row['valid'] = valid
        row['errors'] = errors
        
        if valid is True:
            row = process_arguments(row)
        
    return rows
```


```python
rows = validate_and_process_file('1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json')
```


```python
rows[2]
```




    {u'arguments': u'{}',
     u'arguments_n_keys': 0,
     u'call_id': u'1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json__2',
     u'call_stack': u'',
     u'crawl_id': 1,
     u'errors': u'',
     u'file_name': u'1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json',
     u'func_name': u'version<',
     u'in_iframe': False,
     u'location': u'https://www.tripadvisor.co.uk/BusinessAdvantage',
     u'operation': u'get',
     u'script_col': u'1543',
     u'script_line': u'10',
     u'script_loc_eval': u'',
     u'script_url': u'https://static.tacdn.com/js3/mootools-c-v22847647807b.js',
     u'symbol': u'window.navigator.plugins[Shockwave Flash].description',
     u'time_stamp': u'2017-12-16T07:04:56.069Z',
     u'valid': True,
     u'value': u'Shockwave Flash 28.0 r0'}




```python
rows[3]
```




    {u'arguments': u'{}',
     u'arguments_n_keys': 0,
     u'call_id': u'1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json__3',
     u'call_stack': u'',
     u'crawl_id': 1,
     u'errors': u'',
     u'file_name': u'1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json',
     u'func_name': u'',
     u'in_iframe': False,
     u'location': u'https://www.tripadvisor.co.uk/BusinessAdvantage',
     u'operation': u'get',
     u'script_col': u'77',
     u'script_line': u'16',
     u'script_loc_eval': u'',
     u'script_url': u'https://static.tacdn.com/js3/tripadvisor-c-v23806297793b.js',
     u'symbol': u'window.navigator.userAgent',
     u'time_stamp': u'2017-12-16T07:04:56+0000',
     u'valid': True,
     u'value': u'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}




```python
fileRDD = sc.parallelize(['1_81c7ac09151998d58700669645e2dd69891532b068dd552bf77e6bfb.json'])
validated_rows = fileRDD.flatMap(validate_and_process_file)
validated_df = validated_rows.map(lambda x: (x.get('time_stamp', ""),)).toDF(('time_stamp',))
validated_df = validated_df.withColumn('time_stamp', validated_df.time_stamp.cast(TimestampType()))
validated_df.show(100, False)
```

    +-----------------------+
    |time_stamp             |
    +-----------------------+
    |2017-12-16 07:04:56.067|
    |2017-12-16 07:04:56.068|
    |2017-12-16 07:04:56.069|
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56    |
    |2017-12-16 07:04:56.55 |
    |2017-12-16 07:04:56.552|
    |2017-12-16 07:04:56.597|
    |2017-12-16 07:04:56.598|
    |2017-12-16 07:04:56.758|
    |2017-12-16 07:04:56.793|
    |2017-12-16 07:04:56.794|
    |2017-12-16 07:04:56.795|
    |2017-12-16 07:04:56.797|
    |2017-12-16 07:04:56.819|
    |2017-12-16 07:04:56.819|
    |2017-12-16 07:04:56.819|
    |2017-12-16 07:04:56.82 |
    |2017-12-16 07:04:56.82 |
    |2017-12-16 07:04:56.821|
    |2017-12-16 07:04:56.821|
    |2017-12-16 07:04:56.887|
    |2017-12-16 07:04:56.888|
    |2017-12-16 07:04:56.888|
    |2017-12-16 07:04:56.889|
    |2017-12-16 07:04:56.889|
    |2017-12-16 07:04:56.891|
    |2017-12-16 07:04:56.891|
    |2017-12-16 07:04:56.891|
    |2017-12-16 07:04:56.892|
    |2017-12-16 07:04:56.892|
    |2017-12-16 07:04:56.892|
    |2017-12-16 07:04:56.893|
    |2017-12-16 07:04:56.893|
    |2017-12-16 07:04:56.893|
    |2017-12-16 07:04:56.893|
    |2017-12-16 07:04:56.894|
    |2017-12-16 07:04:56.894|
    |2017-12-16 07:04:56.894|
    |2017-12-16 07:04:56.894|
    |2017-12-16 07:04:56.894|
    |2017-12-16 07:04:56.895|
    |2017-12-16 07:04:56.895|
    |2017-12-16 07:04:56.895|
    |2017-12-16 07:04:56.895|
    |2017-12-16 07:04:56.895|
    |2017-12-16 07:04:56.896|
    |2017-12-16 07:04:56.896|
    +-----------------------+
    


### Time to process

14 min for 20,000 rows - 8 workers


```python
multiplier = 2059735 / 20000
multiplier
```




    102.98675




```python
estimated_time_to_complete = (14 * multiplier) / 60
'{:.0f} hours with 8 workers'.format(estimated_time_to_complete)
```




    u'24 hours with 8 workers'




```python
'{:.0f} hours with 30 workers'.format(estimated_time_to_complete / (30/8))
```




    u'6 hours with 30 workers'




```python
good_data.dtypes
```




    [('argument_0', 'string'),
     ('argument_1', 'string'),
     ('argument_2', 'string'),
     ('argument_3', 'string'),
     ('argument_4', 'string'),
     ('argument_5', 'string'),
     ('argument_6', 'string'),
     ('argument_7', 'string'),
     ('argument_8', 'string'),
     ('arguments', 'string'),
     ('arguments_n_keys', 'bigint'),
     ('call_id', 'string'),
     ('call_stack', 'string'),
     ('crawl_id', 'bigint'),
     ('file_name', 'string'),
     ('func_name', 'string'),
     ('in_iframe', 'boolean'),
     ('location', 'string'),
     ('operation', 'string'),
     ('script_col', 'string'),
     ('script_line', 'string'),
     ('script_loc_eval', 'string'),
     ('script_url', 'string'),
     ('symbol', 'string'),
     ('time_stamp', 'timestamp'),
     ('value', 'string'),
     ('value_1000', 'string'),
     ('value_len', 'int'),
     ('valid', 'boolean'),
     ('errors', 'string')]




```python
good_data.agg({"arguments_n_keys": "max"}).show(1, False)
```

    +---------------------+
    |max(arguments_n_keys)|
    +---------------------+
    |6                    |
    +---------------------+
    



```python
max_keys = good_data[good_data.arguments_n_keys == 6].toPandas()
```


```python
max_keys
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>argument_0</th>
      <th>argument_1</th>
      <th>argument_2</th>
      <th>argument_3</th>
      <th>argument_4</th>
      <th>argument_5</th>
      <th>argument_6</th>
      <th>argument_7</th>
      <th>argument_8</th>
      <th>arguments</th>
      <th>arguments_n_keys</th>
      <th>call_id</th>
      <th>call_stack</th>
      <th>crawl_id</th>
      <th>file_name</th>
      <th>func_name</th>
      <th>in_iframe</th>
      <th>location</th>
      <th>operation</th>
      <th>script_col</th>
      <th>script_line</th>
      <th>script_loc_eval</th>
      <th>script_url</th>
      <th>symbol</th>
      <th>time_stamp</th>
      <th>value</th>
      <th>value_1000</th>
      <th>value_len</th>
      <th>valid</th>
      <th>errors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>50</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":50,"1":50,"2":50,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td></td>
      <td>1</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td>e.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://ck101.com/forum-3689-1.html</td>
      <td>call</td>
      <td>17893</td>
      <td>1</td>
      <td></td>
      <td>https://a.breaktime.com.tw/js/au-ac.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 23:57:03.471</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>100</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":100,"1":50,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td></td>
      <td>1</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td>e.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://ck101.com/forum-3689-1.html</td>
      <td>call</td>
      <td>17990</td>
      <td>1</td>
      <td></td>
      <td>https://a.breaktime.com.tw/js/au-ac.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 23:57:03.474</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>75</td>
      <td>100</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":100,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td></td>
      <td>1</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td>e.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://ck101.com/forum-3689-1.html</td>
      <td>call</td>
      <td>18088</td>
      <td>1</td>
      <td></td>
      <td>https://a.breaktime.com.tw/js/au-ac.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 23:57:03.474</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>75</td>
      <td>75</td>
      <td>75</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":75,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td></td>
      <td>1</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td>e.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://ck101.com/forum-3689-1.html</td>
      <td>call</td>
      <td>18172</td>
      <td>1</td>
      <td></td>
      <td>https://a.breaktime.com.tw/js/au-ac.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 23:57:03.475</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>75</td>
      <td>75</td>
      <td>25</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":25,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td></td>
      <td>1</td>
      <td>1_294a4c2b123af5030649020e47d949319dc240aca847...</td>
      <td>e.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://ck101.com/forum-3689-1.html</td>
      <td>call</td>
      <td>18203</td>
      <td>1</td>
      <td></td>
      <td>https://a.breaktime.com.tw/js/au-ac.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 23:57:03.475</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5</th>
      <td>190</td>
      <td>-40</td>
      <td>100</td>
      <td>50</td>
      <td>100</td>
      <td>50</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":190,"1":-40,"2":100,"3":50,"4":100,"5":50}</td>
      <td>6</td>
      <td>1_381930ffb27a30dd209881b2ba58fff64bc0e9f216bf...</td>
      <td></td>
      <td>1</td>
      <td>1_381930ffb27a30dd209881b2ba58fff64bc0e9f216bf...</td>
      <td>T/q&lt;</td>
      <td>False</td>
      <td>http://igg-games.com/donate-share-game-support...</td>
      <td>call</td>
      <td>192</td>
      <td>27</td>
      <td></td>
      <td>http://c.adsco.re/</td>
      <td>CanvasRenderingContext2D.bezierCurveTo</td>
      <td>2017-12-15 23:31:59.464</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>6</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.120</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>7</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.125</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>8</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.126</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>9</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.128</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>10</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.130</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>11</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.132</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>12</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.253</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>13</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.254</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>14</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.254</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>15</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.255</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>16</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.256</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>17</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831853071795...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].arc</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>20952</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.260</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>18</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.343</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>19</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.343</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>20</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.345</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>21</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.346</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>22</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.347</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>23</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.348</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>24</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.386</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>25</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.387</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>26</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.387</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>27</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.388</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>28</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.388</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>29</th>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
      <td>0</td>
      <td>6.2831854820251465</td>
      <td>1</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":0,"1":0,"2":0.5,"3":0,"4":6.2831854820251...</td>
      <td>6</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td></td>
      <td>1</td>
      <td>1_45ed8d8e5d7ae44f7df637a8065eeec682a0366fe90b...</td>
      <td>_[E].rebuildPath</td>
      <td>False</td>
      <td>http://koubei.checheng.com/1868</td>
      <td>call</td>
      <td>25316</td>
      <td>4</td>
      <td></td>
      <td>http://static.checheng.com/common/car/js/echar...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:49:50.389</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>5505</th>
      <td>84.64775402098894</td>
      <td>196.81592886336148</td>
      <td>186.1316818278283</td>
      <td>143.6184089165181</td>
      <td>74.19190420769155</td>
      <td>86.54646566137671</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":84.64775402098894,"1":196.81592886336148,...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.drawBezier</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>1968</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.bezierCurveTo</td>
      <td>2017-12-16 20:26:16.788</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5506</th>
      <td>72.67305576242507</td>
      <td>84.9425258114934</td>
      <td>65.2983826585114</td>
      <td>197.75180481374264</td>
      <td>20.533224707469344</td>
      <td>135.3440408129245</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":72.67305576242507,"1":84.9425258114934,"2...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.drawBezier</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2086</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.bezierCurveTo</td>
      <td>2017-12-16 20:26:16.788</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5507</th>
      <td>99.78121779859066</td>
      <td>43.84683291427791</td>
      <td>0</td>
      <td>187.30061198584735</td>
      <td>86.71133099123836</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":99.78121779859066,"1":43.84683291427791,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.789</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5508</th>
      <td>92.48007093556225</td>
      <td>143.50589658133686</td>
      <td>0</td>
      <td>141.0011308733374</td>
      <td>123.11494695022702</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":92.48007093556225,"1":143.50589658133686,...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.790</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5509</th>
      <td>119.67781600542367</td>
      <td>169.69978888519108</td>
      <td>0</td>
      <td>55.800757091492414</td>
      <td>187.47618519701064</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":119.67781600542367,"1":169.69978888519108...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.793</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5510</th>
      <td>77.31457282789052</td>
      <td>151.0911524295807</td>
      <td>0</td>
      <td>158.7808130774647</td>
      <td>175.85995625704527</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":77.31457282789052,"1":151.0911524295807,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.818</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5511</th>
      <td>136.9108528830111</td>
      <td>129.0849715936929</td>
      <td>0</td>
      <td>193.59733695164323</td>
      <td>79.43848483264446</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":136.9108528830111,"1":129.0849715936929,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.822</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5512</th>
      <td>94.77118658833206</td>
      <td>86.7674290202558</td>
      <td>0</td>
      <td>107.33789433725178</td>
      <td>110.03469391725957</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":94.77118658833206,"1":86.7674290202558,"2...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.823</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5513</th>
      <td>140.83859999664128</td>
      <td>193.86865813285112</td>
      <td>7.880851300433278</td>
      <td>108.51749181747437</td>
      <td>194.3657205440104</td>
      <td>189.48649396188557</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":140.83859999664128,"1":193.86865813285112...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.drawBezier</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>1850</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.bezierCurveTo</td>
      <td>2017-12-16 20:26:16.824</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5514</th>
      <td>46.29692663438618</td>
      <td>96.02760053239763</td>
      <td>18.071448197588325</td>
      <td>57.38146863877773</td>
      <td>32.03057209029794</td>
      <td>121.3908364996314</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":46.29692663438618,"1":96.02760053239763,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.drawBezier</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>1968</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.bezierCurveTo</td>
      <td>2017-12-16 20:26:16.824</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5515</th>
      <td>74.3725301232189</td>
      <td>145.88332064449787</td>
      <td>117.69094513729215</td>
      <td>84.56234405748546</td>
      <td>107.93095245026052</td>
      <td>77.78915576636791</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":74.3725301232189,"1":145.88332064449787,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.drawBezier</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2086</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.bezierCurveTo</td>
      <td>2017-12-16 20:26:16.824</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5516</th>
      <td>42.94575611129403</td>
      <td>170.8670654334128</td>
      <td>0</td>
      <td>96.81937000714242</td>
      <td>18.408052576705813</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":42.94575611129403,"1":170.8670654334128,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.824</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5517</th>
      <td>96.63917194120586</td>
      <td>34.09094577655196</td>
      <td>0</td>
      <td>155.8480861596763</td>
      <td>61.02013890631497</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":96.63917194120586,"1":34.09094577655196,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.827</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5518</th>
      <td>83.46835416741669</td>
      <td>187.6883869059384</td>
      <td>0</td>
      <td>141.01022300310433</td>
      <td>64.86522327177227</td>
      <td>400</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":83.46835416741669,"1":187.6883869059384,"...</td>
      <td>6</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td></td>
      <td>1</td>
      <td>1_495f66899836a2b66eb6016ed8040cfb1a7a8fd4e709...</td>
      <td>a/h.prototype.makeRadialGradient</td>
      <td>False</td>
      <td>https://www.facebook.com/reporterlive</td>
      <td>call</td>
      <td>2676</td>
      <td>21</td>
      <td></td>
      <td>https://static.xx.fbcdn.net/rsrc.php/v3iUNm4/y...</td>
      <td>CanvasRenderingContext2D.createRadialGradient</td>
      <td>2017-12-16 20:26:16.833</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5519</th>
      <td>80</td>
      <td>10</td>
      <td>20</td>
      <td>0</td>
      <td>3.141592653589793</td>
      <td>false</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":80,"1":10,"2":20,"3":0,"4":3.141592653589...</td>
      <td>6</td>
      <td>1_0eea42797501111f11c8658fc58704957cb9cbb7e013...</td>
      <td></td>
      <td>1</td>
      <td>1_0eea42797501111f11c8658fc58704957cb9cbb7e013...</td>
      <td>e[_ac[580]]</td>
      <td>False</td>
      <td>https://www.gucci.com/ca/en/st/capsule/gg-marm...</td>
      <td>call</td>
      <td>51252</td>
      <td>1</td>
      <td></td>
      <td>https://www.gucci.com/_bm/async.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 21:54:52.263</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5520</th>
      <td>50</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":50,"1":50,"2":50,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>166</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:49.313</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5521</th>
      <td>100</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":100,"1":50,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>263</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:49.314</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5522</th>
      <td>75</td>
      <td>100</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":100,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>361</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:49.315</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5523</th>
      <td>75</td>
      <td>75</td>
      <td>75</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":75,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>445</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:49.315</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5524</th>
      <td>75</td>
      <td>75</td>
      <td>25</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":25,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>476</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:49.316</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5525</th>
      <td>50</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":50,"1":50,"2":50,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>166</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:57.286</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5526</th>
      <td>100</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":100,"1":50,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>263</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:57.287</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5527</th>
      <td>75</td>
      <td>100</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":100,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>361</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:57.288</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5528</th>
      <td>75</td>
      <td>75</td>
      <td>75</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":75,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>445</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:57.288</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5529</th>
      <td>75</td>
      <td>75</td>
      <td>25</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":25,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td></td>
      <td>1</td>
      <td>1_62362d2e30718f0b5ae6e5cf5a09a6d02f05dab973fe...</td>
      <td>[5]&lt;/r.exports.getCanvasFp</td>
      <td>True</td>
      <td>https://www.carsales.com.au/cars/ute-bodystyle/</td>
      <td>call</td>
      <td>476</td>
      <td>26</td>
      <td></td>
      <td>https://z.moatads.com/px2/client.js</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 15:51:57.288</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5530</th>
      <td>50</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":50,"1":50,"2":50,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td></td>
      <td>1</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td>a.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://www.elo7.com.br/login.do?redirectAfter...</td>
      <td>call</td>
      <td>17440</td>
      <td>1</td>
      <td></td>
      <td>https://images.elo7.com.br/assets/v3/common/js...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 21:51:13.309</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5531</th>
      <td>100</td>
      <td>50</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":100,"1":50,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td></td>
      <td>1</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td>a.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://www.elo7.com.br/login.do?redirectAfter...</td>
      <td>call</td>
      <td>17537</td>
      <td>1</td>
      <td></td>
      <td>https://images.elo7.com.br/assets/v3/common/js...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 21:51:13.311</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5532</th>
      <td>75</td>
      <td>100</td>
      <td>50</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":100,"2":50,"3":0,"4":6.28318530717...</td>
      <td>6</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td></td>
      <td>1</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td>a.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://www.elo7.com.br/login.do?redirectAfter...</td>
      <td>call</td>
      <td>17635</td>
      <td>1</td>
      <td></td>
      <td>https://images.elo7.com.br/assets/v3/common/js...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 21:51:13.314</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5533</th>
      <td>75</td>
      <td>75</td>
      <td>75</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":75,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td></td>
      <td>1</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td>a.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://www.elo7.com.br/login.do?redirectAfter...</td>
      <td>call</td>
      <td>17719</td>
      <td>1</td>
      <td></td>
      <td>https://images.elo7.com.br/assets/v3/common/js...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 21:51:13.315</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
    <tr>
      <th>5534</th>
      <td>75</td>
      <td>75</td>
      <td>25</td>
      <td>0</td>
      <td>6.283185307179586</td>
      <td>true</td>
      <td></td>
      <td></td>
      <td></td>
      <td>{"0":75,"1":75,"2":25,"3":0,"4":6.283185307179...</td>
      <td>6</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td></td>
      <td>1</td>
      <td>1_3f9be144934ec4a61e0c2fdad191949af54fc1b3ac2d...</td>
      <td>a.prototype.getCanvasFp</td>
      <td>False</td>
      <td>https://www.elo7.com.br/login.do?redirectAfter...</td>
      <td>call</td>
      <td>17750</td>
      <td>1</td>
      <td></td>
      <td>https://images.elo7.com.br/assets/v3/common/js...</td>
      <td>CanvasRenderingContext2D.arc</td>
      <td>2017-12-16 21:51:13.315</td>
      <td></td>
      <td></td>
      <td>0</td>
      <td>True</td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>5535 rows × 30 columns</p>
</div>




```python
good_data.groupBy('in_iframe').count().show()
```

    +---------+------+
    |in_iframe| count|
    +---------+------+
    |     true|229460|
    |    false|908772|
    +---------+------+
    



```python
good_data.groupBy('symbol').count().orderBy('count', ascending=False).show(100, False)
```

    +---------------------------------------------------------------------+------+
    |symbol                                                               |count |
    +---------------------------------------------------------------------+------+
    |window.document.cookie                                               |341035|
    |window.navigator.userAgent                                           |147308|
    |window.Storage.getItem                                               |104671|
    |window.localStorage                                                  |87653 |
    |window.sessionStorage                                                |41690 |
    |window.Storage.setItem                                               |39289 |
    |window.Storage.removeItem                                            |26465 |
    |window.name                                                          |23416 |
    |CanvasRenderingContext2D.fillStyle                                   |19133 |
    |window.navigator.plugins[Shockwave Flash].description                |17791 |
    |window.screen.colorDepth                                             |14256 |
    |window.navigator.appName                                             |13198 |
    |CanvasRenderingContext2D.fill                                        |11968 |
    |CanvasRenderingContext2D.save                                        |11482 |
    |window.navigator.language                                            |11479 |
    |window.navigator.platform                                            |11358 |
    |CanvasRenderingContext2D.restore                                     |11340 |
    |CanvasRenderingContext2D.font                                        |9405  |
    |CanvasRenderingContext2D.stroke                                      |9059  |
    |window.navigator.plugins[Shockwave Flash].name                       |8846  |
    |CanvasRenderingContext2D.lineWidth                                   |8760  |
    |CanvasRenderingContext2D.strokeStyle                                 |8407  |
    |HTMLCanvasElement.width                                              |7609  |
    |CanvasRenderingContext2D.fillRect                                    |7541  |
    |HTMLCanvasElement.height                                             |7450  |
    |window.navigator.cookieEnabled                                       |6961  |
    |window.Storage.key                                                   |6910  |
    |window.Storage.length                                                |6829  |
    |HTMLCanvasElement.getContext                                         |6708  |
    |window.navigator.appVersion                                          |6689  |
    |CanvasRenderingContext2D.fillText                                    |6614  |
    |window.navigator.doNotTrack                                          |5129  |
    |CanvasRenderingContext2D.arc                                         |5107  |
    |CanvasRenderingContext2D.textBaseline                                |5064  |
    |HTMLCanvasElement.style                                              |4847  |
    |window.navigator.vendor                                              |4610  |
    |CanvasRenderingContext2D.textAlign                                   |4525  |
    |CanvasRenderingContext2D.measureText                                 |3830  |
    |CanvasRenderingContext2D.lineCap                                     |2671  |
    |CanvasRenderingContext2D.shadowBlur                                  |2664  |
    |window.navigator.product                                             |2636  |
    |CanvasRenderingContext2D.shadowColor                                 |2462  |
    |HTMLCanvasElement.nodeType                                           |2287  |
    |CanvasRenderingContext2D.shadowOffsetY                               |2274  |
    |CanvasRenderingContext2D.shadowOffsetX                               |2270  |
    |window.navigator.mimeTypes[application/x-shockwave-flash].type       |2235  |
    |window.navigator.plugins[Shockwave Flash].filename                   |2172  |
    |window.navigator.languages                                           |2021  |
    |CanvasRenderingContext2D.lineJoin                                    |1943  |
    |window.navigator.plugins[Shockwave Flash].length                     |1932  |
    |CanvasRenderingContext2D.globalCompositeOperation                    |1895  |
    |CanvasRenderingContext2D.createRadialGradient                        |1726  |
    |window.navigator.mimeTypes[application/futuresplash].type            |1687  |
    |window.screen.pixelDepth                                             |1540  |
    |CanvasRenderingContext2D.scale                                       |1507  |
    |window.navigator.plugins[Shockwave Flash].version                    |1506  |
    |HTMLCanvasElement.toDataURL                                          |1440  |
    |CanvasRenderingContext2D.bezierCurveTo                               |1390  |
    |CanvasRenderingContext2D.miterLimit                                  |1276  |
    |window.navigator.onLine                                              |1169  |
    |HTMLCanvasElement.nodeName                                           |1077  |
    |window.navigator.mimeTypes[application/futuresplash].suffixes        |991   |
    |window.navigator.mimeTypes[application/x-shockwave-flash].suffixes   |991   |
    |window.Storage.hasOwnProperty                                        |932   |
    |CanvasRenderingContext2D.rect                                        |851   |
    |RTCPeerConnection.localDescription                                   |789   |
    |CanvasRenderingContext2D.arcTo                                       |780   |
    |CanvasRenderingContext2D.createLinearGradient                        |773   |
    |window.navigator.mimeTypes[application/futuresplash].description     |740   |
    |window.navigator.mimeTypes[application/x-shockwave-flash].description|740   |
    |window.navigator.productSub                                          |736   |
    |HTMLCanvasElement.ownerDocument                                      |625   |
    |CanvasRenderingContext2D.rotate                                      |625   |
    |HTMLCanvasElement.className                                          |597   |
    |window.navigator.oscpu                                               |577   |
    |window.navigator.appCodeName                                         |523   |
    |HTMLCanvasElement.parentNode                                         |519   |
    |CanvasRenderingContext2D.strokeRect                                  |513   |
    |CanvasRenderingContext2D.getImageData                                |504   |
    |window.navigator.geolocation                                         |429   |
    |HTMLCanvasElement.tagName                                            |424   |
    |HTMLCanvasElement.id                                                 |407   |
    |CanvasRenderingContext2D.clip                                        |388   |
    |HTMLCanvasElement.setAttribute                                       |356   |
    |RTCPeerConnection.onicecandidate                                     |316   |
    |window.navigator.vendorSub                                           |279   |
    |window.navigator.buildID                                             |250   |
    |HTMLCanvasElement.addEventListener                                   |237   |
    |HTMLCanvasElement.attributes                                         |221   |
    |HTMLCanvasElement.onselectstart                                      |202   |
    |HTMLCanvasElement.classList                                          |202   |
    |CanvasRenderingContext2D.putImageData                                |199   |
    |HTMLCanvasElement.getElementsByTagName                               |193   |
    |HTMLCanvasElement.getAttribute                                       |176   |
    |HTMLCanvasElement.draggable                                          |169   |
    |RTCPeerConnection.iceGatheringState                                  |142   |
    |RTCPeerConnection.createDataChannel                                  |140   |
    |RTCPeerConnection.createOffer                                        |131   |
    |RTCPeerConnection.signalingState                                     |130   |
    |RTCPeerConnection.remoteDescription                                  |130   |
    +---------------------------------------------------------------------+------+
    only showing top 100 rows
    



```python
locations = good_data.groupBy('location').count()
print(locations.count())
```

    19997



```python
file_names = good_data.groupBy('file_name').count()
print(file_names.count())
```

    19997

