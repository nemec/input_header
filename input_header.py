import re

# This class parses Linux's input.h file into an object that is usable
# as if the header file were a class.
# All constants are accessible with <object>.<constant>
# For example:
# >>import input_header
# >>i = input_header.input_header()
# >>print i.BTN_A
# 304

# In general, this class parses the provided file and pulls out all
# lines that begin with #define and contain a Key-Value pair on the
# rest of the line. All values are stored as base-10 integers.
# Can successfully parse lines of the following formats:
# Simple integer:      #define KEY_0			11
# Variable reference:  #define KEY_SCREENLOCK		KEY_COFFEE
# Hexadecimal integer: #define BTN_A			0x130
# Variable Increment:  #define KEY_CNT			(KEY_MAX+1)

# Also provides a search(k) method which returns a list of keys parsed from
# the file that contain the specified string 'k'

'''
Copyright (c) 2010 Daniel Nemec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

class input_header():
  def __init__(self, filename = "/usr/include/linux/input.h"):
    self._inputmap = {}
    try:
      f = open(filename, 'r')
      for line in f:
        m = re.match(r"#define\s+" +
                         r"(?P<key>\w+)\s+" +
                         r"(?P<val>[0-9A-Fa-f]+|" + # Hexadecimal
                         r"[\d]+|" +                # Integer
                         r"\w+|" +                  # Simple substitution
                         r"\(\w+\+1\))$", line)     # Variable Increment
        if m:
          try: # Is it a decimal integer?
            val = int(m.group('val'))
            self._inputmap[m.group('key')] = val
            continue
          except ValueError:
            pass
          try: # Is is a hexidecimal integer?
            val = int(m.group('val'), 16)
            self._inputmap[m.group('key')] = val
            continue
          except ValueError:
            pass
          try: # Is it a substitution?
            s = m.group('val')
            ix = s.find('+')
            if ix < 0:
              if self._inputmap.has_key(s):
                self._inputmap[m.group('key')] = _inputmap[s]
            else:
              sub = s[1:ix]
              eix = s.find(')',ix)
              if self._inputmap.has_key(sub):
                self._inputmap[m.group('key')] = self._inputmap[sub] + int(s[ix+1:eix])
          except:
            pass
              
                
    except IOError:
      raise IOError(1, "Input file %s does not exist." % fil)

  def __getattr__(self, attr):
    try:
        ret = self._inputmap[attr]
    except KeyError:
        raise AttributeError("'%s' object has no attribute '%s'" %
                             (self.__class__.__name__, attr))
    return ret

  def search(self, key):
    ret = []
    for k in self._inputmap.keys():
      if key.lower() in k.lower():
        ret.append(k)
    return ret
