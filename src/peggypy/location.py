from dataclasses import dataclass


@dataclass
class Cursor_Location:
	offset: int
	line:int
	column:int


@dataclass
class Location:
	source:str
	start: Cursor_Location
	end:Cursor_Location