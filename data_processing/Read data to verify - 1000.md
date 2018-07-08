

```python
from __future__ import unicode_literals
from __future__ import division

import pandas as pd
pd.options.display.max_columns = None

TEST_BUCKET = 'telemetry-test-bucket/birdsarah-test'

N_FILES = 1000
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
    script_col: //s2-prod.manchestereveningnews.co.uk/ not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    
    script_url:  not valid ||
    script_line:  not valid ||
    



```python
bad_count = len(bad_data)
good_count = good_data.count()
print('{:.4%}'.format(bad_count / good_count))
```

    0.0491%



```python
good_data.agg({"call_id": "min"}).collect()
```




    [Row(min(call_id)=u'1_00a944fe4f94fd029c55bc63d2ef7071ff082999a3426d18ec00bbce.json__0')]




```python
good_data.agg({"call_id": "max"}).collect()
```




    [Row(max(call_id)=u'1_ff752c8c306eab630e9b4a68a769cd7bc08fe8c297e304e5b61ca86e.json__9')]




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
print('Missing: {}'.format(count - https_location_count - http_location_count))
print('Proportion https: {:.2%}'.format((https_location_count / good_count)))
```

    67,167 rows
    29,803 http rows
    37,364 https rows
    Missing: 0
    Proportion https: 55.63%



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
    |           g|    2|
    |           w|    2|
    |           i|   22|
    |           t|   26|
    +------------+-----+
    



```python
good_data.groupBy('operation').count().show()
```

    +---------+-----+
    |operation|count|
    +---------+-----+
    |      set|11586|
    |     call|21779|
    |      get|33802|
    +---------+-----+
    



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
    |2017-12-15 22:05:19.181|
    +-----------------------+
    



```python
good_data.agg({"time_stamp": "max"}).show(1, False)
```

    +-----------------------+
    |max(time_stamp)        |
    +-----------------------+
    |2017-12-17 01:19:42.627|
    +-----------------------+
    

