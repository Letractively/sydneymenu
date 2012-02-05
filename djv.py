try:
  import django
  ver = django.VERSION
  print "Current Django Version : " + ver.__str__()
  if (ver[0] == 1 and ver[1] >= 3):
    exit(0)
  else:
    exit(1)
except ImportError:
  print "Django Not Installed ..."
  exit(2)
