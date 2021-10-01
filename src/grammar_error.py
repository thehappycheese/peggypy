import re


class Cursor_Location:
	offset: int
	line:int
	column:int

@dataclass
class Location:
	source:str
	start: Cursor_Location
	end:Cursor_Location


# Thrown when the grammar contains an error.
class GrammarError(Exception):

	def __init__(self, message, location:Location, diagnostics=None):
		self.message = message
		self.location = location
		self.diagnostics = diagnostics
		super(message)
		self.name = "GrammarError"
		self.location = location
		if not diagnostics:
			diagnostics = []
		
		self.diagnostics = diagnostics
	

	def toString(self):
		_str = super.toString()
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
	def _entry(srcLines, location, indent, message = ""):
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
	
	# TODO: shoudl this be the __str__ or __repl__ function instead?
	def format(self, sources):
		srcLines = [
			{
				"source":source_text["source"],
				"text":re.split("(\r\n)|\n|\r", source_text["text"])
			}
			for source_text in sources
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
			_str += GrammarError.entry(srcLines, self.location, maxLine)

		for diag in self.diagnostics:
			_str += GrammarError.entry(srcLines, diag.location, maxLine, diag.message)

		return _str
	


