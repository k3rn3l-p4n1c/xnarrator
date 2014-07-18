import json
import requests
from requests.exceptions import ConnectionError
from urllib2 import urlopen
import picwork
import os
 
def download(query, path = "./data/pics/"):
  """Download full size images from Google image search."""
  BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/images?'\
             'v=1.0&q=' + 'cartoon ' + query + '&start=%d'
  
  start = 0
  while start<20:
	  r = requests.get(BASE_URL % start)
	  print 'download',query
	  for image_info in json.loads(r.text)['responseData']['results']:
	    url = image_info['unescapedUrl']
	    print 'url: ',url,
	    try:
	      newFile = '{}{}.{}'.format(path,query+'_0_3',url[-3:])
	      f = open(newFile, 'wb')
	      f.write(urlopen(url).read())
	      f.close()
	    except:
	      print 'error'
	      start += 4
	      continue
	    print 'Download done'
	    try:
	    	t = picwork.transparent(path+query+'_0_3.'+url[-3:],path+query+'_0_3')
	    except:
	      print 'error2'
	      start += 4
	      continue
	    if t < 10:
	    	break
	    return
	  print 'No download'
	  start += 4
              
#download('xperia','./data/pics/')
