import os, apachelog, sys, shlex, subprocess, hashlib
from inc import *

def index(request):

  content = []

  subprocess.Popen("tail -n 100 " + CONFIG.LOG_PATH + "server.log > " + CONFIG.LOG_PATH + "server.log.tmp", shell=True)
  format = r'%v IP %l %u %t \"Request\" Status Bytes \"Referer\" \"User-Agent\"'
  dict = {}

  p = apachelog.parser(format)
  for line in open(CONFIG.LOG_PATH + 'server.log.tmp'):
    try:
      dict = p.parse(line)
      dict.pop("%v")
      dict.pop("%l")
      dict.pop("%u")
      dict['Time'] = dict.pop("%t")
      content.append(dict)
    except:
      sys.stderr.write("Unable to parse %s" % line)

  keys = content[0].keys()
  keys.remove('IP')

  t = loader.get_template('core/log.html')
  c = Context({
      'logList': content,
      'keys': keys,
  })
  return HttpResponse(t.render(c))
