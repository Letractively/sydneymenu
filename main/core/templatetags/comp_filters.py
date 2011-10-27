from django import template
import os
from lxml import etree
from .. import inc 

register = template.Library()

class SelectRender:
  def __init__(self,name):
    self.name = name
    self.style = "" 
    self.fields = []
    self.default = None 
  def Render(self):
    default = "NIL"
    dstr = ""
    if(self.default):
      default = self.default
      dstr = self.default
    rend_result = """\
<div class="extension-drop-list" style="%s">\
<input type="textfield" style="display:none" name="%s" value="%s"></input>\
<div class='current'>%s</div><ul>"""\
    % (self.style,self.name,dstr,default)
    for field in self.fields:
      if (field == self.default):
        rend_result += "<li><h5>"+field+"</h5><span>&#9746</span></li>"
      else:
        rend_result += "<li><h5>"+field+"</h5><span>&#9744</span></li>"
    tail = """</ul></div>"""
    return rend_result+tail
  def AddField(self,field_name):
    self.fields.append(field_name)
    if (self.default == None):
      self.default = field_name
  def SetStyle(self,style):
    self.style = style

class ComboRender:
  def __init__(self, name):
    self.name = name
    self.style = ""
    self.fields = []
  def Render(self):
    rend_result = """\
<div class="extension-combo-select" style="%s">\
<input type="textfield" style="display: none" name="%s" value="%s"/>\
<div class='current'>MIXED</div><ul>"""\
    % (self.style, self.name, ",".join(self.fields))
    for field in self.fields:
      rend_result += "<li><h5>" + field + "</h5><span>&#9744</span></li>"
    tail = """</ul></div>"""
    return rend_result + tail
  def AddField(self, field_name):
    self.fields.append(field_name)
  def SetStyle(self, style):
    self.style = style

class DictRender:
  def __init__(self,name):
    self.name = name
    self.style = ""
    self.dictionary = {}
  def Render(self):
    rend_result = """\
<div class="extension-dict-select" style="%s">\
<input type="textfield" style="display:none" name="%s" />\
<div class='current'>NIL</div><ul class='key'>"""\
    % (self.style,self.name)
    for k in self.dictionary.keys():
      rend_result += "<li class='key'><span class='key'>" + k  + "</span><ul class='item'>"
      for v in self.dictionary[k]:
        rend_result += "<li class='item'><h5>" + v + "</h5></li>"
      rend_result += "</ul></li>"
    rend_result += "</ul>"
    rend_result += "</div>"
    return rend_result
  def SetStyle(self,style):
    self.style = style
  def AddField(self,dic):
    self.dictionary = dic

class AutoCompleteRender:
  def __init__(self, name):
    self.name = name
    self.style = ""
    self.call_back = ""
    self.fields = []
  def Render(self):
    rend_result = """\
<div class="extension-auto-complete" style="%s">\
<!--call_back:%s-->\
<input type="textfield" name="%s"/>\
<div class="autocomp-drop-list"><ul class="hint"></ul>\
</div>\
</div>"""\
    % (self.style,self.call_back,self.name)
    return rend_result
  def SetStyle(self, style):
    self.style = style
  def SetCallBack(self,cb):
    self.call_back = cb

@register.filter("auto_complete")
def auto_complete(acname):
  return AutoCompleteRender(acname)

@register.filter("combo")
def combo(comboname):
  return ComboRender(comboname)

@register.filter("dictionary")
def dictionary(name):
  return DictRender(name)

@register.filter("post")
def post(pname,sname):
  f = open(inc.CONFIG.SERVICES_PATH + sname+'/' + pname + '.post',"r")
  buf = f.read()
  f.close()
  return buf

@register.filter("template")
def template(cname):
  return "comp/_"+cname+".html"


@register.filter("select")
def select(selectname):
  return SelectRender(selectname)

@register.filter("style")
def style(ele_config,style):
  ele_config.SetStyle(style)
  return ele_config

@register.filter("addfield")
def addfield(ele_config,field):
  ele_config.AddField(field)
  return ele_config

@register.filter("callback")
def callback(ele_config,cb):
  ele_config.SetCallBack(cb)
  return ele_config
 
@register.filter("render")
def render(ele_config):
  return ele_config.Render()

@register.filter("xslt")
def xslt(xslt,item):
  return etree.tostring(xslt(item.getroot()))

@register.simple_tag
def xattr(item,path):
  if item:
    return item.xpath(path)[0]
  else:
    return "None" 
