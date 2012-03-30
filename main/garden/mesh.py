from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from core.user import * 

import md5
import urllib
import time
from datetime import datetime

def BuildCondition(xml_node):
   info = {}
   info['condition'] = xml_node.xpath('./condition')[0].get('data')
   info['temp_f'] = xml_node.xpath('./temp_f')[0].get('data')
   info['humidity'] = xml_node.xpath('./humidity')[0].get('data')
   info['icon'] = "http://www.google.com" + xml_node.xpath('./icon')[0].get('data')
   return info

def GetWeatherInfo():
   url = CONFIG.GOOGLE_WEATHER + "?weather=Sydney"
   xml_str = urllib.urlopen(url).read() 
   xml_root = etree.parse(StringIO(xml_str))
   current_node = xml_root.xpath("//current_conditions")[0]
   return BuildCondition(current_node)

def GetSensisServiceList(gear,plant):
   url = CONFIG.SENSIS_API_EP + "&categoryId=28436&query=soil"
   json_rslt = urllib.urlopen(url).read()
   results  = json.loads(json_rslt)
   return results
