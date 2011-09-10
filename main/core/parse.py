import xml.sax
import commands
from main.models import *
from main.exceptions import *
from django.db.models import Q
from settings import SECRET_KEY 
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection 

class TagHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.types = {}
    self.sizes = {}
    # list to store all style="short" element
    self.short = []
    # ................. style="normal" element
    self.normal = []
    # ................. style="long" element
    self.long = []
    self.file_name = "main/models.py"
    self.table_existed = False
    self.table_prefix = "main_"
    self.INDENT = "  "

  # handle the new coming element.
  def startElement(self, name, attrs):
    if(self.table_existed):
      return
    name = name.encode('ascii')
    if(name == "ext_service"):
      return
    if(name == "table"):
      table_name = attrs.getValue("name")
      self.table_name = table_name
      if(self.existed_table(table_name)):
        self.table_existed = True
        return
    else:
      self.types[name] = attrs.getValue("type")

      # if the type is number, then label it to short
      if(self.types[name] == "number"):
        self.short.append({name: self.types[name]})

      # length > 1, means has type and size attribute
      if(attrs.getLength() != 1): 
        self.sizes[name] = attrs.getValue("size")

        # < 50 to be short
        if(int(self.sizes[name]) < 50):
          self.short.append({name: self.types[name]})

        # 50 <= size < 100 to be normal
        elif(int(self.sizes[name]) >= 50 and int(self.sizes[name]) < 100):
          self.normal.append({name: self.types[name]})

        # >= 100 to be long
        elif(int(self.sizes[name]) >= 100):
          self.long.append({name: self.types[name]})

  # see if the model exists, or have name confliction
  def existed_table(self, table_name):
    service_rels = ServiceRel.objects.all()
    try:
      service_rels.get(name = table_name.lower())
      return True
    except ObjectDoesNotExist:
      return False

  # write out the new Model to models.py
  def write_out_model(self):
    output = open(self.file_name, "a")
    output.write("\n#Create automatically based on input XML\n")
    output.write("class " + self.table_name.title() + "(models.Model):\n")
    for field, field_type in self.types.iteritems():
      if(self.sizes.has_key(field)):
        output.write(self.INDENT + field + " = " + self.get_field_type(field_type, self.sizes[field]) + "\n")
      else:
        output.write(self.INDENT + field + " = " + self.get_field_type(field_type, 0) + "\n")
    output.close()

  def add_new_db_entry(self):
    extend_table = ServiceRel(name=self.table_name, description="")
    
    # loop to write short elements
    for short_item in self.short:
      for field, type in short_item.iteritems():
        extend_table.description += "<input type=\"text\" name=\"" + field + "\" class=\"ddb-short\"/>"

    # loop to write normal elements
    for normal_item in self.normal:
      for field, type in normal_item.iteritems():
        extend_table.description += "<input type=\"text\" name=\"" + field + "\" class=\"ddb-normal\" />"
    
    # loop to write long elements
    for long_item in self.long:
      for field, type in long_item.iteritems():
        extend_table.description += "<input type=\"text\" name=\"" + field + "\" class=\"ddb-long\" />"

    extend_table.save()

  # return the related content type, which needs to be written in the models.py
  def get_field_type(self, raw_type, size):
    type_string = "models."
    if(raw_type == "text"):
      return type_string + "CharField(max_length = " + size + ")"
    elif(raw_type == "number"):
      return type_string + "IntegerField()"
    elif(raw_type == "bool"):
      return type_string + "BooleanField()"

def HandleXML():
  xml_file = "/home/hjbolide/data.xml"
  xml_parser = xml.sax.make_parser()
  handler = TagHandler()
  xml_parser.setContentHandler(handler)
  xml_parser.parse(xml_file)
  if (handler.table_existed == True):
    raise TableExistsException("Table exists, sorry")
  handler.write_out_model()
  handler.add_new_db_entry()

def HandleXMLsandbox():
  try: 
    HandleXML()
  except TableExistsException:
    return "Table existed, sorry"
  return "Please sync your db"

def reset():

  handler = TagHandler()

  # reset all the service core
  # extend field set to 'undifined'
  service_cores = ServiceCore.objects.all()
  undefined_servicerel = ServiceRel.objects.get(name='undefined')
  for service_core in service_cores:
    service_core.extend = undefined_servicerel
    service_core.save()
  
  # delete the relationship between ext_service and service_core
  service_rels = ServiceRel.objects.filter(~Q(name='undefined'))
  cursor = connection.cursor()

  # loop to delete the extend tables
  for service_rel in service_rels:
    cursor.execute("DROP TABLE " + handler.table_prefix + service_rel.name)
  service_rels.delete()

  # delete the class from models
  original_end = False

  model_file = file('main/models.py')
  content = model_file.readlines()
  model_file.close()

  new_content = "" 
  for line in content:
    if(original_end):
      break
    if SECRET_KEY in line:
      original_end = True
    new_content += line
  output = open('main/models.py', 'w')
  output.write(new_content)
  output.close()
  return "Reset has been done, please sync your db"
