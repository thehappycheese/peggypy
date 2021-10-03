from dataclasses import dataclass
from typing import Any, Union
import re
from .diagnostic import Diagnostic
from .location import Location

@dataclass
class Source_Line:
	source:Any # TODO: What type should this be?
	text:list[str]

# Thrown when the grammar contains an error.
class GrammarError(Exception):

	message:str
	location:Location
	diagnostics:list[Diagnostic]

	def __init__(self, message:str, location:Location, diagnostics:Union[list[Diagnostic], None]=None):
		super().__init__(message)
		self.message = message
		self.location = location
		self.diagnostics = diagnostics if diagnostics is not None else []
		self.name = "GrammarError"
	

	def toString(self)->str:
		_str = super().__str__()
		if self.location:
			_str += "\n at "
			if self.location.source is not None:
				_str += f"{self.location.source}:"
			_str += f"{self.location.start.line}:{self.location.start.column}"
		for diag in self.diagnostics:
			_str += "\n from "
			if diag.location.source != None and diag.location.source != None:
				_str += f"{diag.location.source}:"
			_str += f"{diag.location.start.line}:{diag.location.start.column}: {diag.message}"
		return _str

	@staticmethod
	def _entry(srcLines:list[Source_Line], location:Location, indent:int, message:str = ""):
		_str = ""
		src = None

		for line in srcLines:
			line.source == location.source

		s = location.start

		if src:
			e = location.end
			line = src.text[s.line - 1]
			last =  e.column if s.line == e.line else line.length + 1
			if message:
				_str += f"\nnote: {message}"
			_str += (
				f"--> {location.source}:{s.line}:{s.column}" +
				f"{' ' * indent} |" +
				f"{_str(s.line):<{indent}} | {line}" +
				f"{' ' * indent} | {' ' * (s.column - 1)}{'^' * (last - s.column)}"
			)
		else:
			_str += f"\n at {location.source}:{s.line}:{s.column}"
			if message:
				_str += f": {message}"
		return _str

	# 
	# @typedef SourceText {source: any, text: string}
	# 
	# Format the error with associated sources.  The `location.source` should have
	# a `toString()` representation in order the result to look nice. If source
	# is `None` or `undefined`, it is skipped from the output
	# 	# Sample output:
	# ```
	# Error: Label "head" is already defined
	#  --> examples/arithmetics.pegjs:15:17
	#    |
	# 15 |   = head:Factor head:(_ ("*" / "/") _ Factor)* {
	#    |                 ^^^^
	# note: Original label location
	#  --> examples/arithmetics.pegjs:15:5
	#    |
	# 15 |   = head:Factor head:(_ ("*" / "/") _ Factor)* {
	#    |     ^^^^
	# ```
	# 	# @param {SourceText[]} sources mapping from location source to source text
	# 	# @returns {string} the formatted error
	
	# TODO: should this be the __str__ or __repl__ function instead?
	def format(self, sources:list[Location]):
		srcLines = [
			Source_Line(
				source = location.source,
				text   = re.split("(\r\n)|\n|\r", location["text"])
			)
			for location in sources
		]

		# Calculate maximum width of all lines
		# TODO: the original code was special with a capital R. The origonal comment above makes no sense.
		# looks like it finds the width of the last line number
		# not the line itself.
		
		maxLine = max(
			self.location.start.line if self.location is not None else -1,
			*(item["location"]["start"]["line"] for item in self.diagnostics)
		)
		maxLine = len(str(maxLine))

		_str = f"Error: {self.message}"
		if self.location:
			_str += GrammarError._entry(srcLines, self.location, maxLine)

		for diag in self.diagnostics:
			_str += GrammarError._entry(srcLines, diag.location, maxLine, diag.message)

		return _str
	


