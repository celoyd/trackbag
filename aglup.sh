aglup () {
	for N in /Volumes/GPS\ TRACKER/GPSFILES/*.log
	do
		cp $N ~/Desktop/tracks/
		T=$(mktemp -t gpx) 
		gpsbabel -i nmea -o gpx $N $T
		B=$(mktemp -t gps) 
		~/Desktop/tracks/trackstuff/agl3080dump.py $T >> $B
		psql -d points -c "\copy points from '$B' with delimiter ','" && rm $T $B && rm $N
	done
}
