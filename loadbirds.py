
from lxml import etree

from gridfs import GridFS
from pymongo import Connection

db = Connection().perches
fs = GridFS(db)
birds = db.birds

xml = open('ioc-names-2.4.xml').read()
root = etree.fromstring(xml)
meta, iocl = [el for el in root.iterchildren()]
metadata = [{x.tag : x.text} for x in meta.iter()]
orders = [el for el in iocl.iterchildren()]

## TODO: strip whitespace
## TODO: split *regions??

for o in orders:
    odata = {}
    odata['code'] = o.find('code').text
    odata['order'] = o.find('latin_name').text.strip()
    odata['note'] = o.find('note').text.strip()
    familia = o.findall('family')
    for f in familia:
        fdata = {}
        fdata['code'] = f.find('code').text
        fdata['latin_name'] = f.find('latin_name').text.strip()
        fdata['english_name'] = f.find('english_name').text.strip()
        fdata['note'] = f.find('note').text.strip()
        genuses = f.findall('genus')
        for g in genuses:
            gdata = {}
            gdata['code'] = g.find('code').text 
            gdata['latin_name'] = g.find('latin_name').text.strip()
            gdata['note'] = g.find('note').text.strip()
            species = g.findall('species')
            for s in species:
                sdata = {}
                sdata['code'] = s.find('code').text 
                sdata['note'] = s.find('note').text.strip()
                sdata['latin_name'] = s.find('latin_name').text.strip()
                sdata['english_name'] = s.find('english_name').text.strip()
                br = [x.strip() for x in s.find('breeding_regions').text.split(',')]
                if not isinstance(br, list):
                    if br is None:
                        br = u''
                    br = [br,]
                sdata['breeding_regions'] = br
                sr = s.find('breeding_subregions').text
                if sr is None:
                    sr = u''
                srl = sr.split(',')
                ## TODO: split on , and & and make sure except isn't lost on Foo except bar & baz
                sr = [sr,]
                sdata['breeding_subregions'] = sr
                sdata['nonbreeding_regions'] = s.find('nonbreeding_regions').text
                sdata['order'] = odata
                sdata['genus'] = gdata
                sdata['family'] = fdata
                birds.insert(sdata)
