from main.models import *

class HandleRequest:
  
  def __init__(self, request):
    self.request = request
    
  
  def add_extend_data(self):
    table_name = ""
    for field, value in self.request.iteritems():
      if(field == "table_name"):
        table_name = value
        break
    item = eval(table_name)()
    for field, value in self.request.iteritems():
      if(field == "table_name"):
        continue
      setattr(item, field, value)

    item.save()

    
