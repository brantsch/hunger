import sys
from mensa.parser import parse
from mensa.util import fetch
import dish_printer
import argparse
import os
import pickle
from datetime import date
import re

menu = None
cache_path = os.environ['HOME']+"/.cache/hunger/"
cache_file = cache_path + "cache"

def update():
	os.makedirs(cache_path,exist_ok=True)
	global menu
	menu = parse(fetch())
	with open(cache_file,'wb') as cache:
		pickle.dump(menu,cache)
	print("hunger successfully updated its cache")

def drop_cache():
	os.remove(cache_file)

def load():
	global menu
	try:
		with open(cache_file,'rb') as cache:
			menu = pickle.load(cache)
	except FileNotFoundError:
		pass
	except:
		raise

def list_all(highlight=None):
	dates = sorted(menu.dates())
	list_for_dates(*dates,highlight=highlight)

def list_today(highlight=None):
	list_for_dates(date.today(),highlight=highlight)

def list_for_dates(*dates,allow_update=True,highlight=None):
	def __check_date(thedate):
		weekday = thedate.weekday()
		if weekday >= 5:
			print("Error: given date is on a weekend. Please try {0} or {1} instead.".format(\
				date.fromordinal(thedate.toordinal()+(7-weekday)),\
				date.fromordinal(thedate.toordinal()-(weekday-4))\
			),file=sys.stderr)
			exit(1)
		else:
			return thedate in menu
	if menu and all(map(__check_date,dates)):
		table = dish_printer.Table()
		for thedate in dates:
			for dish in menu[thedate]:
				table.add(dish)
		table.print(highlight)
	elif allow_update:
		print("No data for date(s) {0}. Will now update cache and try again.".format(", ".join(map(str,dates))), file=sys.stderr)
		update()
		list_for_dates(*dates,allow_update=False,highlight=highlight)
	else:
		print("No data available for given date. Giving up.",file=sys.stderr)
		exit(1)

def main(argv):
	parser = argparse.ArgumentParser("List contents of canteen menu of the THI mensa.")
	parser.add_argument('--force-update','-u',action='store_true',help="Force update of the cache and exit.")
	parser.add_argument('--drop-cache',action='store_true',help="Delete cache file.")
	parser.add_argument('--list-all',action='store_true',help="List all available dishes.")
	parser.add_argument('--date','-d',type=str,help="Show menu for date given as YYYY-MM-DD")
	parser.add_argument('--highlight', '-H', type=set, help="List of flags (e.g. V for 'vegetarian') to highlight in output")
	args = parser.parse_args(argv)
	if args.drop_cache:
		drop_cache()
		exit()
	if args.force_update:
		update()
		exit()
	load()
	if args.list_all:
		list_all(args.highlight)
	elif args.date:
		thedate = None
		match = re.match("\s*\+(\d+)\s*",args.date)
		if match:
			date_offset = int(match.group(0))
			thedate = date.fromordinal(date.today().toordinal()+date_offset)
		if not thedate:
			try:
				year, month, day = map(lambda x: int(x),args.date.split('-'))
				thedate = date(year, month, day)
			except ValueError:	
				print("Invalid date!",file=sys.stderr)
				exit(1)
		list_for_dates(thedate, highlight=args.highlight)
	else:
		list_today(args.highlight)
