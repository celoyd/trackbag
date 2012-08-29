trackbag
========

Ad-hoc tools for taking NMEA GPS data off an Amod AGL 3080 and storing it in postgres.

Requires gpsbabel (http://www.gpsbabel.org or your preferred package library) and the python lxml library.

This is really ad-hoc code. It evolved from other code and does some pointless things, and it won't work out of the box for you, but I hope it might be a useful starting point for setting up your own system. Improvements are, of course, welcome.


Overview
========

I plug in my AGL 3080 and it mounts as an external drive. I run the aglup tool (which I actually have as a shell alias, not a script) and it does this for each raw NMEA log:

1. Copies the log to my hard drive.

2. Uses gpsbabel to create a GPX version of the NMEA.

3. Uses agl3080dump.py to turn the GPX into a CSV.

4. Has postgres read the CSV into a table (described in schema.sql) and, if that worked, deletes the file off the logger.

The most common error I get at this point is duplicate violation, which happens if the logger wrote multiple sessions to one file.

I query the database with the since.sh script (again, actually a shell alias), which writes CSV. That looks like this:

$ since '1 week' 'lon, lat' > points

That's easy to plot with gnuplot, processing, or whatever you like. (I may upload some of my python plotting scripts eventually.)


To do
=====

* Consider PostGIS.

* Figure out why I didn't have gpsbabel write CSV instead of going through GPX.

* Think about storing skyview.

* Handle duplicate violation better.

* Clean up & share plotting scripts.
