
import re

def extract_group_and_escape_char(ch:re.Match[str]) -> str:
    num = ord(ch.group())
    if num<=0xFF:
        return f"\\x{num:0>2X}"
    if num<=0xFFFF:
        return f"\\u{num:0>4X}"
    return f"\\U{num:0>8X}"
    


def stringEscape(s:str) -> str:
    # ECMA-262, 5th ed., 7.8.4: All characters may appear literally in a string
    # literal except for the closing quote character, backslash, carriage
    # return, line separator, paragraph separator, and line feed. Any character
    # may appear in the form of an escape sequence.
    #
    # For portability, we also escape all control and non-ASCII characters.
    
    s
    s = re.sub("\\",                         "\\\\",                        s)  # Backslash
    s = re.sub("\"",                         "\\\"",                        s)  # Closing double quote
    s = re.sub("\0",                         "\\0",                         s)  # None
    s = re.sub("\x08",                       "\\b",                         s)  # Backspace
    s = re.sub("\t",                         "\\t",                         s)  # Horizontal tab
    s = re.sub("\n",                         "\\n",                         s)  # Line feed
    s = re.sub("\v",                         "\\v",                         s)  # Vertical tab
    s = re.sub("\f",                         "\\f",                         s)  # Form feed
    s = re.sub("\r",                         "\\r",                         s)  # Carriage return
    s = re.sub("[\x00-\x1F\x7F-\UFFFFFFFF]", extract_group_and_escape_char, s)
        
    return s


def regexpClassEscape(s:str) -> str:
    # Based on ECMA-262, 5th ed., 7.8.5 & 15.10.1.
    #
    # For portability, we also escape all control and non-ASCII characters.
    
    # TODO: I don't think python recognizes forward slash as special in regex pattern strings?
    # TODO: this whole thing needs a good looking at for python purposes

    s = re.sub("\\",                         "\\\\",                        s)  # Backslash
    s = re.sub("\\/",                        "\\/",                         s)  # Closing slash
    s = re.sub("]",                          "\\]",                         s)  # Closing bracket 
    s = re.sub("\\^",                        "\\^",                         s)  # Caret
    s = re.sub("-",                          "\\-",                         s)  # Dash
    s = re.sub("\0",                         "\\0",                         s)  # None
    s = re.sub("\x08",                       "\\b",                         s)  # Backspace
    s = re.sub("\t",                         "\\t",                         s)  # Horizontal tab
    s = re.sub("\n",                         "\\n",                         s)  # Line feed
    s = re.sub("\v",                         "\\v",                         s)  # Vertical tab
    s = re.sub("\f",                         "\\f",                         s)  # Form feed
    s = re.sub("\r",                         "\\r",                         s)  # Carriage return
    s = re.sub("[\x00-\x1F\x7F-\UFFFFFFFF]", extract_group_and_escape_char, s)
    return s
        
        