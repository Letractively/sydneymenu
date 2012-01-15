from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from user import * 

import md5
import urllib
import time
from datetime import datetime

class FacebookConnectMiddleware(object):
  delete_fb_cookies = False
  facebook_user_is_authenticated = False
  def process_request(self, request):
    try:
      if request.user.is_authenticated():
      ### Nothing to do with logged in user
        return;
      if not CONFIG.FB_API_KEY in request.COOKIES:
        return;
      signature_hash = self.get_facebook_signature(request.COOKIES, True)
      # The hash of the values in the cookie to make sure they're not forged
      if(signature_hash != request.COOKIES[CONFIG.FB_API_KEY]):
        return;
      # If session hasn't expired
      if(datetime.fromtimestamp(float(request.COOKIES[CONFIG.FB_API_KEY+'_expires'])) < datetime.now()):
        return;
      # Make request to FB API to get user's first and last name
      user_info_params = {
                'method': 'Users.getInfo',
                'api_key': CONFIG.FB_API_KEY,
                'call_id': time.time(),
                'v': '1.0',
                'uids': request.COOKIES[CONFIG.FB_API_KEY + '_user'],
                'fields': 'first_name,last_name',
                'format': 'json',
      }
      user_info_hash = self.get_facebook_signature(user_info_params)
      user_info_params['sig'] = user_info_hash
      user_info_params = urllib.urlencode(user_info_params)
      user_info_response  = json.loads(urllib.urlopen(CONFIG.FB_REST_SERVER, user_info_params))

      zoyoe_usr_name = request.COOKIES[CONFIG.FB_API_KEY + '_user']
      zoyoe_password = request.COOKIES[CONFIG.FB_API_KEY + '_user'] + CONFIG.FB_SECRET_KEY
      zoyoe_password = md5.new(zoyoe_password).hexdigest()


      zoyoe_email = user_info_response[0]['email']

      try:
      # Authenticate then login (or display disabled error message)
        django_user = User.objects.get(username=zoyoe_usr_name)
        user = authenticate(username = "fb_" + zoyoe_usr_name,password= zoyoe_password)
        if (user is not None) and user.is_active:
          login(request, user)
          self.facebook_user_is_authenticated = True
        else:
          self.delete_fb_cookies = True
      except User.DoesNotExist:
      # There is no Django account for this Facebook user.
      # Create one, then log the user in.
        # Create user
        user = User.objects.create_user('fb_' + zoyoe_usr_name, zoyoe_email, zoyoe_password)
        user.save()
        user = authenticate(username='fb_' + zoyoe_usr_name,
                        password=zoyoe_password)
        if (user is not None) and user.is_active:
          login(request, user)
          self.facebook_user_is_authenticated = True
        else:
          self.delete_fb_cookies = True
    except:
      return 

  def process_response(self, request, response):        
    if self.delete_fb_cookies is True:
      response.delete_cookie(CONFIG.FB_API_KEY + '_user')
      response.delete_cookie(CONFIG.FB_API_KEY + '_session_key')
      response.delete_cookie(CONFIG.FB_API_KEY + '_expires')
      response.delete_cookie(CONFIG.FB_API_KEY + '_ss')
      response.delete_cookie(CONFIG.FB_API_KEY)
      response.delete_cookie('fbsetting_' + CONFIG.FB_API_KEY)
      self.delete_fb_cookies = False
    return response
                                
  # Generates signatures for FB requests/cookies
  def get_facebook_signature(self, values_dict, is_cookie_check=False):
      signature_keys = []
      for key in sorted(values_dict.keys()):
          if (is_cookie_check and key.startswith(CONFIG.FB_API_KEY + '_')):
              signature_keys.append(key)
          elif (is_cookie_check is False):
              signature_keys.append(key)

      if (is_cookie_check):
          signature_string = ''.join(['%s=%s' % (x.replace(CONFIG.FB_API_KEY + '_',''), values_dict[x]) for x in signature_keys])
      else:
          signature_string = ''.join(['%s=%s' % (x, values_dict[x]) for x in signature_keys])
      signature_string = signature_string + CONFIG.FB_API_SECRET
      return md5.new(signature_string).hexdigest()
