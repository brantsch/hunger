#!/usr/bin/env python3
from mensa.parser import parse
from mensa.util import fetch
import argparse
import os
import pickle
from datetime import date

description = """
List contents of canteen menu of the THI mensa.
"""

dishes = None
cache_path = os.environ['HOME']+"/.cache/hunger/"
cache_file = cache_path + "cache"

def update():
	os.makedirs(cache_path,exist_ok=True)
	global dishes
	dishes = parse(fetch())
	with open(cache_file,'wb') as cache:
		pickle.dump(dishes,cache)
	print("hunger successfully updated its cache")

def drop_cache():
	os.remove(cache_file)

def load():
	global dishes
	try:
		with open(cache_file,'rb') as cache:
			dishes = pickle.load(cache)
	except FileNotFoundError:
		#update()
		pass
	except:
		raise

def list_all():
	for dish in dishes:
		print(dish)

def list_today():
	today = date.today()
	global dishes
	need_update = True
	if dishes: 
		for dish in dishes:
			if dish.date == today:
				need_update = False
				print(dish)
	if need_update:
		print("No entry found for today. Will now update cache. Try again after cache is updated.")
		update()

def main():
	parser = argparse.ArgumentParser(description)
	parser.add_argument('--force-update','-u',action='store_true')
	parser.add_argument('--drop-cache',action='store_true')
	parser.add_argument('--list-all',action='store_true')
	args = parser.parse_args()
	if args.drop_cache:
		drop_cache()
		exit()
	if args.force_update:
		update()
	load()
	if args.list_all:
		list_all()
	else:
		list_today()
	
if __name__ == "__main__":
	main()
