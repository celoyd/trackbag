#!/usr/bin/env python

'''

plot position with lines

VERY ugly code, will document later

To do (incomplete):

* use proper cosines for latgrain/longrain
* off by ones
* tunable distance filtering
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

longrain = 1/50000.0
latgrain = longrain/1.5 #longrain/sqrt(2)

def K(h, a):
	factor = 255 * a
	
	r = sin(pi*h)
	g = sin(pi*(h + 1.0/3.0))
	b = sin(pi*(h + 2.0/3.0))
	
	return tuple(int(factor*ch*ch) for ch in (r, g, b))

notch = 8

def increment(thing, plus):
	return (
		thing[0] - plus[0],
		thing[1] - plus[1],
		thing[2] - plus[2])

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
	
	while True: #x0 != x1 and y0 != y1:
		if x0 == x1 and y0 == y1: break
		p[x0, y0] = increment(p[x0, y0], c)
		#if x0 == x1 and y0 == y1: break
		e2 = 2*err
		if e2 > -dy:
			err -= dy
			x0 = x0 + sx
		if e2 < dx:
			err = err + dx
			y0 = y0 + sy

width = int(round((lonrange[1]-lonrange[0]) * 1/longrain)) + 2
height = int(round((latrange[1]-latrange[0]) * 1/latgrain)) + 2

i = Image.new('RGB', (width, height), (255,255,255))
p = i.load()

cx = connect(database='points', user='char', host='localhost')
c = cx.cursor('twinkles')

def scale(xy):
	

c.execute("select lat, lon, extract(epoch from time), pdop from points where lat > %s and lat < %s and lon > %s and lon < %s" % (latrange[0], latrange[1], lonrange[0], lonrange[1]))

#  and extract(dow from time) = 4

t = 0

lastpoint = []

for point in c:
#	if None in point:
#		point = (point[0], point[1], point[2], 2)
	if None in point:
		continue
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
		print point
	
	color = K(((182 + point[2])/365.0), 1.0/point[3])
	
	try:
		line([lastpoint['x'], [x, y], p, color)
	except:
		pass
	
	lastpoint = [x, y]
		
	t += 1

#i = invert(i)
i.save(argv[1])

print(t)