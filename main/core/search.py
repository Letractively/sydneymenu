from user import *
from django.db.models import Q

def BuildQueryReg(sstr,spath):
  reg = re.compile("[a-zA-Z]+")
  itms = reg.finditer(sstr)
  reg_str = [] 
  for t in itms:
    reg_str.append(t.group()) 
  if reg_str:
    reg_exp = "("+"|".join(reg_str)+")" 
    return reg_exp
  else:
    return None

def ComputeDistance(latlong1,latlong2):
  r = 6371
  dlat = Rad(latlong1['lat'] - latlong2['lat'])
  dlong = Rad(latlong1['long'] - latlong2['long'])
  a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(Rad(latlong1['lat']))*math.cos(Rad(latlong2['lat']))*math.sin(dlong/2)*math.sin(dlong/2)
  c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a));
  return r*c 


def FiltByDistance(services,llbase,radius):
  results = []
  if llbase['lat'] and llbase['long'] and radius:
    for service in services:
      llinc = {'lat':float(service.latitude)/1000000,'long':float(service.longitude)/1000000}
      dis = ComputeDistance(llbase,llinc)
      if(dis < radius):
        results.append(service)
  else:
    for service in services:
      results.append(service)
  return results

