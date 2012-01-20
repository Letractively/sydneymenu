from core.user import * 
from core.inc import *
from glue.models import *

collect_handler = {'name':(name_patten,(lambda x:x),lambda x, v: (x.update(name = v)))}

