from core.inc import *


def Test(request):
  test_t = loader.get_template('test.html')
  dic = {"key0":["item0","item1","item2"],"key1":["item0","item1","item2"]}
  c = Context({'RANDOM':123,'DICT':dic})
  return HttpResponse(test_t.render(c))


