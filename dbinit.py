import os, sys
os.path.join(os.path.abspath('..'), 'sydneymenu', 'main')
sys.path.append(os.path.join(os.path.abspath('..'), 'sydneymenu', 'main'))

#print sys.path
print "-----------------"
os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'

from main.core.models import ServiceRel 
from main.pybb.models import Forum,Category

try:
    get_undefined_record = ServiceRel.objects.get(name='undefined')
except ServiceRel.DoesNotExist:
    blank_rel_record = ServiceRel(name='undefined')
    blank_rel_record.save()
try:
    get_category = Category.objects.get(name='Services')
except Category.DoesNotExist:
    category_record = Category(name='Services')
    category_record.save()
try:
    get_category = Category.objects.get(name='Issues')
except Category.DoesNotExist:
    category_record = Category(name='Issues')
    category_record.save()
 
    print 'Initial record has been inserted'
    
print 'Database has been initialized'
