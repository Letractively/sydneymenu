from lxml import etree
from StringIO import StringIO

xsd_file = open('default.xsd') 
valid_file = open('test.xml')
form_xslt_file = open('form.xslt')
template_xslt_file = open('template.xslt')
try:
  schema_doc = etree.parse(xsd_file)
  print "Parse XSD:"
  schema = etree.XMLSchema(schema_doc)
  print "Parse XML:"
  valid_doc = etree.parse(valid_file)
  print "Parse form xslt:"
  form_xslt_doc = etree.parse(form_xslt_file)
  form_xslt = etree.XSLT(form_xslt_doc)
  print "Validation of test doc:"
  print schema.assertValid(valid_doc)
  form = form_xslt(schema_doc,name="'item'")
  print etree.tostring(form.getroot(),pretty_print = True)
except etree.XMLSyntaxError, e:
  print e
except etree.DocumentInvalid, e:
  print e.args
finally:
  print 'test-finished'
  xsd_file.close()
  form_xslt_file.close()
  valid_file.close()

