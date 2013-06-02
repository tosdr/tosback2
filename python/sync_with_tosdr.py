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

def missing_from_tosback2(tosdr,tosback2):
    ks=dict(tosback2).keys()
    return [x for x in tosdr if x[0] not in ks]

def tosback2_write(data, direct):
    r=et.Element('sitename',{'name':data[0]})
    for x in data[1]:
        et.SubElement(et.SubElement(et.SubElement(\
            r, "docname", {'name':x[0]}),"url",{'name':x[1]}),"norecurse",{'name':'arbitrary'})

    r.text='\n ';r.tail='\n' #pretty printing
    for x in r:
        x.text='\n   ';
        x.tail=(r[-1]==x and '\n' or '\n ');
        x[0].text='\n     ';
        x[0].tail='\n ';
        x[0][0].tail='\n   '
    et.ElementTree(r).write(os.path.join(direct, data[0]+'.xml'))
