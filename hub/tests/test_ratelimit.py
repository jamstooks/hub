from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase, override_settings

import django_cache_url
from mock import patch
from time import sleep
import sys


# @override_settings(BROWSE_RATE_LIMIT='10/5m') #  couldn't get this to work
@override_settings(
    CACHES={'default': django_cache_url.parse('locmem://hub_test')},
    RATELIMIT_ENABLE=True)
class RateLimitTestCase(TestCase):
    """
    Test rate limiting for specific urls
    """
    
    def setUp(self):
        pass

    def test_login(self):
        """
            11th request in succession should raise Ratelimited
        """
        url = reverse('login')
        error_count = 0
        for i in range(6):
            response = self.client.post(url, {'username': 'user'})
            if i <= 4:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 403)
            sleep(.2)

    def test_search(self):
        """
            101st request in succession should raise Ratelimited
        """
        # tried reloading the view with the updated settings
        # Keeping this failed attempt in here:
        # from hub.apps.browse.views import BrowseView
        # patch('hub.apps.browse.views.BrowseView', BrowseView)
        
        url = reverse('browse:browse', kwargs={'ct': 'video'})
        error_count = 0
        for i in range(6):
            response = self.client.get(url)
            if i <= 4:
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 403)
            sleep(.2)
