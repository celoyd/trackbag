since () {
	psql -d points -At -F ', ' -c "select $2 from points where time > now() - interval '$1' $3"
}
