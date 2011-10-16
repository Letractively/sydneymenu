from django import template
from user import * 
from glue.forum import *

register = template.Library()

def HistoryExplain(hs):
  if (hs.type == "POST_REMOVE"):
    return hs.who + " removed a post: '" + hs.para + "'"
  elif (hs.type == "POST_ADD"):
    return hs.who + " added a new post: '" + hs.para + "'"
  elif (hs.type == "IMAGE_ADD"):
    return hs.who + " added a new image in gallery: '" + hs.para + "'"
  elif (hs.type == "GIRL_ADD"):
    return hs.who + " added girl info: '" + hs.para + "'"
  elif (hs.type == "GIRL_REMOVE"):
    return hs.who + " removed girl info: '" + hs.para + "'"
  elif (hs.type == "REPORT"):
    plist = json.loads(hs.para)
    [address,lat,lon,t] = plist
    return hs.who + " shared his experience of %s in %s"%(unquote(t),hs.service)
 
def HistoryExplainXML(hs):
  if(hs.type == "REPORT"):
    plist = json.loads(hs.para)
    [address,lat,lon,t] = plist
    ret_str = """<REPORT name='%s' who='%s' type='%s'><latlong>%d,%d</latlong><address>%s</address></REPORT>"""%(hs.service,hs.who,t,lat,lon,address)
    return ret_str
  else:
    return "<REF/>"
 

@register.filter("hash")
def hash(dict,key):
  "Return the value of a key in a dictionary. "
  if(dict and dict.has_key(key)):
    return dict[key]
  else:
    return None

@register.filter("attr")
def attr(obj,key):
  "Return the value of a key in a obj. "
  if (obj):
    if(obj.hasattr(key)):
      return obj.getattr(key)
    else:
      return None
  else:
    return None

@register.filter("hs_explain")
def attr(obj):
    return HistoryExplain(obj)

@register.filter("hs_explain_xml")
def attr(obj):
    return HistoryExplainXML(obj)
