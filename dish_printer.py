"""
This module handles printing of dishes of tables to the console.
"""

from collections import OrderedDict

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

	def print(self,colors=True):
		"""
		Tabulate the list of dishes this Table has accumulated to the console.
		By default, colors are enabled.
		"""
		for dish in self.dishes:
			for attr in self.widths:
				val = str(getattr(dish,attr))
				width = self.widths[attr]+1
				print(val.ljust(width),end='')
			print()
