

```python
"""
Jupyter Notebook for generating statistics from random files
Example workflow:
-create df from entity list
-generate random files
-generate count for # of scripts used per TDL
-visualise data in bar chart
"""


import pandas as pd
import sys
sys.path.append('..')
import matplotlib
import sample_data
from utils import load_data_util

#Do not truncate cell values
pd.set_option('display.max_colwidth', -1)
```


```python
#Create df from entity list
result = sample_data.make_entity_list_df()
result["count"] = 0
result
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
      <th>properties</th>
      <th>resources</th>
      <th>sites</th>
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2leep.com</th>
      <td>[2leep.com]</td>
      <td>[2leep.com]</td>
      <td>{2leep.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>33Across</th>
      <td>[33across.com, tynt.com]</td>
      <td>[33across.com, tynt.com]</td>
      <td>{tynt.com, 33across.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>365Media</th>
      <td>[aggregateintelligence.com]</td>
      <td>[365dm.com, 365media.com, aggregateintelligence.com]</td>
      <td>{365dm.com, aggregateintelligence.com, 365media.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4INFO</th>
      <td>[4info.com, adhaven.com]</td>
      <td>[4info.com, adhaven.com]</td>
      <td>{adhaven.com, 4info.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4mads</th>
      <td>[4mads.com]</td>
      <td>[4mads.com]</td>
      <td>{4mads.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>63 Squares</th>
      <td>[63labs.com]</td>
      <td>[63squares.com, 63labs.com, i-stats.com]</td>
      <td>{i-stats.com, 63labs.com, 63squares.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AD Europe</th>
      <td>[adeurope.com]</td>
      <td>[adeurope.com]</td>
      <td>{adeurope.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AD2ONE</th>
      <td>[ad2onegroup.com]</td>
      <td>[ad2onegroup.com]</td>
      <td>{ad2onegroup.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ADITION</th>
      <td>[adition.com]</td>
      <td>[adition.com]</td>
      <td>{adition.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ADP Dealer Services</th>
      <td>[cdkglobal.com]</td>
      <td>[cdkglobal.com, adpdealerservices.com, admission.net, cobalt.com]</td>
      <td>{admission.net, cobalt.com, adpdealerservices.com, cdkglobal.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ADTECH</th>
      <td>[adtech.com, adtech.de, adtechus.com]</td>
      <td>[adtech.com, adtech.de, adtechus.com]</td>
      <td>{adtechus.com, adtech.com, adtech.de}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ADTELLIGENCE</th>
      <td>[adtelligence.de]</td>
      <td>[adtelligence.de]</td>
      <td>{adtelligence.de}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ADZ</th>
      <td>[adzcentral.com]</td>
      <td>[adzcentral.com]</td>
      <td>{adzcentral.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AERIFY MEDIA</th>
      <td>[aerifymedia.com, anonymous-media.com]</td>
      <td>[aerifymedia.com, anonymous-media.com]</td>
      <td>{anonymous-media.com, aerifymedia.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AK</th>
      <td>[aggregateknowledge.com, agkn.com]</td>
      <td>[aggregateknowledge.com, agkn.com]</td>
      <td>{aggregateknowledge.com, agkn.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AKQA</th>
      <td>[akqa.com]</td>
      <td>[akqa.com, srtk.net]</td>
      <td>{akqa.com, srtk.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AOL</th>
      <td>[aol.com, adsonar.com, advertising.com, atwola.com, leadback.com, tacoda.net, 5min.com, aim.com, aolcdn.com, aoltechguru.com, autoblog.com, cambio.com, dailyfinance.com, editions.com, engadget.com, games.com, homesessive.com, huffingtonpost.com, makers.com, mandatory.com, mapquest.com, moviefone.com, noisecreep.com, patch.com, pawnation.com, shortcuts.com, shoutcast.com, spinner.com, stylelist.com, stylemepretty.com, surphace.com, techcrunch.com, theboombox.com, theboot.com, userplane.com, winamp.com]</td>
      <td>[aol.com, adsonar.com, advertising.com, atwola.com, leadback.com, tacoda.net, 5min.com, aim.com, aolcdn.com, editions.com, mapquest.com, patch.com, shortcuts.com, shoutcast.com, spinner.com, surphace.com, userplane.com, winamp.com, adtechjp.com]</td>
      <td>{stylelist.com, winamp.com, leadback.com, patch.com, makers.com, mapquest.com, autoblog.com, aol.com, aolcdn.com, mandatory.com, dailyfinance.com, shoutcast.com, stylemepretty.com, cambio.com, atwola.com, games.com, shortcuts.com, huffingtonpost.com, engadget.com, spinner.com, techcrunch.com, tacoda.net, aim.com, surphace.com, advertising.com, editions.com, aoltechguru.com, userplane.com, 5min.com, homesessive.com, noisecreep.com, adtechjp.com, adsonar.com, moviefone.com, theboombox.com, pawnation.com, theboot.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AT Internet</th>
      <td>[atinternet.com, hit-parade.com, xiti.com]</td>
      <td>[atinternet.com, hit-parade.com, xiti.com]</td>
      <td>{xiti.com, hit-parade.com, atinternet.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AT&amp;T</th>
      <td>[att.com, yp.com]</td>
      <td>[att.com, yp.com]</td>
      <td>{yp.com, att.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AUTOCENTRE.UA</th>
      <td>[autocentre.ua, am.ua]</td>
      <td>[autocentre.ua, am.ua]</td>
      <td>{am.ua, autocentre.ua}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>AWeber</th>
      <td>[aweber.com]</td>
      <td>[aweber.com]</td>
      <td>{aweber.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Abax Interactive</th>
      <td>[abaxinteractive.com]</td>
      <td>[abaxinteractive.com]</td>
      <td>{abaxinteractive.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Accelia</th>
      <td>[accelia.net, durasite.net]</td>
      <td>[accelia.net, durasite.net]</td>
      <td>{durasite.net, accelia.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Accordant Media</th>
      <td>[accordantmedia.com]</td>
      <td>[accordantmedia.com]</td>
      <td>{accordantmedia.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Acquisio</th>
      <td>[acquisio.com, clickequations.net]</td>
      <td>[acquisio.com, clickequations.net]</td>
      <td>{acquisio.com, clickequations.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Act-On</th>
      <td>[act-on.com, actonsoftware.com]</td>
      <td>[act-on.com, actonsoftware.com]</td>
      <td>{actonsoftware.com, act-on.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Actisens</th>
      <td>[actisens.com, gestionpub.com]</td>
      <td>[actisens.com, gestionpub.com]</td>
      <td>{gestionpub.com, actisens.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ActivEngage</th>
      <td>[activengage.com]</td>
      <td>[activengage.com]</td>
      <td>{activengage.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ActiveConversion</th>
      <td>[activeconversion.com, activemeter.com]</td>
      <td>[activeconversion.com, activemeter.com]</td>
      <td>{activemeter.com, activeconversion.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>Acuity</th>
      <td>[acuity.com, acuityads.com, acuityplatform.com]</td>
      <td>[acuity.com, acuityads.com, acuityplatform.com]</td>
      <td>{acuity.com, acuityplatform.com, acuityads.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>kikin</th>
      <td>[kikin.com]</td>
      <td>[kikin.com]</td>
      <td>{kikin.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>m6d</th>
      <td>[dstillery.com]</td>
      <td>[dstillery.com, m6d.com, media6degrees.com]</td>
      <td>{m6d.com, media6degrees.com, dstillery.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>madvertise</th>
      <td>[madvertise.com]</td>
      <td>[madvertise.com]</td>
      <td>{madvertise.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>mashero</th>
      <td>[mashero.com]</td>
      <td>[mashero.com]</td>
      <td>{mashero.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>media.net</th>
      <td>[media.net]</td>
      <td>[media.net]</td>
      <td>{media.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>mediaFORGE</th>
      <td>[mediaforge.com]</td>
      <td>[mediaforge.com]</td>
      <td>{mediaforge.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>motigo</th>
      <td>[motigo.com]</td>
      <td>[motigo.com, nedstatbasic.net]</td>
      <td>{nedstatbasic.net, motigo.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>myThings</th>
      <td>[mythings.com, mythingsmedia.com]</td>
      <td>[mythings.com, mythingsmedia.com]</td>
      <td>{mythings.com, mythingsmedia.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>newtention</th>
      <td>[newtention.de, newtention.net, newtentionassets.net]</td>
      <td>[newtention.de, newtention.net, newtentionassets.net]</td>
      <td>{newtentionassets.net, newtention.de, newtention.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>nrelate</th>
      <td>[nrelate.com]</td>
      <td>[nrelate.com]</td>
      <td>{nrelate.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>nugg.ad</th>
      <td>[nugg.ad]</td>
      <td>[nugg.ad, nuggad.net]</td>
      <td>{nugg.ad, nuggad.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>nurago</th>
      <td>[sensic.net]</td>
      <td>[nurago.com, nurago.de, sensic.net]</td>
      <td>{nurago.de, nurago.com, sensic.net}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>onAd</th>
      <td>[onad.eu]</td>
      <td>[onad.eu]</td>
      <td>{onad.eu}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>phpMyVisites</th>
      <td>[phpmyvisites.us]</td>
      <td>[phpmyvisites.us]</td>
      <td>{phpmyvisites.us}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>plista</th>
      <td>[plista.com]</td>
      <td>[plista.com]</td>
      <td>{plista.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>quadrantOne</th>
      <td>[quadrantone.com]</td>
      <td>[quadrantone.com]</td>
      <td>{quadrantone.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>reddit</th>
      <td>[reddit.com]</td>
      <td>[reddit.com]</td>
      <td>{reddit.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>sociomantic labs</th>
      <td>[sociomantic.com]</td>
      <td>[sociomantic.com]</td>
      <td>{sociomantic.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>sophus3</th>
      <td>[sophus3.com]</td>
      <td>[sophus3.com, sophus3.co.uk]</td>
      <td>{sophus3.com, sophus3.co.uk}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>stat4u</th>
      <td>[4u.pl]</td>
      <td>[4u.pl]</td>
      <td>{4u.pl}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>uCoz</th>
      <td>[ucoz.com, ucoz.ae, ucoz.fr, ucoz.net, ucoz.ru]</td>
      <td>[ucoz.com, ucoz.ae, ucoz.br, ucoz.du, ucoz.fr, ucoz.net, ucoz.ru]</td>
      <td>{ucoz.ae, ucoz.ru, ucoz.du, ucoz.com, ucoz.net, ucoz.fr, ucoz.br}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>up-value</th>
      <td>[up-value.de]</td>
      <td>[up-value.de]</td>
      <td>{up-value.de}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>vistrac</th>
      <td>[vistrac.com]</td>
      <td>[vistrac.com]</td>
      <td>{vistrac.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>whos.amung.us</th>
      <td>[amung.us]</td>
      <td>[amung.us]</td>
      <td>{amung.us}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>xAd</th>
      <td>[xad.com]</td>
      <td>[xad.com]</td>
      <td>{xad.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>xplosion interactive</th>
      <td>[xplosion.de]</td>
      <td>[xplosion.de]</td>
      <td>{xplosion.de}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>youknowbest</th>
      <td>[youknowbest.com]</td>
      <td>[youknowbest.com]</td>
      <td>{youknowbest.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>zanox</th>
      <td>[zanox.com, buy.at, zanox-affiliate.de]</td>
      <td>[zanox.com, buy.at, zanox-affiliate.de]</td>
      <td>{zanox-affiliate.de, buy.at, zanox.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>zapunited</th>
      <td>[zapunited.com, zaparena.com]</td>
      <td>[zapunited.com, zaparena.com]</td>
      <td>{zaparena.com, zapunited.com}</td>
      <td>0</td>
    </tr>
    <tr>
      <th>ÖWA</th>
      <td>[oewa.at]</td>
      <td>[oewa.at, oewabox.at]</td>
      <td>{oewa.at, oewabox.at}</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>1035 rows × 4 columns</p>
</div>




```python
#Load random files
files = load_data_util.load_random_data(10, "false")
files
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
      <th>arguments</th>
      <th>call_stack</th>
      <th>crawl_id</th>
      <th>file_number</th>
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
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>1</td>
      <td></td>
      <td>True</td>
      <td>https://platform.twitter.com/widgets/tweet_button.64457a6e8f493e1f1022f50e4e7e67e8.en.html#dnt=false&amp;id=twitter-widget-0&amp;lang=en&amp;original_referer=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html&amp;size=m&amp;text=Watch%20Murder%20on%20the%20Orient%20Express%20(2017)%20Online%20Free%20-%20123Movies%3A&amp;time=1513442859514&amp;type=share&amp;url=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html%23.WjVOJbvPkHI.twitter</td>
      <td>get</td>
      <td>13</td>
      <td>27</td>
      <td></td>
      <td>https://platform.twitter.com/widgets/tweet_button.64457a6e8f493e1f1022f50e4e7e67e8.en.html#dnt=false&amp;id=twitter-widget-0&amp;lang=en&amp;original_referer=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html&amp;size=m&amp;text=Watch%20Murder%20on%20the%20Orient%20Express%20(2017)%20Online%20Free%20-%20123Movies%3A&amp;time=1513442859514&amp;type=share&amp;url=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html%23.WjVOJbvPkHI.twitter</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T16:47:39.937Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>1</td>
      <td></td>
      <td>True</td>
      <td>https://platform.twitter.com/widgets/tweet_button.64457a6e8f493e1f1022f50e4e7e67e8.en.html#dnt=false&amp;id=twitter-widget-0&amp;lang=en&amp;original_referer=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html&amp;size=m&amp;text=Watch%20Murder%20on%20the%20Orient%20Express%20(2017)%20Online%20Free%20-%20123Movies%3A&amp;time=1513442859514&amp;type=share&amp;url=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html%23.WjVOJbvPkHI.twitter</td>
      <td>get</td>
      <td>13211</td>
      <td>27</td>
      <td></td>
      <td>https://platform.twitter.com/widgets/tweet_button.64457a6e8f493e1f1022f50e4e7e67e8.en.html#dnt=false&amp;id=twitter-widget-0&amp;lang=en&amp;original_referer=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html&amp;size=m&amp;text=Watch%20Murder%20on%20the%20Orient%20Express%20(2017)%20Online%20Free%20-%20123Movies%3A&amp;time=1513442859514&amp;type=share&amp;url=https%3A%2F%2F123movies.io%2Fmovie%2Fmurder-on-the-orient-express-52784%2Fwatching.html%23.WjVOJbvPkHI.twitter</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T16:47:39.942Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>2</td>
      <td></td>
      <td>True</td>
      <td>https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2166112977110757&amp;output=html&amp;h=190&amp;slotname=1586388620&amp;adk=3771989983&amp;adf=1596241330&amp;w=220&amp;lmt=1513413720&amp;loeid=368226211&amp;rafmt=10&amp;format=220x190_0ads_al&amp;url=http%3A%2F%2Fwww.revistahogar.com%2F&amp;flash=28.0.0&amp;wgl=1&amp;adsid=NT&amp;dt=1513413716189&amp;bpp=10&amp;bdt=663&amp;fdt=3731&amp;idt=4075&amp;shv=r20171206&amp;cbv=r20170110&amp;saldr=aa&amp;prev_fmts=728x90&amp;correlator=3150626740774&amp;frm=20&amp;ga_vid=242795170.1513413716&amp;ga_sid=1513413716&amp;ga_hid=959375706&amp;ga_fc=1&amp;pv=1&amp;icsg=2&amp;nhd=1&amp;dssz=2&amp;mdo=0&amp;mso=0&amp;u_tz=0&amp;u_his=1&amp;u_java=0&amp;u_h=768&amp;u_w=1366&amp;u_ah=768&amp;u_aw=1366&amp;u_cd=24&amp;u_nplug=1&amp;u_nmime=2&amp;adx=935&amp;ady=5&amp;biw=1353&amp;bih=697&amp;abxe=1&amp;eid=21061122%2C62710011%2C62710014%2C191880502%2C368226201%2C21061319&amp;oid=3&amp;nmo=1&amp;rx=0&amp;eae=0&amp;fc=528&amp;brdim=%2C%2C0%2C0%2C1366%2C0%2C1366%2C768%2C1366%2C697&amp;vis=1&amp;rsz=%7C%7ClE%7C&amp;abl=CS&amp;ppjl=f&amp;pfx=0&amp;fu=144&amp;bc=1&amp;ifi=2&amp;xpc=M50iGKYleF&amp;p=http%3A//www.revistahogar.com&amp;dtd=4154</td>
      <td>get</td>
      <td>7772</td>
      <td>1</td>
      <td></td>
      <td>https://tpc.googlesyndication.com/pagead/js/r20171206/r20110914/abg.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T08:42:01.025Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>2</td>
      <td></td>
      <td>True</td>
      <td>https://googleads.g.doubleclick.net/pagead/ads?client=ca-pub-2166112977110757&amp;output=html&amp;h=190&amp;slotname=1586388620&amp;adk=3771989983&amp;adf=1596241330&amp;w=220&amp;lmt=1513413720&amp;loeid=368226211&amp;rafmt=10&amp;format=220x190_0ads_al&amp;url=http%3A%2F%2Fwww.revistahogar.com%2F&amp;flash=28.0.0&amp;wgl=1&amp;adsid=NT&amp;dt=1513413716189&amp;bpp=10&amp;bdt=663&amp;fdt=3731&amp;idt=4075&amp;shv=r20171206&amp;cbv=r20170110&amp;saldr=aa&amp;prev_fmts=728x90&amp;correlator=3150626740774&amp;frm=20&amp;ga_vid=242795170.1513413716&amp;ga_sid=1513413716&amp;ga_hid=959375706&amp;ga_fc=1&amp;pv=1&amp;icsg=2&amp;nhd=1&amp;dssz=2&amp;mdo=0&amp;mso=0&amp;u_tz=0&amp;u_his=1&amp;u_java=0&amp;u_h=768&amp;u_w=1366&amp;u_ah=768&amp;u_aw=1366&amp;u_cd=24&amp;u_nplug=1&amp;u_nmime=2&amp;adx=935&amp;ady=5&amp;biw=1353&amp;bih=697&amp;abxe=1&amp;eid=21061122%2C62710011%2C62710014%2C191880502%2C368226201%2C21061319&amp;oid=3&amp;nmo=1&amp;rx=0&amp;eae=0&amp;fc=528&amp;brdim=%2C%2C0%2C0%2C1366%2C0%2C1366%2C768%2C1366%2C697&amp;vis=1&amp;rsz=%7C%7ClE%7C&amp;abl=CS&amp;ppjl=f&amp;pfx=0&amp;fu=144&amp;bc=1&amp;ifi=2&amp;xpc=M50iGKYleF&amp;p=http%3A//www.revistahogar.com&amp;dtd=4154</td>
      <td>get</td>
      <td>6589</td>
      <td>1</td>
      <td></td>
      <td>https://tpc.googlesyndication.com/pagead/js/r20171206/r20110914/activeview/osd_listener.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T08:42:01.083Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>injectDOM/&lt;</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>13</td>
      <td>28</td>
      <td></td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T05:43:41.025Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>injectDOM/&lt;</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>9</td>
      <td>29</td>
      <td></td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>window.navigator.platform</td>
      <td>2017-12-16T05:43:41.026Z</td>
      <td>Linux x86_64</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1f.td_0f</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>62</td>
      <td>207</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T05:43:41.385Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1f.td_0f</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>62</td>
      <td>207</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.vendor</td>
      <td>2017-12-16T05:43:41.386Z</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1f.td_0f</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>62</td>
      <td>207</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.platform</td>
      <td>2017-12-16T05:43:41.386Z</td>
      <td>Linux x86_64</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1f.td_0f</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>62</td>
      <td>207</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.appVersion</td>
      <td>2017-12-16T05:43:41.386Z</td>
      <td>5.0 (X11)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>131</td>
      <td>94</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T05:43:41.394Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>222</td>
      <td>94</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T05:43:41.394Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>82</td>
      <td>95</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.mimeTypes[application/futuresplash].type</td>
      <td>2017-12-16T05:43:41.395Z</td>
      <td>application/futuresplash</td>
    </tr>
    <tr>
      <th>9</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>82</td>
      <td>95</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.mimeTypes[application/x-shockwave-flash].type</td>
      <td>2017-12-16T05:43:41.395Z</td>
      <td>application/x-shockwave-flash</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>8</td>
      <td>99</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.screen.colorDepth</td>
      <td>2017-12-16T05:43:41.399Z</td>
      <td>24</td>
    </tr>
    <tr>
      <th>11</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_C0</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>106</td>
      <td>123</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].name</td>
      <td>2017-12-16T05:43:41.401Z</td>
      <td>Shockwave Flash</td>
    </tr>
    <tr>
      <th>12</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_C0</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>147</td>
      <td>123</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].name</td>
      <td>2017-12-16T05:43:41.401Z</td>
      <td>Shockwave Flash</td>
    </tr>
    <tr>
      <th>13</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_C0</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>2</td>
      <td>124</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].description</td>
      <td>2017-12-16T05:43:41.401Z</td>
      <td>Shockwave Flash 28.0 r0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_cL</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>136</td>
      <td>130</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.platform</td>
      <td>2017-12-16T05:43:41.401Z</td>
      <td>Linux x86_64</td>
    </tr>
    <tr>
      <th>15</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_cL</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>136</td>
      <td>130</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.platform</td>
      <td>2017-12-16T05:43:41.401Z</td>
      <td>Linux x86_64</td>
    </tr>
    <tr>
      <th>16</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>44</td>
      <td>102</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].name</td>
      <td>2017-12-16T05:43:41.402Z</td>
      <td>Shockwave Flash</td>
    </tr>
    <tr>
      <th>17</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>44</td>
      <td>102</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].description</td>
      <td>2017-12-16T05:43:41.402Z</td>
      <td>Shockwave Flash 28.0 r0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>44</td>
      <td>102</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].filename</td>
      <td>2017-12-16T05:43:41.403Z</td>
      <td>libflashplayer.so</td>
    </tr>
    <tr>
      <th>19</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_1l</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>44</td>
      <td>102</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>window.navigator.plugins[Shockwave Flash].length</td>
      <td>2017-12-16T05:43:41.403Z</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>{"0":"2d"}</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_2W</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>call</td>
      <td>176</td>
      <td>56</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>HTMLCanvasElement.getContext</td>
      <td>2017-12-16T05:43:41.404Z</td>
      <td></td>
    </tr>
    <tr>
      <th>21</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_2W</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>get</td>
      <td>28</td>
      <td>57</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>CanvasRenderingContext2D.font</td>
      <td>2017-12-16T05:43:41.405Z</td>
      <td>10px sans-serif</td>
    </tr>
    <tr>
      <th>22</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_2W</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>set</td>
      <td>71</td>
      <td>57</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>HTMLCanvasElement.width</td>
      <td>2017-12-16T05:43:41.406Z</td>
      <td>300</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_2W</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>set</td>
      <td>87</td>
      <td>57</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>HTMLCanvasElement.height</td>
      <td>2017-12-16T05:43:41.406Z</td>
      <td>100</td>
    </tr>
    <tr>
      <th>24</th>
      <td>{"0":"2d"}</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_2W</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>call</td>
      <td>110</td>
      <td>57</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>HTMLCanvasElement.getContext</td>
      <td>2017-12-16T05:43:41.406Z</td>
      <td></td>
    </tr>
    <tr>
      <th>25</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>3</td>
      <td>td_2W</td>
      <td>True</td>
      <td>https://signin.ebay.com.hk/t_n.html?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e&amp;suppressFlash=true</td>
      <td>set</td>
      <td>12</td>
      <td>58</td>
      <td></td>
      <td>https://src.ebay-us.com/fp/check.js?org_id=usllpic0&amp;session_id=5dd9736e1600acc3dc202f90fff4f20e</td>
      <td>CanvasRenderingContext2D.font</td>
      <td>2017-12-16T05:43:41.407Z</td>
      <td>8px Arial</td>
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
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>[8]&lt;/&lt;/E</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>23332</td>
      <td>4</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T22:56:00.338Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>r</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>20639</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T22:56:00.501Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.552Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.553Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>8</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.553Z</td>
      <td></td>
    </tr>
    <tr>
      <th>9</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.554Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>10</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.554Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>11</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.554Z</td>
      <td></td>
    </tr>
    <tr>
      <th>12</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>f</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>4236</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.navigator.userAgent</td>
      <td>2017-12-16T22:56:00.560Z</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.775Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>14</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.776Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>15</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.776Z</td>
      <td></td>
    </tr>
    <tr>
      <th>16</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.777Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>17</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.777Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>18</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.777Z</td>
      <td></td>
    </tr>
    <tr>
      <th>19</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.779Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>20</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.779Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>21</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.779Z</td>
      <td></td>
    </tr>
    <tr>
      <th>22</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.819Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>23</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.819Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>24</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.820Z</td>
      <td></td>
    </tr>
    <tr>
      <th>25</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.822Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>26</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>get</td>
      <td>21702</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T22:56:00.823Z</td>
      <td>{"adcashufpv3":"98769fa110ed831803f220b47f5cb456","taboola global:user-id":"94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9","animeid:session-data":"v2_658284d15c8f830e92c29ed7438c543e_94459edd-d6d2-4836-a647-4c248b0676df-tuct12f26d9_1513464957_1513464957_CIi3jgYQ3p5DGKWWqoyGLCABKAMw4QE","taboola global:local-storage-keys":"[\"animeid:session-data\",\"taboola global:user-id\"]"}</td>
    </tr>
    <tr>
      <th>27</th>
      <td>{"0":"dev"}</td>
      <td></td>
      <td>1</td>
      <td>9</td>
      <td>a</td>
      <td>False</td>
      <td>https://www.animeid.tv/genero/primavera-2014</td>
      <td>call</td>
      <td>21716</td>
      <td>6</td>
      <td></td>
      <td>https://vidstat.taboola.com/vpaid/vPlayer/player/v8.3.7/OvaMediaPlayer.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T22:56:00.823Z</td>
      <td></td>
    </tr>
    <tr>
      <th>0</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>10</td>
      <td>match/g.forgetMatches</td>
      <td>True</td>
      <td>https://ih.adscale.de/adscale-ih/map?ssl=1&amp;format=video&amp;nut&amp;uu=403411513454937142</td>
      <td>get</td>
      <td>1</td>
      <td>1</td>
      <td></td>
      <td>https://js.adscale.de/match.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T20:09:12.295Z</td>
      <td>{"unsent-matches":"[{\"tpid\":38,\"tpuid\":\"CAESEHdTMH4KUb7UuY0F_JbADto\"},{\"tpid\":48,\"tpuid\":\"87279397a87f693c007cddcf1e5e3706\"},{\"tpid\":60,\"tpuid\":\"f0e0785a-1309-4847-986d-bb1c1b9e4df8\"},{\"tpid\":101,\"tpuid\":\"BBID-01-01881689408131165\"},{\"tpid\":72,\"tpuid\":\"6500239471295461400\"},{\"tpid\":42,\"tpuid\":\"8454069888780563120\"},{\"tpid\":75,\"tpuid\":\"6570173748852387650\"}]"}</td>
    </tr>
    <tr>
      <th>1</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>10</td>
      <td>match/g.recallMatches</td>
      <td>True</td>
      <td>https://ih.adscale.de/adscale-ih/map?ssl=1&amp;format=video&amp;nut&amp;uu=403411513454937142</td>
      <td>get</td>
      <td>137</td>
      <td>1</td>
      <td></td>
      <td>https://js.adscale.de/match.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T20:09:12.296Z</td>
      <td>{"unsent-matches":"[{\"tpid\":38,\"tpuid\":\"CAESEHdTMH4KUb7UuY0F_JbADto\"},{\"tpid\":48,\"tpuid\":\"87279397a87f693c007cddcf1e5e3706\"},{\"tpid\":60,\"tpuid\":\"f0e0785a-1309-4847-986d-bb1c1b9e4df8\"},{\"tpid\":101,\"tpuid\":\"BBID-01-01881689408131165\"},{\"tpid\":72,\"tpuid\":\"6500239471295461400\"},{\"tpid\":42,\"tpuid\":\"8454069888780563120\"},{\"tpid\":75,\"tpuid\":\"6570173748852387650\"}]"}</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>10</td>
      <td>match/g.recallMatches</td>
      <td>True</td>
      <td>https://ih.adscale.de/adscale-ih/map?ssl=1&amp;format=video&amp;nut&amp;uu=403411513454937142</td>
      <td>get</td>
      <td>163</td>
      <td>1</td>
      <td></td>
      <td>https://js.adscale.de/match.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T20:09:12.296Z</td>
      <td>{"unsent-matches":"[{\"tpid\":38,\"tpuid\":\"CAESEHdTMH4KUb7UuY0F_JbADto\"},{\"tpid\":48,\"tpuid\":\"87279397a87f693c007cddcf1e5e3706\"},{\"tpid\":60,\"tpuid\":\"f0e0785a-1309-4847-986d-bb1c1b9e4df8\"},{\"tpid\":101,\"tpuid\":\"BBID-01-01881689408131165\"},{\"tpid\":72,\"tpuid\":\"6500239471295461400\"},{\"tpid\":42,\"tpuid\":\"8454069888780563120\"},{\"tpid\":75,\"tpuid\":\"6570173748852387650\"}]"}</td>
    </tr>
    <tr>
      <th>3</th>
      <td>{"0":"unsent-matches"}</td>
      <td></td>
      <td>1</td>
      <td>10</td>
      <td>match/g.recallMatches</td>
      <td>True</td>
      <td>https://ih.adscale.de/adscale-ih/map?ssl=1&amp;format=video&amp;nut&amp;uu=403411513454937142</td>
      <td>call</td>
      <td>165</td>
      <td>1</td>
      <td></td>
      <td>https://js.adscale.de/match.js</td>
      <td>window.Storage.getItem</td>
      <td>2017-12-16T20:09:12.297Z</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>NaN</td>
      <td></td>
      <td>1</td>
      <td>10</td>
      <td>match/g.forgetMatches</td>
      <td>True</td>
      <td>https://ih.adscale.de/adscale-ih/map?ssl=1&amp;format=video&amp;nut&amp;uu=403411513454937142</td>
      <td>get</td>
      <td>867</td>
      <td>1</td>
      <td></td>
      <td>https://js.adscale.de/match.js</td>
      <td>window.localStorage</td>
      <td>2017-12-16T20:09:12.298Z</td>
      <td>{"unsent-matches":"[{\"tpid\":38,\"tpuid\":\"CAESEHdTMH4KUb7UuY0F_JbADto\"},{\"tpid\":48,\"tpuid\":\"87279397a87f693c007cddcf1e5e3706\"},{\"tpid\":60,\"tpuid\":\"f0e0785a-1309-4847-986d-bb1c1b9e4df8\"},{\"tpid\":101,\"tpuid\":\"BBID-01-01881689408131165\"},{\"tpid\":72,\"tpuid\":\"6500239471295461400\"},{\"tpid\":42,\"tpuid\":\"8454069888780563120\"},{\"tpid\":75,\"tpuid\":\"6570173748852387650\"}]"}</td>
    </tr>
    <tr>
      <th>5</th>
      <td>{"0":"unsent-matches","1":"[]"}</td>
      <td></td>
      <td>1</td>
      <td>10</td>
      <td>match/g.forgetMatches</td>
      <td>True</td>
      <td>https://ih.adscale.de/adscale-ih/map?ssl=1&amp;format=video&amp;nut&amp;uu=403411513454937142</td>
      <td>call</td>
      <td>867</td>
      <td>1</td>
      <td></td>
      <td>https://js.adscale.de/match.js</td>
      <td>window.Storage.setItem</td>
      <td>2017-12-16T20:09:12.298Z</td>
      <td></td>
    </tr>
  </tbody>
</table>
<p>216 rows × 15 columns</p>
</div>




```python
#Get count for each TDL
result = sample_data.sample_random_files(files)
result
```

    match found!  script_url:  twitter.com calledFrom:  platform.twitter.com
    match found!  script_url:  googlesyndication.com calledFrom:  tpc.googlesyndication.com
    match found!  script_url:  googlesyndication.com calledFrom:  tpc.googlesyndication.com
    match found!  script_url:  ebay.com.hk calledFrom:  signin.ebay.com.hk
    match found!  script_url:  ebay.com calledFrom:  signin.ebay.com.hk
    match found!  script_url:  criteo.net calledFrom:  static.criteo.net
    match found!  script_url:  criteo.com calledFrom:  sslwidget.criteo.com
    match found!  script_url:  googlesyndication.com calledFrom:  pagead2.googlesyndication.com
    match found!  script_url:  outbrain.com calledFrom:  widgets.outbrain.com
    match found!  script_url:  youtube.com calledFrom:  www.youtube.com
    match found!  script_url:  youtube.com calledFrom:  www.youtube.com
    match found!  script_url:  taboola.com calledFrom:  vidstat.taboola.com
    match found!  script_url:  adscale.de calledFrom:  js.adscale.de
    




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
      <th>properties</th>
      <th>resources</th>
      <th>sites</th>
      <th>count</th>
      <th>calledFrom</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Criteo</th>
      <td>[criteo.com, criteo.net]</td>
      <td>[criteo.com, criteo.net, hooklogic.com, hlserve.com]</td>
      <td>{criteo.net, hlserve.com, hooklogic.com, criteo.com}</td>
      <td>2</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>Google</th>
      <td>[abc.xyz, google.com, ingress.com, admeld.com, blogger.com, google-melange.com, google.ad, google.ae, google.com.af, google.com.ag, google.com.ai, google.al, google.am, google.co.ao, google.com.ar, google.as, google.at, google.com.au, google.az, google.ba, google.com.bd, google.be, google.bf, google.bg, google.com.bh, google.bi, google.bj, google.com.bn, google.com.bo, google.com.br, google.bs, google.bt, google.co.bw, google.by, google.com.bz, google.ca, google.cd, google.cf, google.cg, google.ch, google.ci, google.co.ck, google.cl, google.cm, google.cn, google.com.co, google.co.cr, google.com.cu, google.cv, google.com.cy, google.cz, google.de, google.dj, google.dk, google.dm, google.com.do, google.dz, google.com.ec, google.ee, google.com.eg, google.es, google.com.et, google.fi, google.com.fj, google.fm, google.fr, google.ga, google.ge, google.gg, google.com.gh, google.com.gi, google.gl, google.gm, google.gp, google.gr, google.com.gt, google.gy, google.com.hk, google.hn, google.hr, google.ht, google.hu, google.co.id, google.ie, google.co.il, google.im, google.co.in, google.iq, google.is, google.it, google.je, google.com.jm, google.jo, google.co.jp, google.co.ke, google.com.kh, google.ki, google.kg, google.co.kr, google.com.kw, ...]</td>
      <td>[google.com, 2mdn.net, admeld.com, admob.com, cc-dt.com, destinationurl.com, doubleclick.net, gmail.com, google-analytics.com, googleadservices.com, googlemail.com, googlesyndication.com, googlevideo.com, googletagservices.com, invitemedia.com, postrank.com, smtad.net, apture.com, blogger.com, ggpht.com, gmodules.com, googleapis.com, googleusercontent.com, gstatic.com, recaptcha.net, youtube.com, googletagmanager.com]</td>
      <td>{google.td, google.ba, googleusercontent.com, google.co.cr, google.cm, google.bj, google.com.bo, google.co.jp, cc-dt.com, google.am, google.co.ao, google.ml, google.be, google.bf, google.com.br, google.com.gi, google.st, google.co.uz, google.cz, recaptcha.net, google.com.ai, google.is, google.com.kh, google.bs, google.vg, google.com.co, google.dk, google.gp, google.sn, google.co.ck, google.com.om, google.com.bn, google.com.pa, google.co.ve, google.ie, google.tk, google.cg, google.fi, googlevideo.com, google.tn, google.ae, 2mdn.net, google.as, google.com.bd, panoramio.com, google.cn, google.com, google.com.my, googlemail.com, google.co.il, google.ws, google.ch, google.com.py, google.im, google.ad, google.com.uy, admeld.com, google.com.qa, googlesyndication.com, google.cv, google.hu, google.com.tj, google.co.zw, google.ki, google.de, google.cat, google.nr, google.rs, google-analytics.com, google.lt, google.si, google.to, google.com.pk, google.com.gt, google.com.ly, google.co.ug, abc.xyz, google.by, google.pt, google.com.vn, google.ga, google.pl, apture.com, google.com.bz, google.no, google.co.za, google.ne, google.ci, google.com.kw, google.nu, google.com.ua, google.co.id, google.co.kr, postrank.com, google.co.uk, googleapis.com, google.az, google.com.sl, google.com.eg, google.ps, ...}</td>
      <td>5</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>Outbrain</th>
      <td>[outbrain.com, sphere.com]</td>
      <td>[outbrain.com, sphere.com, visualrevenue.com]</td>
      <td>{outbrain.com, visualrevenue.com, sphere.com}</td>
      <td>1</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>Taboola</th>
      <td>[taboola.com]</td>
      <td>[taboola.com, perfectmarket.com]</td>
      <td>{perfectmarket.com, taboola.com}</td>
      <td>1</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>Twitter</th>
      <td>[twitter.com, crashlytics.com, tweetdeck.com, twitter.jp, digits.com, fabric.io]</td>
      <td>[twitter.com, backtype.com, crashlytics.com, tweetdeck.com, twimg.com, twitter.jp, fabric.io]</td>
      <td>{twitter.com, fabric.io, crashlytics.com, twitter.jp, twimg.com, digits.com, backtype.com, tweetdeck.com}</td>
      <td>1</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>adscale</th>
      <td>[stroeer.de]</td>
      <td>[stroeer.de, adscale.de]</td>
      <td>{stroeer.de, adscale.de}</td>
      <td>1</td>
      <td>[]</td>
    </tr>
    <tr>
      <th>eBay</th>
      <td>[ebay.com, ebay.at, ebay.ba, ebay.be, ebay.com.au, ebay.ca, ebay.ch, ebay.cn, ebay.de, ebay.es, ebay.fr, ebay.com.hk, ebay.ie, ebay.in, ebay.it, ebay.co.jp, ebay.co.kr, ebay.com.my, ebay.nl, ebay.com.ph, ebay.pl, ebay.com.sg, ebay.com.tw, ebay.co.uk, gopjn.com]</td>
      <td>[ebay.com, gopjn.com]</td>
      <td>{ebay.ba, ebay.pl, ebay.com.sg, ebay.co.kr, ebay.es, ebay.cn, ebay.ca, ebay.com.tw, ebay.co.uk, gopjn.com, ebay.com.my, ebay.com.hk, ebay.at, ebay.ch, ebay.in, ebay.de, ebay.co.jp, ebay.nl, ebay.com.au, ebay.be, ebay.fr, ebay.it, ebay.ie, ebay.com, ebay.com.ph}</td>
      <td>2</td>
      <td>[]</td>
    </tr>
  </tbody>
</table>
</div>




```python
result.plot(kind="bar")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x210625f24e0>




![png](output_4_1.png)

