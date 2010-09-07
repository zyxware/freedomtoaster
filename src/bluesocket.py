#!/usr/bin/python
"""
Copyright (c) 2007 Cesar Oliveira

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
"""

import urllib;
import urllib2;
import cgi;
import time;

options = {
    'username' : "username",
    'password' : "password",
    'test_site' : "http://senecac.on.ca",
    'wait' : 300    # in seconds
};

while 1:
    seneca = urllib.urlopen(options['test_site']);

    if seneca.geturl() != options['test_site']:
        # We have been redirected to bluesocket

        map = { 
            'bs_name': options['username'],
            'bs_password': options['password'],
            '_FORM_SUBMIT': '1',
            'which_form' : 'reg',
            # source is our IP address. It's in the url
            'source' : cgi.parse_qs(seneca.geturl())['source'][0]
         };
        # encode to application/x-www-form-urlencoded
        encoded = urllib.urlencode(map);
        # if you want to disconnect, go to net2.senecac.on.ca/login.pl
        # and it will bring up the bluesocket popup
        urllib2.urlopen("https://net2.senecac.on.ca/login.pl", encoded);
    time.sleep(options['wait']);

