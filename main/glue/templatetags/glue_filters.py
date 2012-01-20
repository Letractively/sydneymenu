from django import template
from lxml import etree
import os
import json
from glue.models import *

register = template.Library()

@register.simple_tag
def collect(service,user):
  objs = UsersOfService(service) 
  msg = str(len(objs))
  msg += " users have collect this service in their local services."
  if(user.is_authenticated()):
    if(len(objs.filter(user = user))):
      msg += """<span class='btngray'
             style='float:right;top:-10px;position:relative;'>"""
      msg += """<a href='/glue/collection/personal/'>
              you have already collected this service
            </a>"""
      msg += "</span>"
    else:
      msg += """<span class='btnblue' onclick='zoyoe.admin.Collect()'
             style='float:right;top:-10px;position:relative;'>collect this service</span>"""
  else:
    msg += """<span class='btnblue' onclick='zoyoe.admin.Collect()'
             style='float:right;top:-10px;position:relative;'>collect this service</span>"""
  return msg
