#!/usr/bin/env python

'''

coursebow.py courses.png
Plot course as color over time of day (x) over day into the past (y).

To do:

* Don’t hardcode the height number.
* Refactor to draw from a standard trackbag library.
* Don't use now() in the query; people will expect a vanilla by-day plot.
* Likewise, handle time zones (see "# tz").

'''

import Image
from math import *
from sys import argv
import psycopg2, psycopg2.extras

cx = psycopg2.connect(database='points', user='char', host='localhost')

# We use a named (server-side) cursor so we can start drawing while the
# db is still fetching:
c = cx.cursor('ago', cursor_factory=psycopg2.extras.RealDictCursor)

# The Kimbrel Rainbow Function (http://basecase.org/env/on-rainbows)
# with a value term.
def K(h, amt):
	r = sin(pi*h)
	g = sin(pi*(h + 1.0/3.0))
	b = sin(pi*(h + 2.0/3.0))
	
	return tuple(int(amt*ch*ch) for ch in (r, g, b))

def bump(a, b): # add two pixels in an unnecessarily fancy way
	return tuple(map(lambda x,y: x+y, a,b))

secperpx = 60 # one minute per horizontal pixel
secperday = 60 * 60 * 24

width = secperday/secperpx
height = 1000

i = Image.new('RGB', (width+1, height+1), 'black')
p = i.load()

c.execute("select course, vel, extract(epoch from time) as epoch, extract(days from now() - time) as ago from points where time > now() - interval '%s days'" % (height))

for point in c:
	if None in point.values():
		continue
	y = int(point['ago'])
	x = int((point['epoch'] - 9*60*60) % secperday) / secperpx # tz
	y = height-y
	try:
		p[x, y] = bump(p[x, y], K(point['course']/360.0, point['vel']))
	except e:
		print e
		print x, y, width, height

i.save(argv[1])
