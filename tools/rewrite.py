'''
Created on Jan 29, 2012
Import a JSON dump and convert it to a CSV column based file
@author: Joel Haasnoot
'''
import csv, codecs, cStringIO
import simplejson as json


class DictUnicodeWriter(object):
    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()

f = codecs.open('cxx', encoding='utf-8', mode='r') 
content = f.read()
f.close()
content = "{"+content.split('>{')[1].split('}<')[0]+"}"
j = json.loads(content, encoding='utf-8', parse_int=str)

import csv
f = open('cxx.csv', mode='wb')
keys = j['HALTELIST'].keys()
cxxWriter = DictUnicodeWriter(f, map(unicode.lower, keys))
cxxWriter.writeheader();
for i in range(1, len(j['HALTELIST']['ID'])):
    row = {}
    for key in keys:
        if j['HALTELIST'][key][i] == True:
            j['HALTELIST'][key][i] = "1"
        elif j['HALTELIST'][key][i] == False:
            j['HALTELIST'][key][i] = "0"
        elif j['HALTELIST'][key][i] is None:
            j['HALTELIST'][key][i] = ''
        row[key.lower()] = j['HALTELIST'][key][i]
    cxxWriter.writerow(row)
f.close()