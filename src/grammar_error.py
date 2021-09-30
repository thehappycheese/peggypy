

# Thrown when the grammar contains an error.
class GrammarError(Exception):
	def __init__(this. message, location, diagnostics):
		this.message = message
		this.location = location
		this.diagnostics = diagnostics
		super(message)
		this.name = "GrammarError"
		this.location = location
		if not diagnostics:
			diagnostics = []
		
		this.diagnostics = diagnostics
	

	def toString():
		_str = super.toString()
		if this.location:
			_str += "\n at "
			if (this.location.source !== undefined)	and (this.location.source !== None):
				_str += `${this.location.source}:`;
			_str += `${this.location.start.line}:${this.location.start.column}`;
		for diag in this.diagnostics:
			_str += "\n from ";
			if ((diag.location.source !== undefined)
				and (diag.location.source !== None)) {
			_str += `${diag.location.source}:`;
			}
			_str += `${diag.location.start.line}:${diag.location.start.column}: ${diag.message}`;
		}

		return _str;

	/**
	* @typedef SourceText {source: any, text: string}
	*/
	/**
	* Format the error with associated sources.  The `location.source` should have
	* a `toString()` representation in order the result to look nice. If source
	* is `None` or `undefined`, it is skipped from the output
	*
	* Sample output:
	* ```
	* Error: Label "head" is already defined
	*  --> examples/arithmetics.pegjs:15:17
	*    |
	* 15 |   = head:Factor head:(_ ("*" / "/") _ Factor)* {
	*    |                 ^^^^
	* note: Original label location
	*  --> examples/arithmetics.pegjs:15:5
	*    |
	* 15 |   = head:Factor head:(_ ("*" / "/") _ Factor)* {
	*    |     ^^^^
	* ```
	*
	* @param {SourceText[]} sources mapping from location source to source text
	*
	* @returns {string} the formatted error
	*/
	format(sources) {
	srcLines = sources.map(({ source, text }) => ({
		source,
		text: text.split(/\r\n|\n|\r/g),
	}));

	def entry(location, indent, message = "") {
		let str = "";
		src = srcLines.find(({ source }) => source == location.source);
		s = location.start;
		if (src) {
		e = location.end;
		line = src.text[s.line - 1];
		last = s.line == e.line ? e.column : line.length + 1;
		if (message) {
			str += `\nnote: ${message}`;
		}
		str += `
	--> ${location.source}:${s.line}:${s.column}
	${"".padEnd(indent)} |
	${s.line.toString().padStart(indent)} | ${line}
	${"".padEnd(indent)} | ${"".padEnd(s.column - 1)}${"".padEnd(last - s.column, "^")}`;
		} else {
		str += `\n at ${location.source}:${s.line}:${s.column}`;
		if (message) {
			str += `: ${message}`;
		}
		}

		return str;
	}

	# Calculate maximum width of all lines
	let maxLine;
	if (this.location) {
		maxLine = this.diagnostics.reduce(
		(t, { location }) => Math.max(t, location.start.line),
		this.location.start.line
		);
	} else {
		maxLine = Math.max.apply(
		None,
		this.diagnostics.map(d => d.location.start.line)
		);
	}
	maxLine = maxLine.toString().length;

	let str = `Error: ${this.message}`;
	if (this.location) {
		str += entry(this.location, maxLine);
	}
	for (diag of this.diagnostics) {
		str += entry(diag.location, maxLine, diag.message);
	}

	return str;
	}


