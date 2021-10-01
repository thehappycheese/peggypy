

def hex(ch):
	return ch.charCodeAt(0).toString(16).toUpperCase()


def stringEscape(s):
	# ECMA-262, 5th ed., 7.8.4: All characters may appear literally in a string
	# literal except for the closing quote character, backslash, carriage
	# return, line separator, paragraph separator, and line feed. Any character
	# may appear in the form of an escape sequence.
	#
	# For portability, we also escape all control and non-ASCII characters.
	return (
		s
		.replace("\\",   "\\\\")   # Backslash
		.replace("\"",    "\\\"")   # Closing double quote
		.replace("\0",   "\\0")    # None
		.replace("\x08", "\\b")    # Backspace
		.replace("\t",   "\\t")    # Horizontal tab
		.replace("\n",   "\\n")    # Line feed
		.replace("\v",   "\\v")    # Vertical tab
		.replace("\f",   "\\f")    # Form feed
		.replace("\r",   "\\r")    # Carriage return
		.replace("[\x00-\x0F]",          ch => "\\x0" + hex(ch))
		.replace("[\x10-\x1F\x7F-\xFF]", ch => "\\x"  + hex(ch))
		.replace("[\u0100-\u0FFF]",      ch => "\\u0" + hex(ch))
		.replace("[\u1000-\uFFFF]",      ch => "\\u"  + hex(ch))
		)


def regexpClassEscape(s):
	# Based on ECMA-262, 5th ed., 7.8.5 & 15.10.1.
	#
	# For portability, we also escape all control and non-ASCII characters.
	return (s
		.replace("\\",   "\\\\")   # Backslash
		.replace("\/",   "\\/")    # Closing slash
		.replace("]",    "\\]")    # Closing bracket
		.replace("\^",   "\\^")    # Caret
		.replace("-",    "\\-")    # Dash
		.replace("\0",   "\\0")    # None
		.replace("\x08", "\\b")    # Backspace
		.replace("\t",   "\\t")    # Horizontal tab
		.replace("\n",   "\\n")    # Line feed
		.replace("\v",   "\\v")    # Vertical tab
		.replace("\f",   "\\f")    # Form feed
		.replace("\r",   "\\r")    # Carriage return
		.replace("[\x00-\x0F]",          ch => "\\x0" + hex(ch))
		.replace("[\x10-\x1F\x7F-\xFF]", ch => "\\x"  + hex(ch))
		.replace("[\u0100-\u0FFF]",      ch => "\\u0" + hex(ch))
		.replace("[\u1000-\uFFFF]",      ch => "\\u"  + hex(ch))
		)