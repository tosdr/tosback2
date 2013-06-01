#Released into the Public Domain, via CC-0 if necessary.

import json, os
import xml.etree.ElementTree as et

def tosback2(filename):
    r=et.parse(filename).getroot()
    z=[(x.attrib['name'],x[0].attrib['name'])
                              for x in r]
    z.sort()
    return [(r.attrib['name'],z)]

def tosdr(filename):
    try:
        r=json.load(open(filename))['tosback2']
        z=[(x['name'],x['url']) for x in r.values() if type(x)==dict]
        z.sort()
        return [(r['sitename'],z)]
    except (ValueError), e:
        print filename
        raise e
    except KeyError,e:
        print e, filename

def all_items(d,func,ext):
    return [y[0] for y in map(func, [os.path.join(d,x) for x in os.listdir(d) if x.endswith(ext)]) if y]
