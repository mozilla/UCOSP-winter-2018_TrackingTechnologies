

```python
import sys
sys.path.append('..')
from utils import load_data_util
```


```python
import pandas as pd
import json
```

**This analysis aim to look at known sites which calls known session replay sites to see if we can find signs of session replay activity.**

Session replay providers are services that offer websites a way to track their users - from how they interact with the site to what searches they performed and input they provided. Some session replay providers may even record personal information such as personal addresses and credit card information.

The list of session replay sites comes from the  [**Princeton WebTAP project**](https://webtransparency.cs.princeton.edu/no_boundaries/session_replay_sites.html), which listed sites within the Alexa top 10,000 that show signs of session replay scripts.

With a sample size of 500 sites - 21 were found to use session replay calls.
However when we boil it down to the base url the sample size reduced to 279 unique base urls and 15 of which uses session replay:
  
*'hdrezka.ag',
*'sprashivai.ru',
*'getcourse.ru',
*'www.cardinalcommerce.com',
*'tap.az',
*'out.pladform.ru',
*'www.geekbuying.com',
*'www.the-star.co.ke',
*'dnevnik.ru',
*'studfiles.net',
*'pagseguro.uol.com.br',
*'www.universal.org',
*'dugtor.ru',
*'seasonvar.ru',
*'porn555.com'

Correlation between call symbols and wheter or not the call is a session replay call is also attempted, however the correlation weren't very strong - with the highest being **window.navigator.plugins[Shockwave Flash].version** at 0.105229





```python
data_frame = load_data_util.load_random_data(500, seed=3)
```

    rejected '1_21e5ef84bd5a70860d496896c77a226c50efce2ca8ac54c6d9757539.json' because: script_col is '' when it should be a number.
    rejected '1_a36b8d1d4be60955eeb0830dd5fa6ae88ef7e0388c4329b62ec14a9e.json' because: Invalid call stack format: row and column information was not present at the end of a call stack frame.
    

Get the list of known session replay providers


```python
def get_replay_sites():
    """Loads a list of session replay providers from the Princeton WebTAP project,
    which listed sites within the Alexa top 10,000 that show signs of session replay scripts.
    """
    replay_list = pd.read_csv('../data/sr_site_list.csv')
    return replay_list.third_party.unique()
```


```python
replay_sites = get_replay_sites()
```

Get the list of calls where the script_url is one of the known session replay providers


```python
def get_replay_data_frames(replay_sites):
    """Parses through the data frame containing calls from the crawl and returns a data frame containing a subset of the 
    calls with a script_url string containing one of the provided replay providers.
    """
    replay_data_frames = []
    for replay_provider in replay_sites:
        replay_data_frames.append(data_frame.query("script_url.str.contains('"+ replay_provider +"')"))
    return pd.concat(replay_data_frames)
```


```python
replay_calls = get_replay_data_frames(replay_sites)
```


```python
replay_sites
```




    array(['yandex.ru', 'clicktale.net', 'hotjar.com', 'sessioncam.com',
           'inspectlet.com', 'userreplay.net', 'mouseflow.com',
           'decibelinsight.net', 'fullstory.com', 'luckyorange.com',
           'quantummetric.com', 'salemove.com', 'smartlook.com',
           'logrocket.com'], dtype=object)



Of the ~25000 calls examined, 864 of them are to one of the listed session replay providers.


```python
data_frame.shape
```




    (25460, 15)




```python
replay_calls.shape
```




    (864, 15)



Adds a flag onto the data frame to indicate if a given call is to a known session replay provider


```python
def add_is_provider_tag_to_df():
    """Adds a flag onto the data frame to indicate if a given call is to a known session replay provider
    """
    data_frame["is_replay_provider"] = 0
    for index in replay_calls.index:
        data_frame.loc[[index], ["is_replay_provider"]] = 1
```


```python
add_is_provider_tag_to_df()
```

There doesn't seem to be a strong correlation between other numerical columns and if the call is to a session replay provider. But looking at the numeric column, this is not a surprise file_number, script_col etc...


```python
data_frame.corr()["is_replay_provider"]
```




    crawl_id                   NaN
    file_number          -0.061402
    in_iframe            -0.082053
    script_col           -0.065132
    script_line          -0.031306
    is_replay_provider    1.000000
    Name: is_replay_provider, dtype: float64



Next attempt is to hot encode the symbol column, and see if any symbols has a correlation with a session replay call.


```python
symbol_encoded = pd.get_dummies(data_frame["symbol"])
```


```python
data_frame_with_symbol = pd.concat([data_frame, symbol_encoded], axis=1)
```

Again, no strong correlations were found


```python
data_frame_with_symbol.corr().is_replay_provider.sort_values(ascending = False)
```




    is_replay_provider                                                       1.000000
    window.navigator.plugins[Shockwave Flash].version                        0.105229
    window.navigator.languages                                               0.092501
    window.navigator.mimeTypes[application/futuresplash].description         0.072583
    window.navigator.mimeTypes[application/x-shockwave-flash].description    0.072583
    window.navigator.mimeTypes[application/futuresplash].suffixes            0.064548
    window.navigator.mimeTypes[application/x-shockwave-flash].suffixes       0.064548
    window.navigator.mimeTypes[application/futuresplash].type                0.044148
    window.navigator.mimeTypes[application/x-shockwave-flash].type           0.033428
    window.navigator.platform                                                0.033294
    window.navigator.plugins[Shockwave Flash].filename                       0.032890
    window.navigator.onLine                                                  0.027419
    window.navigator.plugins[Shockwave Flash].name                           0.026443
    window.navigator.oscpu                                                   0.025387
    window.navigator.doNotTrack                                              0.017437
    window.Storage.setItem                                                   0.015234
    window.Storage.getItem                                                   0.013496
    window.navigator.productSub                                              0.013329
    window.navigator.cookieEnabled                                           0.009732
    window.document.cookie                                                   0.007715
    window.navigator.vendor                                                  0.007705
    window.navigator.language                                                0.005037
    window.navigator.plugins[Shockwave Flash].description                    0.004430
    window.Storage.clear                                                    -0.001175
    CanvasRenderingContext2D.isPointInPath                                  -0.001175
    OfflineAudioContext.createOscillator                                    -0.001175
    OscillatorNode.frequency                                                -0.001175
    OfflineAudioContext.createDynamicsCompressor                            -0.001175
    OfflineAudioContext.startRendering                                      -0.001175
    OfflineAudioContext.destination                                         -0.001175
                                                                               ...   
    window.navigator.plugins[Shockwave Flash].length                        -0.006107
    CanvasRenderingContext2D.fillRect                                       -0.006649
    CanvasRenderingContext2D.bezierCurveTo                                  -0.007053
    window.Storage.key                                                      -0.007246
    window.screen.pixelDepth                                                -0.007435
    window.navigator.product                                                -0.008060
    window.Storage.length                                                   -0.008560
    CanvasRenderingContext2D.lineWidth                                      -0.009109
    CanvasRenderingContext2D.stroke                                         -0.009260
    HTMLCanvasElement.width                                                 -0.009409
    HTMLCanvasElement.height                                                -0.009409
    CanvasRenderingContext2D.fillStyle                                      -0.009482
    RTCPeerConnection.localDescription                                      -0.009699
    CanvasRenderingContext2D.fillText                                       -0.009981
    CanvasRenderingContext2D.textAlign                                      -0.010783
    window.navigator.appName                                                -0.011444
    HTMLCanvasElement.getContext                                            -0.011591
    CanvasRenderingContext2D.measureText                                    -0.011651
    CanvasRenderingContext2D.textBaseline                                   -0.011769
    window.Storage.removeItem                                               -0.013386
    window.navigator.appVersion                                             -0.015682
    window.name                                                             -0.016805
    CanvasRenderingContext2D.font                                           -0.016886
    window.sessionStorage                                                   -0.024096
    script_line                                                             -0.031306
    window.navigator.userAgent                                              -0.035954
    file_number                                                             -0.061402
    script_col                                                              -0.065132
    in_iframe                                                               -0.082053
    crawl_id                                                                      NaN
    Name: is_replay_provider, Length: 128, dtype: float64



Group the symbols called by the file number to see if any common calls were made between different sites: window.document.cookie was called by all sites


```python
symbols_groupedby_file_number = data_frame_with_symbol.query("is_replay_provider == 1").groupby("file_number").symbol.unique()
for groups in symbols_groupedby_file_number:
    print(groups)
```

    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name' 'window.name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.Storage.setItem' 'window.navigator.vendor'
     'window.navigator.onLine' 'window.navigator.platform']
    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name' 'window.name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.Storage.setItem' 'window.navigator.platform'
     'window.navigator.vendor']
    ['window.document.cookie']
    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name' 'window.name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.Storage.setItem' 'window.navigator.vendor'
     'window.navigator.platform']
    ['window.document.cookie']
    ['window.document.cookie']
    ['window.document.cookie']
    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name' 'window.name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.Storage.setItem' 'window.navigator.vendor'
     'window.navigator.platform']
    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.name' 'window.Storage.setItem'
     'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.navigator.vendor' 'window.navigator.platform']
    ['window.document.cookie']
    ['window.document.cookie']
    ['window.document.cookie']
    ['window.navigator.userAgent' 'window.document.cookie'
     'window.navigator.cookieEnabled' 'window.localStorage'
     'window.Storage.setItem' 'window.Storage.removeItem'
     'window.sessionStorage' 'window.navigator.doNotTrack'
     'window.navigator.language' 'window.screen.colorDepth'
     'window.navigator.platform' 'window.navigator.appName'
     'window.navigator.plugins[Shockwave Flash].name'
     'window.navigator.languages' 'window.navigator.oscpu'
     'window.navigator.productSub' 'window.Storage.getItem']
    ['window.navigator.userAgent' 'window.document.cookie'
     'window.navigator.cookieEnabled' 'window.localStorage'
     'window.Storage.setItem' 'window.Storage.removeItem'
     'window.sessionStorage']
    ['window.navigator.doNotTrack' 'window.document.cookie'
     'window.navigator.userAgent' 'window.navigator.language'
     'window.screen.colorDepth' 'window.sessionStorage' 'window.localStorage'
     'window.navigator.platform' 'window.navigator.appName'
     'window.navigator.plugins[Shockwave Flash].name'
     'window.navigator.languages' 'window.navigator.oscpu'
     'window.navigator.productSub' 'window.Storage.getItem']
    ['window.Storage.getItem' 'window.Storage.setItem'
     'window.navigator.userAgent' 'window.navigator.onLine'
     'window.localStorage' 'window.navigator.platform'
     'window.document.cookie']
    ['window.document.cookie' 'window.navigator.vendor'
     'window.Storage.getItem' 'window.Storage.setItem' 'window.localStorage'
     'window.navigator.platform' 'window.navigator.userAgent']
    ['window.navigator.userAgent' 'window.localStorage'
     'window.Storage.setItem' 'window.Storage.removeItem'
     'window.document.cookie' 'window.Storage.getItem']
    ['window.document.cookie']
    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name' 'window.name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.Storage.setItem' 'window.navigator.vendor'
     'window.navigator.platform']
    ['window.localStorage' 'window.navigator.userAgent'
     'window.document.cookie' 'window.Storage.getItem'
     'window.Storage.removeItem' 'window.name' 'window.Storage.setItem'
     'window.navigator.languages'
     'window.navigator.plugins[Shockwave Flash].name'
     'window.screen.colorDepth'
     'window.navigator.plugins[Shockwave Flash].version'
     'window.navigator.plugins[Shockwave Flash].description'
     'window.navigator.plugins[Shockwave Flash].filename'
     'window.navigator.mimeTypes[application/futuresplash].type'
     'window.navigator.mimeTypes[application/futuresplash].description'
     'window.navigator.mimeTypes[application/futuresplash].suffixes'
     'window.navigator.mimeTypes[application/x-shockwave-flash].type'
     'window.navigator.mimeTypes[application/x-shockwave-flash].description'
     'window.navigator.mimeTypes[application/x-shockwave-flash].suffixes'
     'window.navigator.cookieEnabled' 'window.navigator.language'
     'window.navigator.vendor' 'window.navigator.platform'
     'window.navigator.onLine']
    

In total, 21 urls called a session replay provider, however if we boil it down to base url, only 15 unique sites were found


```python
replay_calls.file_number.unique().size
```




    21




```python
from urllib.parse import urlparse
```


```python
list(set([urlparse(location).netloc for location in replay_calls.location.unique()]))
```




    ['hdrezka.ag',
     'sprashivai.ru',
     'getcourse.ru',
     'www.cardinalcommerce.com',
     'tap.az',
     'out.pladform.ru',
     'www.geekbuying.com',
     'www.the-star.co.ke',
     'dnevnik.ru',
     'studfiles.net',
     'pagseguro.uol.com.br',
     'www.universal.org',
     'dugtor.ru',
     'seasonvar.ru',
     'porn555.com']




```python
len(list(set([urlparse(location).netloc for location in data_frame.location.unique()])))
```




    279




```python
len(list(set([urlparse(location).netloc for location in replay_calls.location.unique()])))
```




    15



The number of calls per file, didn't seem to be an indicator for if the site uses a session replay provider either
