#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

plot position with lines

A slightly different version of this made http://basecase.org/env/GPS-seasons

VERY ugly code, will document later

To do (incomplete):

* off by ones
* dict cursor
* etc., etc., etc.
* less hard-coding

'''

import Image
from math import *
from psycopg2 import connect
from sys import argv

latrange = [45.45, 45.65]
lonrange = [-122.75, -122.5]

'''
We do a simple rectangular projection that's equidistant along the center
latitude. This is basically correct in terms of distance, area, and angle
at the scale of a city or small region. If you want something fancier, use
a real GIS package winking emoticon.
'''

# Degrees of latitude per pixel. 1 degree is about 111 km or 69 mi.
longrain = 1/10000.0

# Derive the degrees of longitude per pixel. Assume a spherical earth.
latgrain = longrain * cos(radians(
	latrange[0] + (latrange[1] - latrange[0])/2.0
))

def K(h, a):
	factor = 255 * a
	r = sin(pi*h)
	g = sin(pi*(h + 1.0/3.0))
	b = sin(pi*(h + 2.0/3.0))
	return tuple(int(factor*ch*ch) for ch in (r, g, b))

# This bump function actually subtracts, because we start from white.
def bump(a, b): #               ↓ there
	return tuple(map(lambda x,y: x-y, a,b))

def line(f, t, p, c): # Bresenham's, from Wikipedia
	x0, x1 = f[0], t[0]
	y0, y1 = f[1], t[1]
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	
	err = dx-dy
	
	if x0 < x1: sx = 1
	else: sx = -1
	
	if y0 < y1: sy = 1
	else: sy = -1
	
	while True: # Looping on True and breaking? Ick. Why?
		if x0 == x1 and y0 == y1: break
		p[x0, y0] = bump(p[x0, y0], c)
		e2 = 2*err
		if e2 > -dy:
			err -= dy
			x0 = x0 + sx
		if e2 < dx:
			err = err + dx
			y0 = y0 + sy

width = int(round((lonrange[1]-lonrange[0]) * 1/longrain)) + 1
height = int(round((latrange[1]-latrange[0]) * 1/latgrain)) + 1

i = Image.new('RGB', (width, height), (255,255,255))
p = i.load()

cx = connect(database='points', user='char', host='localhost')
c = cx.cursor('twinkles')

c.execute("select lat, lon, extract(epoch from time), pdop from points where lat > %s and lat < %s and lon > %s and lon < %s and time > now() - interval '2 months' order by time" % (latrange[0], latrange[1], lonrange[0], lonrange[1]))

# and extract(dow from time) = 4

t = 0

lastpoint = []

for point in c:
	if None in point: continue
	
	y = int((point[0]-latrange[0]) * 1/latgrain)
	x = int((point[1]-lonrange[0]) * 1/longrain)

	y = height-y

	if lastpoint == []:
		lastpoint = point
	try:
		if (point[2] - lastpoint[2]) > 3:
	#if abs(x - lastpoint[0]) > 500 or abs(y - lastpoint[1]) > 500:
			lastpoint = point
	except:
		pass
		#print point
	
	color = K(((182 + point[2])/365.0), 1.0/point[3])
	
	try:
		line(lastpoint, [x, y], p, color)
	except:
		pass
	
	lastpoint = [x, y]
		
	t += 1

i.save(argv[1])

#print(t)