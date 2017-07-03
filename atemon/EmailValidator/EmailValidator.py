"""
Copyright (c) 2014 Agile Technology Engineers Monastery - ATEMON.

Git Hub: https://github.com/atemon
Twitter: https://twitter.com/atemonastery

This file is part of EmailValidator library and distributed under the MIT license (MIT).

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

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
import subprocess
import re


class EmailValidator(object):
    """Check if given email is valid."""

    def nslookup_installed(self):
        """Check if nslookupo is installed."""
        p = subprocess.Popen(['which', 'nslookup'], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        try:
            assert out
        except:
            raise Exception("nslookup not installed/path not set!" + err)

        return True

    def valid_mx(self, domain):
        """Check if a valid mx is registered for email."""
        try:
            self.nslookup_installed()
        except:
            return True  # Valid email as we cant check with nslookup

        p = subprocess.Popen(['nslookup', '-query=mx', domain], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()

        try:
            return bool(re.search('mail exchanger', out))
        except:
            # raise Exception("Exception in DNS lookup!" + err)
            return False

    def is_valid(self, email=None):
        """Check validity of email."""
        if not email:
            return False

        # RFC 3696
        # In addition to restrictions on syntax, there is a length limit on email addresses.
        # That limit is a maximum of 64 characters (octets) in the "local part" (before the "@")
        # and a maximum of 255 characters (octets) in the domain part (after the "@") for a total
        # length of 320 characters. However, there is a restriction in RFC 2821 on the length of
        # an address in MAIL and RCPT commands of 254 characters. Since addresses that do not fit
        # in those fields are not normally useful, the upper limit on address lengths should
        # normally be considered to be 254.

        if len(email) > 254:
            return False

        parts = email.split('@')
        if len(parts) > 2 or len(parts[0]) > 64 or len(parts[1]) > 255:
            return False

        if not re.match('[a-z0-9\!\#\$\%\&\'\*\+\/\=\?\^\_\`\{\|\}\~\-]+(?:\.[a-z0-9\!\#\$\%\&\'\*\+\/\=\?\^\_\`\{\|\}\~\-]+)*', email.lower()):
            return False
        #  A valid mail exchange server is configured!
        return self.valid_mx(parts[1])
