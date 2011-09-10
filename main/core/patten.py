import re
import sys
from ModelHelper import *
#
# The global patten used:
#
latlong_patten = re.compile("^-?\d+\.(\d)+$")
name_patten = re.compile("^[a-zA-Z\s_\-0-9,]+$")
type_patten = re.compile("^[a-zA-Z]+$")
email_patten = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
phone_patten = re.compile("[0-9\(\)\s]+")
grade_patten = re.compile("[0-9]+")
privilege_patten = re.compile("[a-zA-Z]+")
description_patten = re.compile(".+")
address_patten = re.compile("[a-zA-Z0-9\s]+")
url_patten = re.compile("((https?):((//)|(\\\\)))?[\w\d:#@%/;$()~_?\+-=\\\.&]*")
password_patten = re.compile("[a-zA-Z\d#@%]+")
number_patten = re.compile("[0-9-]+")  #FIX ME: This is really buggy
day_patten = re.compile("((Sun)|(Mon)|(Tue)|(Wed)|(Thu)|(Fri)|(Sat)|,)+")  #FIX ME: This is really buggy
layout_patten = re.compile("[a-zA-Z-]+")  #FIX ME: This is really buggy
time_range_patten = re.compile("[0-9]{1,2}:[0-9]{2}")
#
# Validate groups used to validate request input
#

set_timerange_handler = {'start':(time_range_patten,(lambda x:x),lambda x, v: (x.update(start = v)))
  ,'end':(time_range_patten,(lambda x:x),lambda x, v:(x.update(end=v)))}

addserv_handler = {
   'latitude':(latlong_patten,(lambda x: int(eval(x)*1000000)),lambda x, v: setattr(x,'latitude',v))
  ,'longitude':(latlong_patten,(lambda x: int(eval(x)*1000000)),lambda x, v: setattr(x,'longitude',v))
  ,'name':(name_patten,(lambda x:x),lambda x, v:setattr(x,'name',v))
  ,'type':(type_patten,(lambda x:x),lambda x, v:setattr(x,'type',v))
  ,'privilege':(privilege_patten,(lambda x:x),lambda x, v:setattr(x,'privilege',v))
  ,'email':(email_patten,(lambda x:x),lambda x, v:setattr(x,'email',v))
  ,'phone':(phone_patten,(lambda x:x),lambda x, v:setattr(x,'phone',v))
#  ,'grade':(grade_patten,(lambda x:eval(x)),lambda x, v:setattr(x,'grade',v))
  ,'aveage':(number_patten,(lambda x:x),lambda x, v:setattr(x,'aveage',v))
  ,'days':(day_patten,(lambda x:x),lambda x, v:setattr(x,'days',v))
#  ,'privilege':(privilege_patten,(lambda x:x),lambda x, v:setattr(x,'privilege',v))
  ,'description':(description_patten,(lambda x:x),lambda x, v:setattr(x,'description',v))
  ,'address':(address_patten,(lambda x:x),lambda x, v:setattr(x,'address',v))
  ,'icon':(url_patten,(lambda x:x),lambda x, v:setattr(x,'icon',v))}

mdyserv_handler = {
   'type':(type_patten,(lambda x:x),lambda x, v:setattr(x,'type',v))
  ,'phone':(phone_patten,(lambda x:x),lambda x, v:setattr(x,'phone',v))
  ,'aveage':(number_patten,(lambda x:x),lambda x, v:setattr(x,'aveage',v))
  ,'days':(day_patten,(lambda x:x),lambda x, v:setattr(x,'days',v))
  ,'description':(description_patten,(lambda x:x),lambda x, v:setattr(x,'description',v))}


addgirl_handler = {'name':(name_patten,(lambda x:x),lambda x, v: (x.update(name = v)))
  ,'age':(number_patten,(lambda x:x),lambda x, v:(x.update(age = v)))
  ,'size':(number_patten,(lambda x:x),lambda x, v:(x.update(size = v)))
  ,'description':(description_patten,(lambda x:x),lambda x, v:(x.update(description = v)))
  ,'icon':(url_patten,(lambda x:x),lambda x, v:(x.update(icon = v)))
  ,'nation':(name_patten,(lambda x:x),lambda x, v:(x.update(nation = v)))}

addgallery_handler = {'name':(name_patten,(lambda x:x),lambda x, v: (x.update(name = v)))}

addpost_handler = {'name':(name_patten,(lambda x:x),lambda x, v: (x.update(name = v)))}

login_validater = {'name':name_patten,'password':password_patten}

login_handler = {'name':(name_patten,(lambda x:x),lambda x, v:x.update(name = v))
    ,'password':(password_patten,(lambda x:x),lambda x, v:x.update(password = v))}

reg_handler = {'name':(name_patten,(lambda x:x),lambda x, v:x.update(name = v))
    ,'password':(password_patten,(lambda x:x),lambda x, v:x.update(password = v))
    ,'email':(email_patten,(lambda x:x),lambda x, v:x.update(email=v))}

pwd_handler = {'password':(password_patten,(lambda x:x),lambda x, v:x.update(password = v))}

addroster_handler = {'name':(name_patten,(lambda x:x),lambda x, v: (x.update(name = v)))}

delroster_handler = {'name':(name_patten,(lambda x:x),lambda x, v: (x.update(name = v)))}

savelayout_handler = {'left':(layout_patten,(lambda x:x),lambda x, v: (x.update(left = v.split(','))))
  ,'middle':(layout_patten,(lambda x:x),lambda x, v: (x.update(middle = v.split(','))))
  ,'right':(layout_patten,(lambda x:x),lambda x, v: (x.update(right = v.split(','))))}



#UNIT TEST
if __name__ == "__main__":
    try:
        assert command_validate['latitude'].match("151.202377")
        assert latlong_patten.match("-33.890049")
        assert not latlong_patten.match("-33.8900490")
        assert not latlong_patten.match("abc")
        assert not latlong_patten.match("abc.bcd")
        assert not latlong_patten.match("245.123")

        assert email_patten.match("p_ssg@hotmail.com")
        assert email_patten.match("gaoxin.braceup@gmail.com")

        assert name_patten.match("xin,gao")
        assert not name_patten.match("$xin,gao")

        assert phone_patten.match("0449832333")
        assert not phone_patten.match("aab0098765")

        assert url_patten.match ("http://www.google.com")
        assert url_patten.match ("http://www.google.com/test.jpg")
        assert not url_patten.match ("abd://http://www.google.com/test.jpg")
        print "data.py SUCCESSFUL"
    except AssertionError:
        print "data.py FAIL!"
