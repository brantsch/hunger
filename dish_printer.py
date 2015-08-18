"""
This module handles printing of dishes of tables to the console.
"""

from collections import OrderedDict

C_BG_GREEN = "\x1b[42m"
C_BG_DEFAULT = "\x1b[49m"

class Table():
	def __init__(self):
		self.widths = OrderedDict([
				("date",0),
				("indications",0),
				("name",0),
				("price_s",0)
				])
		self.dishes = []

	def add(self,dish):
		"""
		Add the given dish to the table.
		"""
		for attr in self.widths:
			self.widths[attr] = max(self.widths[attr],len(str(getattr(dish,attr))))
		self.dishes.append(dish)

	def print(self, highlight=None):
		"""
		Tabulate the list of dishes this Table has accumulated to the console.
		The *highlight* parameter takes a set of flags. If a dish matches them, it is printed with a highlight color.
		"""
		for dish in self.dishes:
			do_highlight = False
			if highlight and highlight.issubset(dish.indications):
				print(C_BG_GREEN,end='') # green background
				do_highlight = True
			for attr in self.widths:
				val = str(getattr(dish,attr))
				width = self.widths[attr]+1
				print(val.ljust(width),end='')
			if do_highlight:
				print(C_BG_DEFAULT,end='')
			print()
