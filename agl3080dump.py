#!/usr/bin/env python2.7

from lxml import etree
from sys import argv
from string import lstrip, replace
from sys import exit

def tag(t):
	return "{http://www.topografix.com/GPX/1/0}" + t

t = etree.parse(argv[1])

pts = t.findall('//' + tag('trkpt'))

elements = ['time', 'lat', 'lon', 'ele', 'speed', 'trust', 'source', 'fix', 'hdop', 'vdop', 'pdop', 'sat', 'course']

for pt in pts:	
	data = {}
	for datum in elements:
		data[datum] = '\N'

	data['time'] = "'" + replace(lstrip(pt.findtext(tag('time'))), 'T', ' ') + "'"

	data['lat'] = lstrip(pt.get('lat'))
	data['lon'] = lstrip(pt.get('lon'))

	for datum in elements:
		if datum not in ['time', 'lat', 'lon', 'trust', 'source']:
			try: data[datum] = lstrip(pt.findtext(tag(datum)))
			except: pass
	
	#data['fix'] = "'" + data['fix'] + "'"
	
	try:
		data['speed'] = str(float(data['speed']))
	except: pass

	try:
		if data['sat'] == 'NULL':
			data['sat'] = '0'
	except: pass

	data['trust'] = 't'
	data['source'] = 'AGL3080'
	
	out = []
	for e in elements:
		out.append(data[e])
	print ','.join(out)
