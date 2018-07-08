

```python
import dask.dataframe as dd
import dask.multiprocessing
import json
import numpy as np
import pandas as pd

from ast import literal_eval
from dask.delayed import delayed
from dask.diagnostics import ProgressBar
from datetime import datetime
from pandas.api.types import CategoricalDtype
from path import Path

PROJECT_DIR = Path.getcwd().parent  # Could assert some things here to check we got the right path
CACHE_OLD_DIR = Path.joinpath(PROJECT_DIR, 'cache')  # Where the originally downloaded files are
CACHE_NEW_DIR = Path.joinpath(PROJECT_DIR, 'cache_new.parquet')  # Where the parquet files are going to live

N_PARTITIONS = 2999  # This was decided after trial and error
```


```python
# Force into multiprocessing - works well for our data
dask.set_options(get=dask.multiprocessing.get)
```




    <dask.context.set_options at 0x7f489bc531d0>




```python
operation_categorical_type = CategoricalDtype(categories=["get", "set", "call", "set (failed)"])

symbol_counts = pd.read_csv('symbol_counts.csv', names=['symbol', 'count'])
symbol_categorical_type = CategoricalDtype(categories=symbol_counts.symbol.values)
```

## Make even(ish) partitions based on call counts.

This still doesn't make them even due to "value" field being so variable. But it's better than just slicing up the list of files.


```python
index_with_counts = pd.read_csv('file_index_with_counts.csv.gz')
index_with_counts = index_with_counts.rename(columns=dict(crawl_id='call_count'))
index_with_counts = index_with_counts.sort_values('file_name')
index_with_counts.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>file_name</th>
      <th>call_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1_00001314358470f0c99914d5c7af0cd89248e54883ac...</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1_000014b53a60c645e3ac9bde6bae020430c930b3cc59...</td>
      <td>30</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1_00003e3765a73da45db5265de2b22424e025d61380f7...</td>
      <td>4</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1_00004636d8310609e710934f194bfb41a5f0ac7ed5e0...</td>
      <td>78</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1_00004b8315fd1954f06dd80b85ebc61f7ab006785cd3...</td>
      <td>64</td>
    </tr>
  </tbody>
</table>
</div>




```python
index_with_counts['cum_call_count'] = index_with_counts.call_count.cumsum()
index_with_counts.head(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>file_name</th>
      <th>call_count</th>
      <th>cum_call_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1_00001314358470f0c99914d5c7af0cd89248e54883ac...</td>
      <td>6</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1_000014b53a60c645e3ac9bde6bae020430c930b3cc59...</td>
      <td>30</td>
      <td>36</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1_00003e3765a73da45db5265de2b22424e025d61380f7...</td>
      <td>4</td>
      <td>40</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1_00004636d8310609e710934f194bfb41a5f0ac7ed5e0...</td>
      <td>78</td>
      <td>118</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1_00004b8315fd1954f06dd80b85ebc61f7ab006785cd3...</td>
      <td>64</td>
      <td>182</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1_00004cab8dbbf5a10ec8f4fe3d7a816c69a69ff6dcfb...</td>
      <td>32</td>
      <td>214</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1_000052c9c1a2bcf00536c9b3f4132222339f74379067...</td>
      <td>10</td>
      <td>224</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1_000055875d91ca961b32d7e535548ed87e50de528399...</td>
      <td>27</td>
      <td>251</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1_00005baacbbbd2ce9442b6afa0c914506329f669a5b0...</td>
      <td>102</td>
      <td>353</td>
    </tr>
    <tr>
      <th>9</th>
      <td>1_00006011493ed94fb8010cead84ee610cdbece5de961...</td>
      <td>3</td>
      <td>356</td>
    </tr>
  </tbody>
</table>
</div>




```python
total_calls = index_with_counts.cum_call_count.max()
n_per_partition = total_calls / N_PARTITIONS
print('Total calls: {:,}'.format(total_calls))
print('Calls per partition: ~{:,.0f}'.format(n_per_partition))
```

    Total calls: 113,790,736
    Calls per partition: ~37,943



```python
index_with_counts['planned_partition'] = np.floor_divide(index_with_counts.cum_call_count, n_per_partition)
index_with_counts.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>file_name</th>
      <th>call_count</th>
      <th>cum_call_count</th>
      <th>planned_partition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1_00001314358470f0c99914d5c7af0cd89248e54883ac...</td>
      <td>6</td>
      <td>6</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1_000014b53a60c645e3ac9bde6bae020430c930b3cc59...</td>
      <td>30</td>
      <td>36</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1_00003e3765a73da45db5265de2b22424e025d61380f7...</td>
      <td>4</td>
      <td>40</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1_00004636d8310609e710934f194bfb41a5f0ac7ed5e0...</td>
      <td>78</td>
      <td>118</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1_00004b8315fd1954f06dd80b85ebc61f7ab006785cd3...</td>
      <td>64</td>
      <td>182</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
index_with_counts.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>file_name</th>
      <th>call_count</th>
      <th>cum_call_count</th>
      <th>planned_partition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>875367</th>
      <td>1_ffffe72029d7bfc78edecbb36680b3bf1684792e0e9c...</td>
      <td>9</td>
      <td>113790675</td>
      <td>2998.0</td>
    </tr>
    <tr>
      <th>875368</th>
      <td>1_ffffe728e149d0187f4c19aa72e0702399ee4146e631...</td>
      <td>2</td>
      <td>113790677</td>
      <td>2998.0</td>
    </tr>
    <tr>
      <th>875369</th>
      <td>1_ffffefa6429f4c246f35332bc97c0c611aff1e5f2f87...</td>
      <td>8</td>
      <td>113790685</td>
      <td>2998.0</td>
    </tr>
    <tr>
      <th>875370</th>
      <td>1_fffff099cd4647207aeb9433939c99d26e85adfa8c7b...</td>
      <td>1</td>
      <td>113790686</td>
      <td>2998.0</td>
    </tr>
    <tr>
      <th>875371</th>
      <td>1_fffffec2c395d8cad2f6daabc097cb5322148f73e0b3...</td>
      <td>50</td>
      <td>113790736</td>
      <td>2998.0</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Check penultimate break
rough_break = index_with_counts.cum_call_count.values[-1] - n_per_partition
index_with_counts[
    (index_with_counts.cum_call_count < rough_break + 300) &
    (index_with_counts.cum_call_count > rough_break - 200)
]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>file_name</th>
      <th>call_count</th>
      <th>cum_call_count</th>
      <th>planned_partition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>874771</th>
      <td>1_ffebe26b2675d2bbd4ea87bfb0e96108089183e4e8c3...</td>
      <td>80</td>
      <td>113752600</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874772</th>
      <td>1_ffebe2c957605eb75994ac5920c276ccb84ccd96af4c...</td>
      <td>2</td>
      <td>113752602</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874773</th>
      <td>1_ffebe53d510bb0f2697cd57ffac52783584174a2abcf...</td>
      <td>5</td>
      <td>113752607</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874774</th>
      <td>1_ffebe61fc50a3c8727378eaafc46d12c5b8addbfecca...</td>
      <td>1</td>
      <td>113752608</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874775</th>
      <td>1_ffebee8e62264d7477d826c885497dfa339a2a719012...</td>
      <td>6</td>
      <td>113752614</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874776</th>
      <td>1_ffebfb26e0b93fe8af36cc62c8b14167edd4e2e4aa14...</td>
      <td>1</td>
      <td>113752615</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874777</th>
      <td>1_ffec021028079880f4fa67f6ca30faa7c20ecd12455f...</td>
      <td>2</td>
      <td>113752617</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874778</th>
      <td>1_ffec0573acf6a05e4fe5ec0c854e499116c45f50b88d...</td>
      <td>12</td>
      <td>113752629</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874779</th>
      <td>1_ffec18e50e877e5ac018736e6162d6043244ba544d3d...</td>
      <td>4</td>
      <td>113752633</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874780</th>
      <td>1_ffec222605f05bc6c8a95ff09a8659626c1ae454e77d...</td>
      <td>16</td>
      <td>113752649</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874781</th>
      <td>1_ffec2ab591b803cc9050298a0d390fe74856a175054b...</td>
      <td>20</td>
      <td>113752669</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874782</th>
      <td>1_ffec3011fbb5e9932b5cc7c9af206dac4792f0edc3e0...</td>
      <td>21</td>
      <td>113752690</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874783</th>
      <td>1_ffec36600e1b6eac11c835b4a46a65a3de32e218ba0f...</td>
      <td>44</td>
      <td>113752734</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874784</th>
      <td>1_ffec41acdd336ca44b20f6218a3c46fc592d97788680...</td>
      <td>5</td>
      <td>113752739</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874785</th>
      <td>1_ffec46af1ebde44a1e712f74d1adb294e755a959988a...</td>
      <td>3</td>
      <td>113752742</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874786</th>
      <td>1_ffec57a85f9eb61b2ec1c17e415c99541add9130bece...</td>
      <td>1</td>
      <td>113752743</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874787</th>
      <td>1_ffec6cf77814d756b2ae09dd2ed6318377ca2422e742...</td>
      <td>4</td>
      <td>113752747</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874788</th>
      <td>1_ffec85e23b35e2f4af2a05616010755c984e4370f3fe...</td>
      <td>2</td>
      <td>113752749</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874789</th>
      <td>1_ffec898effabd6d358be9340d62298debf89feed0250...</td>
      <td>1</td>
      <td>113752750</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874790</th>
      <td>1_ffec8a44af60bc3372f48fc9a2e3aac1375ff4e54e0e...</td>
      <td>4</td>
      <td>113752754</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874791</th>
      <td>1_ffec8c0e7ee9566fdf91240e9bcbf1088bd82e80344d...</td>
      <td>2</td>
      <td>113752756</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874792</th>
      <td>1_ffec8c498005491870ca3b3c6e36e35fe0523e7977b4...</td>
      <td>4</td>
      <td>113752760</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874793</th>
      <td>1_ffec95dc9e01c1dd952265e58be3318ae8e4c4a98a41...</td>
      <td>2</td>
      <td>113752762</td>
      <td>2997.0</td>
    </tr>
    <tr>
      <th>874794</th>
      <td>1_ffec9cecff312c4106f22ff39db4f86940708eee16d9...</td>
      <td>56</td>
      <td>113752818</td>
      <td>2998.0</td>
    </tr>
    <tr>
      <th>874795</th>
      <td>1_ffeca301dc407aca04e35ad46472c9c02ed138691935...</td>
      <td>230</td>
      <td>113753048</td>
      <td>2998.0</td>
    </tr>
    <tr>
      <th>874796</th>
      <td>1_ffeca73b505128a53e6bfd88fb711b045fea79350a58...</td>
      <td>2</td>
      <td>113753050</td>
      <td>2998.0</td>
    </tr>
  </tbody>
</table>
</div>



## Process data


```python
fix_data = lambda x:  "[" + x[1:-1] + "]"

def get_files_for_split(split_number):
    filtered = index_with_counts[index_with_counts.planned_partition == split_number]
    return filtered.file_name.values
    
def get_data_from_file(file_name):
    fp = Path.joinpath(CACHE_OLD_DIR, file_name)
    with open(fp, 'r') as f:
        raw_data = f.read()
    data = json.loads(fix_data(raw_data))
    return data

def convert_to_dict(item):
    item = item.replace('false', 'False')
    item = item.replace('true', 'True')
    item = item.replace('null', 'None')
    try:
        return literal_eval(item)
    except:
        return {}

def make_df_from_data(data, file_name):
    df = pd.DataFrame.from_records(data)

    # Make script_col and script_line numeric, an drop rows with bad values
    df['script_col'] = pd.to_numeric(df.script_col, errors='coerce')
    df['script_line'] = pd.to_numeric(df.script_line, errors='coerce')
    df = df.dropna(subset=['script_col', 'script_line'])
    df['script_col'] = df['script_col'].astype(int)
    df['script_line'] = df['script_line'].astype(int)
    
    # Make sure arguments column is always present
    if 'arguments' not in df.columns:
        df['arguments'] = "{}"
    
    # Parse arguments
    df['arguments'] = df.arguments.astype(str)
    df['_arg_as_dict'] = df.arguments.apply(convert_to_dict)
    df['arguments_n_keys'] = df._arg_as_dict.apply(len).astype(int)

    # Based on previous computation of max_keys_count
    for n in range(9):
        key = 'argument_{}'.format(n)
        df[key] = df._arg_as_dict.apply(lambda x: x.get(str(n))).astype(str)
    df = df.drop('_arg_as_dict', axis=1)
    
    # Add file_name column
    df['file_name'] = file_name
    
    # Make a unique call_id
    df['call_id'] = df.file_name.str.cat(df.index.astype(str), sep='__')
    
    # Make a value len and initial value
    df['value_len'] = df.value.str.len()
    df['value_1000'] = df.value.str.slice(0, 1000)
    
    # Make a timestamp
    df['time_stamp'] = pd.to_datetime(df.time_stamp, errors='coerce')
    
    # Make categorical
    df['operation'] = df.operation.astype(operation_categorical_type)
    df['symbol'] = df.symbol.astype(symbol_categorical_type)
    
    # Set call_id as index
    df = df.set_index('call_id')
    
    # Reorder columns so consistent (keeps parquet happy)
    df = df.sort_index(axis='columns')
    return df

def get_df(file_name):
    data = get_data_from_file(file_name)
    df = make_df_from_data(data, file_name)
    return df
```

### Test single write and read (with pandas)


```python
%%time
dfs = []
for file_name in get_files_for_split(100):
    dfs.append(get_df(file_name))
```

    CPU times: user 12 s, sys: 173 ms, total: 12.2 s
    Wall time: 12.8 s



```python
%%time
all_df = pd.concat(dfs)
```

    CPU times: user 1.38 s, sys: 17.9 ms, total: 1.4 s
    Wall time: 1.4 s



```python
len(all_df)
```




    37702




```python
all_df.dtypes
```




    argument_0                  object
    argument_1                  object
    argument_2                  object
    argument_3                  object
    argument_4                  object
    argument_5                  object
    argument_6                  object
    argument_7                  object
    argument_8                  object
    arguments                   object
    arguments_n_keys             int64
    call_stack                  object
    crawl_id                     int64
    file_name                   object
    func_name                   object
    in_iframe                     bool
    location                    object
    operation                 category
    script_col                   int64
    script_line                  int64
    script_loc_eval             object
    script_url                  object
    symbol                    category
    time_stamp          datetime64[ns]
    value                       object
    value_1000                  object
    value_len                    int64
    dtype: object




```python
all_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <th>...</th>
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
    </tr>
    <tr>
      <th>call_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1_08747931a7eb972db94f687affd20af95c8b54af91f8bb979b23f0c4.json__0</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>7726</td>
      <td>2</td>
      <td></td>
      <td>http://www.82cook.com/js/jquery-1.6.2.min.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16 23:20:39.271</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_08747931a7eb972db94f687affd20af95c8b54af91f8bb979b23f0c4.json__1</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>5</td>
      <td>64</td>
      <td></td>
      <td>http://www.82cook.com/entiz/enti.php?bn=23</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16 23:20:39.320</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_08747931a7eb972db94f687affd20af95c8b54af91f8bb979b23f0c4.json__2</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>5</td>
      <td>170</td>
      <td></td>
      <td>http://www.82cook.com/entiz/enti.php?bn=23</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16 23:20:39.325</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_08747931a7eb972db94f687affd20af95c8b54af91f8bb979b23f0c4.json__3</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>832</td>
      <td>27</td>
      <td></td>
      <td>http://www.google-analytics.com/ga.js</td>
      <td>window.document.cookie</td>
      <td>2017-12-16 23:20:39.613</td>
      <td>PHPSESSID=k5uklrf1t9151jrpcv8q7ig2f2</td>
      <td>PHPSESSID=k5uklrf1t9151jrpcv8q7ig2f2</td>
      <td>36</td>
    </tr>
    <tr>
      <th>1_08747931a7eb972db94f687affd20af95c8b54af91f8bb979b23f0c4.json__4</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>150</td>
      <td>29</td>
      <td></td>
      <td>http://www.google-analytics.com/ga.js</td>
      <td>window.screen.colorDepth</td>
      <td>2017-12-16 23:20:39.614</td>
      <td>24</td>
      <td>24</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 27 columns</p>
</div>




```python
%%time
all_df.to_parquet(
    Path.joinpath('test.parquet'),
    compression='snappy',
    engine='fastparquet',
    write_index=True
)
```

    CPU times: user 755 ms, sys: 16.5 ms, total: 772 ms
    Wall time: 775 ms



```python
%%time
df = pd.read_parquet(
    Path.joinpath('test.parquet'), 
)
```

    CPU times: user 511 ms, sys: 16.8 ms, total: 528 ms
    Wall time: 537 ms



```python
df.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <th>...</th>
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
    </tr>
    <tr>
      <th>call_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1_08891a2d9c077343b114b865bde7584a7c80294f2c24789c3b186490.json__1</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>714</td>
      <td>71</td>
      <td></td>
      <td>https://platform.instagram.com/en_US/embeds.js</td>
      <td>window.name</td>
      <td>2017-12-16 22:27:59.818</td>
      <td></td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>1_08891a2d9c077343b114b865bde7584a7c80294f2c24789c3b186490.json__2</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>716</td>
      <td>71</td>
      <td></td>
      <td>https://platform.instagram.com/en_US/embeds.js</td>
      <td>window.name</td>
      <td>2017-12-16 22:27:59.819</td>
      <td></td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>1_08891a2d9c077343b114b865bde7584a7c80294f2c24789c3b186490.json__3</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>57</td>
      <td>76</td>
      <td></td>
      <td>https://platform.instagram.com/en_US/embeds.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16 22:27:59.819</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_08891a2d9c077343b114b865bde7584a7c80294f2c24789c3b186490.json__4</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>333</td>
      <td>122</td>
      <td></td>
      <td>https://apis.google.com/_/scs/apps-static/_/js...</td>
      <td>window.name</td>
      <td>2017-12-16 22:28:00.397</td>
      <td></td>
      <td></td>
      <td>0</td>
    </tr>
    <tr>
      <th>1_08891a2d9c077343b114b865bde7584a7c80294f2c24789c3b186490.json__5</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>3798</td>
      <td>23</td>
      <td></td>
      <td>https://cdns.gigya.com/js/gigya.js?apiKey=3_zF...</td>
      <td>window.document.cookie</td>
      <td>2017-12-16 22:28:00.523</td>
      <td>iduser=172.16.1.150.1513463269507053; __gads=I...</td>
      <td>iduser=172.16.1.150.1513463269507053; __gads=I...</td>
      <td>621</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 27 columns</p>
</div>




```python
df.dtypes
```




    argument_0                  object
    argument_1                  object
    argument_2                  object
    argument_3                  object
    argument_4                  object
    argument_5                  object
    argument_6                  object
    argument_7                  object
    argument_8                  object
    arguments                   object
    arguments_n_keys             int64
    call_stack                  object
    crawl_id                     int64
    file_name                   object
    func_name                   object
    in_iframe                     bool
    location                    object
    operation                 category
    script_col                   int64
    script_line                  int64
    script_loc_eval             object
    script_url                  object
    symbol                    category
    time_stamp          datetime64[ns]
    value                       object
    value_1000                  object
    value_len                    int64
    dtype: object



### Make meta and divisions


```python
meta = pd.DataFrame(columns=[
    'argument_0',
    'argument_1',
    'argument_2',
    'argument_3',
    'argument_4',
    'argument_5',
    'argument_6',
    'argument_7',
    'argument_8',
    'arguments',
    'arguments_n_keys',
    'call_id',
    'call_stack',
    'crawl_id',
    'file_name',
    'func_name',
    'in_iframe',
    'location',
    'operation',
    'script_col',
    'script_line',
    'script_loc_eval',
    'script_url',
    'symbol',
    'time_stamp',
    'value',
    'value_1000',
    'value_len'
], dtype='object')
meta = meta.set_index('call_id')

meta.arguments_n_keys = meta.arguments_n_keys.astype(np.int64)
meta.crawl_id = meta.crawl_id.astype(np.int64)
meta.in_iframe = meta.in_iframe.astype(bool)
meta.operation = meta.operation.astype(operation_categorical_type)
meta.script_col = meta.script_col.astype(np.int64)
meta.script_line = meta.script_line.astype(np.int64)
meta.symbol = meta.symbol.astype(symbol_categorical_type)
meta.time_stamp = meta.time_stamp.astype('datetime64[ns]')
meta.value_len = meta.value_len.astype(np.int64)

print(meta.dtypes)
print(meta.index)
```

    argument_0                  object
    argument_1                  object
    argument_2                  object
    argument_3                  object
    argument_4                  object
    argument_5                  object
    argument_6                  object
    argument_7                  object
    argument_8                  object
    arguments                   object
    arguments_n_keys             int64
    call_stack                  object
    crawl_id                     int64
    file_name                   object
    func_name                   object
    in_iframe                     bool
    location                    object
    operation                 category
    script_col                   int64
    script_line                  int64
    script_loc_eval             object
    script_url                  object
    symbol                    category
    time_stamp          datetime64[ns]
    value                       object
    value_1000                  object
    value_len                    int64
    dtype: object
    Index([], dtype='object', name='call_id')



```python
assert np.all(meta.dtypes.keys() == df.dtypes.keys())
```


```python
divisions = [get_files_for_split(n)[0] for n in range(N_PARTITIONS)] + ['2']
print('{} divisions'.format(len(divisions)))
divisions[-5:]
```

    3000 divisions





    ['1_ffa165173a4c48978172af7e6e1f0c5848edb9904dfcc8ce5d5a33bb.json',
     '1_ffba2e877be3a027c6fde6f6fe77d27f61acd59e6832de0282e17a8d.json',
     '1_ffd18cfc37f4d0b14c86ed568b3db6d84f41ee7f237a008ba010fc67.json',
     '1_ffec9cecff312c4106f22ff39db4f86940708eee16d980674875c05a.json',
     '2']




```python
with open('divisions.txt', 'w') as f:
    f.write("\r\n".join(divisions))
```

## Run all


```python
def process_chunk(split_number):
    dfs = []
    files = get_files_for_split(split_number)
    for file_name in files:
        dfs.append(get_df(file_name))
    all_df = pd.concat(dfs)
    return all_df
```


```python
%%time
dfs = [delayed(process_chunk)(split_number) for split_number in range(N_PARTITIONS)]
```

    CPU times: user 148 ms, sys: 7.03 ms, total: 155 ms
    Wall time: 152 ms



```python
df = dd.from_delayed(dfs, meta=meta, divisions=divisions)
out = df.to_parquet(
    CACHE_NEW_DIR, compression='snappy', engine='fastparquet', write_index=True, compute=False
)
```


```python
len(df.dask)
```




    5998




```python
# Used ~10GB RAM on my machine
with ProgressBar():
    out.compute()
```

    [########################################] | 100% Completed |  7hr 34min 30.5s


## Test run data


```python
# Based on sample of 5 - basic data
print('{} hours to finish'.format(((3000 / 5) * 0.5) / 60))

# Based on sample of 5 - all data
print('{} hours to finish'.format(((3000 / 5) * 1.8) / 60))

# Based on a sample of 10 - all data (multiprocessing)
print('{} hours to finish'. format(((3000 / 10) * 2) / 60))
```

    5.0 hours to finish
    18.0 hours to finish
    10.0 hours to finish



```python
df = dd.read_parquet(CACHE_NEW_DIR)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
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
      <th>...</th>
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
    </tr>
    <tr>
      <th>call_id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__0</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>4206</td>
      <td>2</td>
      <td></td>
      <td>https://mech.iitm.ac.in/meiitm/wp-includes/js/...</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-15 23:52:40.662</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__1</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>2640</td>
      <td>11</td>
      <td></td>
      <td>https://mech.iitm.ac.in/meiitm/wp-includes/js/...</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-15 23:52:40.742</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__2</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>6226</td>
      <td>4</td>
      <td></td>
      <td>https://mech.iitm.ac.in/meiitm/wp-admin/js/iri...</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-15 23:52:40.751</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>68</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__3</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>6262</td>
      <td>4</td>
      <td></td>
      <td>https://mech.iitm.ac.in/meiitm/wp-admin/js/iri...</td>
      <td>window.navigator.appName</td>
      <td>2017-12-15 23:52:40.752</td>
      <td>Netscape</td>
      <td>Netscape</td>
      <td>8</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__4</th>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>{}</td>
      <td>...</td>
      <td>get</td>
      <td>66</td>
      <td>1</td>
      <td></td>
      <td>https://mech.iitm.ac.in/meiitm/wp-includes/js/...</td>
      <td>window.navigator.appVersion</td>
      <td>2017-12-15 23:52:45.707</td>
      <td>5.0 (X11)</td>
      <td>5.0 (X11)</td>
      <td>9</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 27 columns</p>
</div>




```python
df = dd.read_parquet(CACHE_NEW_DIR, columns='crawl_id')
df.head()
```




    call_id
    1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__0    1
    1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__1    1
    1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__2    1
    1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__3    1
    1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__4    1
    Name: crawl_id, dtype: int64




```python
%%time
df.value_counts().compute()
```

    CPU times: user 18.6 s, sys: 576 ms, total: 19.2 s
    Wall time: 21.8 s





    1    113718973
    Name: crawl_id, dtype: int64




```python
with ProgressBar():
    df = df.reset_index()
    df = df.drop('crawl_id', axis='columns')
    df.to_parquet('index.parquet', compression='snappy', engine='fastparquet')
```

    [########################################] | 100% Completed | 34.3s



```python
with ProgressBar():
    random_indexes = df.sample(frac=0.001).compute()
```

    [########################################] | 100% Completed | 23.3s



```python
random_indexes = random_indexes.reset_index()
random_indexes = random_indexes.drop('crawl_id', axis='columns')
print(len(random_indexes))
random_indexes.head()
```

    113826





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>call_id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1_00177953e32e7046c0739d5edb4974877b3c6f634570...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1_0013e00455bedc6adbc37ef23ea98be2fa9b64725511...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1_0016f101d8a724a6cff2efc31b4a608556548f9f5a30...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1_00171b687c805fa961859d83a562b82d8d289ac41c30...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1_0001213aecc8140d73918b7fcd11af181a850ce5b7d2...</td>
    </tr>
  </tbody>
</table>
</div>




```python
twenty_rows = random_indexes.sample(n=20)
twenty_rows.call_id.values
```




    array(['1_880a50322a54983b7d187546b45e05be77a6d991fc53acfc97aa954a.json__8',
           '1_93937a3129d9f9852b02ad01129e36b2389dcaa2e06da91160a63b3f.json__49',
           '1_345a66f5857331bc0e4f69ee8c6d86fcb07da6b395cc5146746c12b3.json__87',
           '1_c40a615742db891c09e04e19ace734641b1fea8775f49b2066053c9c.json__0',
           '1_b150cf01d6110180f21f09a8cd7d771b274458423a220bd48633e968.json__43',
           '1_7090b764e88efb03cb1665b44a242eb94682d13d7f4e1a3ff45f00e6.json__228',
           '1_a7a39c545b286b1b197c41bf587b254d4dc4f1e8a24aa1424b112255.json__1000',
           '1_bb869d7becb7ad38bfa2869e56d861a0754df06c928f6e33edc882dd.json__19',
           '1_9fecc85901a68ef06fa445419184b24bd503bb88d600d46cfecaf3a8.json__15',
           '1_19714bf818ee2bbcef666e34b363c147d7f99ed1aa616886c630266d.json__456',
           '1_b8a0fe42f7de1b1e65cd1188e9373963c4716c22bb7c955fcc47188c.json__211',
           '1_94cad047dabce97d8f8935b1dcf7294a55c60a9b9bdc01b12d1b550c.json__15',
           '1_5b1758c610443baefdcb4a63b0cf877f5d63af3cf84c16b80a65a599.json__187',
           '1_87d0bc1745024c44d186a6bc5e6a2ec6b7b19fc2c4744bb4578b2655.json__175',
           '1_392cf4ef21b68ddfeafc1bad500b050701d55a142790d8e0e50ee3c2.json__123',
           '1_72e6bc91e0b06000a4427c937ca6e7caba495a9737e0e473c8d636c4.json__309',
           '1_7f612e0a69024ff9caccb9ec42753a7712c788a001bd2fbccf722699.json__603',
           '1_edab73ed1f7e8b4f212b03d8e0fe660592f076e7407a68b645719574.json__2',
           '1_7490a65415d870ec5c7716bbe7c48b0de5a45cad50274642ef5fc0df.json__58',
           '1_acd45e6300e2c4287dd425ddd677c25891bc9fe6df4cdd1d5dfd8e77.json__54'],
          dtype=object)



### Pick these 20 random rows out of the dataset - getting location and script_url values


```python
df = dd.read_parquet(CACHE_NEW_DIR, columns=['location', 'script_url'], engine='fastparquet')
df.divisions = divisions
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>location</th>
      <th>script_url</th>
    </tr>
    <tr>
      <th>call_id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__0</th>
      <td>https://mech.iitm.ac.in/meiitm/</td>
      <td>https://mech.iitm.ac.in/meiitm/wp-includes/js/...</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__1</th>
      <td>https://mech.iitm.ac.in/meiitm/</td>
      <td>https://mech.iitm.ac.in/meiitm/wp-includes/js/...</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__2</th>
      <td>https://mech.iitm.ac.in/meiitm/</td>
      <td>https://mech.iitm.ac.in/meiitm/wp-admin/js/iri...</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__3</th>
      <td>https://mech.iitm.ac.in/meiitm/</td>
      <td>https://mech.iitm.ac.in/meiitm/wp-admin/js/iri...</td>
    </tr>
    <tr>
      <th>1_00001314358470f0c99914d5c7af0cd89248e54883ac3b5083395b61.json__4</th>
      <td>https://mech.iitm.ac.in/meiitm/</td>
      <td>https://mech.iitm.ac.in/meiitm/wp-includes/js/...</td>
    </tr>
  </tbody>
</table>
</div>




```python
%%time
success = []
failed = []
for index in twenty_rows.call_id.values:
    print('Looking for {}'.format(index))
    try:
        df.loc[index,:].compute()
        success.append(index)
    except:
        failed.append(index)
```

    Looking for 1_880a50322a54983b7d187546b45e05be77a6d991fc53acfc97aa954a.json__8
    Looking for 1_93937a3129d9f9852b02ad01129e36b2389dcaa2e06da91160a63b3f.json__49
    Looking for 1_345a66f5857331bc0e4f69ee8c6d86fcb07da6b395cc5146746c12b3.json__87
    Looking for 1_c40a615742db891c09e04e19ace734641b1fea8775f49b2066053c9c.json__0
    Looking for 1_b150cf01d6110180f21f09a8cd7d771b274458423a220bd48633e968.json__43
    Looking for 1_7090b764e88efb03cb1665b44a242eb94682d13d7f4e1a3ff45f00e6.json__228
    Looking for 1_a7a39c545b286b1b197c41bf587b254d4dc4f1e8a24aa1424b112255.json__1000
    Looking for 1_bb869d7becb7ad38bfa2869e56d861a0754df06c928f6e33edc882dd.json__19
    Looking for 1_9fecc85901a68ef06fa445419184b24bd503bb88d600d46cfecaf3a8.json__15
    Looking for 1_19714bf818ee2bbcef666e34b363c147d7f99ed1aa616886c630266d.json__456
    Looking for 1_b8a0fe42f7de1b1e65cd1188e9373963c4716c22bb7c955fcc47188c.json__211
    Looking for 1_94cad047dabce97d8f8935b1dcf7294a55c60a9b9bdc01b12d1b550c.json__15
    Looking for 1_5b1758c610443baefdcb4a63b0cf877f5d63af3cf84c16b80a65a599.json__187
    Looking for 1_87d0bc1745024c44d186a6bc5e6a2ec6b7b19fc2c4744bb4578b2655.json__175
    Looking for 1_392cf4ef21b68ddfeafc1bad500b050701d55a142790d8e0e50ee3c2.json__123
    Looking for 1_72e6bc91e0b06000a4427c937ca6e7caba495a9737e0e473c8d636c4.json__309
    Looking for 1_7f612e0a69024ff9caccb9ec42753a7712c788a001bd2fbccf722699.json__603
    Looking for 1_edab73ed1f7e8b4f212b03d8e0fe660592f076e7407a68b645719574.json__2
    Looking for 1_7490a65415d870ec5c7716bbe7c48b0de5a45cad50274642ef5fc0df.json__58
    Looking for 1_acd45e6300e2c4287dd425ddd677c25891bc9fe6df4cdd1d5dfd8e77.json__54
    CPU times: user 384 ms, sys: 3.55 s, total: 3.94 s
    Wall time: 21 s



```python
%%time
df.loc[twenty_rows.call_id.values,:].compute()
```

    CPU times: user 166 ms, sys: 169 ms, total: 335 ms
    Wall time: 2.19 s





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>location</th>
      <th>script_url</th>
    </tr>
    <tr>
      <th>call_id</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1_19714bf818ee2bbcef666e34b363c147d7f99ed1aa616886c630266d.json__456</th>
      <td>http://askul.co.jp/e/15/</td>
      <td>http://assets.adobedtm.com/29bc4dc777738960adb...</td>
    </tr>
    <tr>
      <th>1_345a66f5857331bc0e4f69ee8c6d86fcb07da6b395cc5146746c12b3.json__87</th>
      <td>https://fr.zopim.com/</td>
      <td>https://www.google-analytics.com/analytics.js</td>
    </tr>
    <tr>
      <th>1_392cf4ef21b68ddfeafc1bad500b050701d55a142790d8e0e50ee3c2.json__123</th>
      <td>http://www.mediamarkt.de/de/category/_streamin...</td>
      <td>http://js.redblue.de/fee/js/dist/core.js</td>
    </tr>
    <tr>
      <th>1_5b1758c610443baefdcb4a63b0cf877f5d63af3cf84c16b80a65a599.json__187</th>
      <td>https://www.zhibo8.cc/zhibo/other/2017/1119113...</td>
      <td>https://www.zhibo8.cc/js/2016/ndanmu.js</td>
    </tr>
    <tr>
      <th>1_7090b764e88efb03cb1665b44a242eb94682d13d7f4e1a3ff45f00e6.json__228</th>
      <td>https://musique.fnac.com/s121859/T-shirts-post...</td>
      <td>https://actor-5637.kxcdn.com/actor/3E2C5D6A15C...</td>
    </tr>
    <tr>
      <th>1_72e6bc91e0b06000a4427c937ca6e7caba495a9737e0e473c8d636c4.json__309</th>
      <td>http://www.xianliao.me/h/9cc46d7c653ee32363f89...</td>
      <td>http://cdn.xianliao.me/assets/5334b5d63c4a3db5...</td>
    </tr>
    <tr>
      <th>1_7490a65415d870ec5c7716bbe7c48b0de5a45cad50274642ef5fc0df.json__58</th>
      <td>http://iitb.ac.in/en/event/quami-ekta-saptah</td>
      <td>http://maps.googleapis.com/maps-api-v3/api/js/...</td>
    </tr>
    <tr>
      <th>1_7f612e0a69024ff9caccb9ec42753a7712c788a001bd2fbccf722699.json__603</th>
      <td>https://www.stoloto.ru/gzhl/game?int=sitemap&amp;l...</td>
      <td>https://web.redhelper.ru/container/main.js?ver...</td>
    </tr>
    <tr>
      <th>1_87d0bc1745024c44d186a6bc5e6a2ec6b7b19fc2c4744bb4578b2655.json__175</th>
      <td>https://bbcdn.go.goldbachpoland.bbelements.com...</td>
      <td>https://code.createjs.com/createjs-2015.11.26....</td>
    </tr>
    <tr>
      <th>1_880a50322a54983b7d187546b45e05be77a6d991fc53acfc97aa954a.json__8</th>
      <td>http://grid.mk/twitter</td>
      <td>https://ajax.cloudflare.com/cdn-cgi/scripts/90...</td>
    </tr>
    <tr>
      <th>1_93937a3129d9f9852b02ad01129e36b2389dcaa2e06da91160a63b3f.json__49</th>
      <td>https://disqus.com/embed/comments/?base=defaul...</td>
      <td>https://c.disquscdn.com/next/embed/lounge.bund...</td>
    </tr>
    <tr>
      <th>1_94cad047dabce97d8f8935b1dcf7294a55c60a9b9bdc01b12d1b550c.json__15</th>
      <td>https://disqus.com/embed/comments/?base=defaul...</td>
      <td>https://ssl.google-analytics.com/ga.js</td>
    </tr>
    <tr>
      <th>1_9fecc85901a68ef06fa445419184b24bd503bb88d600d46cfecaf3a8.json__15</th>
      <td>http://www.joann.com/art-supplies-and-painting...</td>
      <td>http://tags.tiqcdn.com/utag/joann/main/prod/ut...</td>
    </tr>
    <tr>
      <th>1_a7a39c545b286b1b197c41bf587b254d4dc4f1e8a24aa1424b112255.json__1000</th>
      <td>https://www.thestudentroom.co.uk/forumdisplay....</td>
      <td>https://static.thestudentroom.co.uk/5a3104ea5d...</td>
    </tr>
    <tr>
      <th>1_acd45e6300e2c4287dd425ddd677c25891bc9fe6df4cdd1d5dfd8e77.json__54</th>
      <td>http://www.timesjobs.com/bestconsultant/nation...</td>
      <td>http://www.google-analytics.com/analytics.js</td>
    </tr>
    <tr>
      <th>1_b150cf01d6110180f21f09a8cd7d771b274458423a220bd48633e968.json__43</th>
      <td>https://www.zoom.com.br/cd-dvd-e-blu-ray</td>
      <td>https://www.google-analytics.com/analytics.js</td>
    </tr>
    <tr>
      <th>1_b8a0fe42f7de1b1e65cd1188e9373963c4716c22bb7c955fcc47188c.json__211</th>
      <td>https://www.raileurope.com/index.html</td>
      <td>https://actorssl-5637.kxcdn.com/actor/b4976499...</td>
    </tr>
    <tr>
      <th>1_bb869d7becb7ad38bfa2869e56d861a0754df06c928f6e33edc882dd.json__19</th>
      <td>https://www.creagames.com/ref/409</td>
      <td>https://www.google-analytics.com/analytics.js</td>
    </tr>
    <tr>
      <th>1_c40a615742db891c09e04e19ace734641b1fea8775f49b2066053c9c.json__0</th>
      <td>http://staticxx.facebook.com/connect/xd_arbite...</td>
      <td>http://staticxx.facebook.com/connect/xd_arbite...</td>
    </tr>
    <tr>
      <th>1_edab73ed1f7e8b4f212b03d8e0fe660592f076e7407a68b645719574.json__2</th>
      <td>https://ovstk.demdex.net/dest5.html?d_nsid=und...</td>
      <td>https://ovstk.demdex.net/dest5.html?d_nsid=und...</td>
    </tr>
  </tbody>
</table>
</div>



### 2 seconds to pull 20 random rows out of 131million - yay!
