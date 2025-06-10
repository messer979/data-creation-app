import sqlite3
import arrow

file_suffix = arrow.now().format('YYYY_MM_DD_HHmm')


def get_connection(file_name):
	return sqlite3.connect(file_name + file_suffix +".sqlite")


