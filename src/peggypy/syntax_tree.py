
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional as Typing_Optional, Union
from enum import Enum

class MATCH(Enum):
	ALWAYS = 1
	SOMETIMES = 0
	NEVER = -1
	def invert(self)->MATCH:
		if self==MATCH.ALWAYS:
			return MATCH.NEVER
		elif self == MATCH.NEVER:
			return MATCH.ALWAYS
		else:
			return MATCH.SOMETIMES


@dataclass(init=True)
class Cursor_Location:
	offset:int
	line:int
	column:int
	@staticmethod
	def lift(arg:dict[str, int]) -> Cursor_Location:
		return Cursor_Location(**arg)


@dataclass
class Location:
	start:Cursor_Location
	end:Cursor_Location
	@staticmethod
	def lift(arg:dict[str,dict[str,int]]) -> Location:
		return Location(**{k:Cursor_Location.lift(v) for k,v in arg.items()})

	
@dataclass(init=False)
class Node:
	type:str
	location:Location
	match:Typing_Optional[MATCH]=field(default=None, init=False)

@dataclass
class Expression(Node):
	expression:Rule_Expression

@dataclass
class Code(Node):
	type:str=field(default="code", init=False)
	code:str
	codeLocation:Location

@dataclass
class Grammar(Node):
	type:str=field(default="grammar", init=False)
	top_level_initializer:Typing_Optional[Code] = None
	initializer:Typing_Optional[Code] = None
	rules:list[Rule] = field(default_factory=list)





@dataclass
class Top_Level_Initializer(Code):
	type:str=field(default="top_level_initializer", init=False)


@dataclass
class Initializer(Code):
	type:str=field(default="initializer", init=False)


@dataclass
class Named(Node):
	type:str=field(default="named", init=False)
	name:str
	expression:Rule_Expression


@dataclass
class Rule(Node):
	type:str=field(default="rule", init=False)
	name:str
	nameLocation:Location
	expression:Union[Rule_Expression, Named]


@dataclass
class Action(Code, Expression):
	type:str=field(default="action", init=False)


@dataclass
class Choice(Node):
	type:str=field(default="choice", init=False)
	alternatives:list[Rule_Expression]


@dataclass
class Sequence(Node):
	type:str=field(default="sequence", init=False)
	elements:list[Rule_Expression]


@dataclass
class Labeled(Expression):
	type:str=field(default="labeled", init=False)
	label:Typing_Optional[str]  # should only be None if pick is true. must always be specified
	labelLocation:Location
	pick:bool=False


@dataclass()
class Text(Expression):
	"""`$rule` signifies that expression should be collected to a single text string instead of an array of tokens"""
	type:str=field(default="text", init=False)


@dataclass()
class Simple_And(Expression):
	"""`&rule`"""
	type:str=field(default="simple_and", init=False)


@dataclass()
class Simple_Not(Expression):
	"""`!rule`"""
	type:str=field(default="simple_and", init=False)


@dataclass()
class Optional(Expression):
	"""`rule?`"""
	type:str=field(default="optional", init=False)


@dataclass()
class Zero_or_More(Expression):
	"""`rule*`"""
	type:str=field(default="zero_or_more", init=False)


@dataclass()
class One_or_More(Expression):
	"""`rule*`"""
	type:str=field(default="one_or_more", init=False)


@dataclass()
class Group(Expression):
	"""`(rules)`"""
	type:str=field(default="group", init=False)


@dataclass()
class Semantic_And(Code):
	"""`&{code}` match succeeds if code returns truthey value"""
	type:str=field(default="semantic_and", init=False)

@dataclass()
class Semantic_Not(Code):
	"""`!{code}` match fails if code returns truthey value"""
	type:str=field(default="semantic_not", init=False)

@dataclass()
class Rule_Ref(Node):
	type:str=field(default="rule_ref", init=False)
	name:str

@dataclass()
class Literal(Node):
	type:str=field(default="literal", init=False)
	value:str
	ignoreCase:bool

@dataclass()
class Class(Node):
	type:str=field(default="class", init=False)
	parts:list[Union[str,list[str]]]
	inverted:bool
	ignoreCase:bool

class Any(Node):
	type:str=field(default="any", init=False)

Rule_Expression = Union[
	Code,
	Choice,
	Action,
	Sequence,
	Labeled,
	Text,
	Simple_And,
	Simple_Not,
	Optional,
	Zero_or_More,
	One_or_More,
	Group,
	Semantic_And,
	Semantic_Not,
	Rule_Ref,
	Literal,
	Class,
	Any
]

# NodeType = Literal[
# 	"top_level_initializer",
# 	"initializer",
# 	"grammar",
# 	"rule",
# 	"named",
# 	"choice",
# 	"action",
# 	"sequence",
# 	"labeled",
# 	"text",
# 	"simple_and",
# 	"simple_not",
# 	"optional",
# 	"zero_or_more",
# 	"one_or_more",
# 	"group",
# 	"semantic_and",
# 	"semantic_not",
# 	"rule_ref",
# 	"literal",
# 	"_class",
# 	"_any",
# ]