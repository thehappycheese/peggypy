
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Union
from enum import Enum

from .location import Location

NodeType = Literal[
	"top_level_initializer",
	"initializer",
	"grammar",
	"rule",
	"named",
	"choice",
	"action",
	"sequence",
	"labeled",
	"text",
	"simple_and",
	"simple_not",
	"optional",
	"zero_or_more",
	"one_or_more",
	"group",
	"semantic_and",
	"semantic_not",
	"rule_ref",
	"literal",
	"_class",
	"_any",
]

# TODO: rename refactor
class Node_MATCH(Enum):
	ALWAYS_MATCH = 1
	SOMETIMES_MATCH = 0
	NEVER_MATCH = -1


@dataclass
class Node:
	name: str
	value: Union[str,list[Any]]  # TODO: is this a string or a list? Seems to be a string if its a literal...
	type: NodeType
	expression: Node        # TODO: this could be the wrong type?
	location: Location
	literals: Any
	expectations: Any
	functions: Any
	bytecode: Any
	code:str
	alternatives:list[Node]
	label: str              # TODO: type unknown? 
	pick: Any               # TODO: type unknown? 
	ignoreCase: bool        # TODO: type unknown? is this a function?
	parts: Any              # TODO: type unknown? is this a function?
	inverted: Any           # TODO: type unknown? is this a function?
	match:Optional[Node_MATCH]         = None
	topLevelInitializer: Optional[str] = None
	initializer: Optional[str]         = None
	rules: list[Node]                  = field(default_factory=list)
	elements: Optional[list[Node]]     = None
	attributes: Optional[list[Node]]   = None

	
	
	