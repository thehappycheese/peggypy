
from __future__ import annotations
from typing import Any, Callable, TypeVar, Union


from .syntax_tree import (
	Action,
	Choice,
	Class,
	Expression,
	Grammar,
	Labeled,
	Node,
	Rule,
	Rule_Ref,
	Sequence,
	Any as st_Any,
	Code,
	Literal
)



# class Node_Visitor(Protocol):
# 	def __call__(_, self:Visitor, node:Node, *args: Any, **kwds: Any) -> Any: ...




def visitNop(self:Visitor, node:Node, options:dict[str, Any]) -> Any:
	pass


def visitExpression(self:Visitor, node:Expression, options:dict[str, Any]) -> Any:
	return self.visit(node.expression, options)


def visitAlternatives(self:Visitor, node:Choice, options:dict[str, Any]) -> Any:
	"""must be overidden if return value is required"""
	for child in node.alternatives:
		self.visit(child, options)

	
def visitElements(self:Visitor, node:Sequence, options:dict[str, Any]) -> Any:
	"""must be overidden if return value is required"""
	for child in node.elements:
		self.visit(child, options)


def grammar(self:Visitor, node:Grammar, options:dict[str, Any]) -> Any:
	if node.top_level_initializer is not None:
		self.visit(node.top_level_initializer, options)

	if node.initializer is not None:
		self.visit(node.initializer, options)

	for rule in node.rules:
		self.visit(rule, options)





class Visitor:
	funcs:dict[str, Node_Visitor]

	def __init__(self, funcs:dict[str, Node_Visitor]):

		ff:Node_Visitor = visitElements
		print(ff)
		default_funcs:dict[str, Node_Visitor] = {
			"grammar":               grammar,
			"top_level_initializer": visitNop,
			"initializer":           visitNop,
			"rule":                  visitExpression,
			"named":                 visitExpression,
			"choice":                visitAlternatives,
			"sequence":              visitElements,
			"action":                visitExpression,
			"labeled":               visitExpression,
			"text":                  visitExpression,
			"simple_and":            visitExpression,
			"simple_not":            visitExpression,
			"optional":              visitExpression,
			"zero_or_more":          visitExpression,
			"one_or_more":           visitExpression,
			"group":                 visitExpression,
			"semantic_and":          visitNop,
			"semantic_not":          visitNop,
			"rule_ref":              visitNop,
			"literal":               visitNop,
			"class":                 visitNop,
			"any":                   visitNop,
		}
		self.funcs = default_funcs | funcs

	def visit(self, node:Any, options:dict[str, Any]) -> Any:
		return self[node.type](self, node, options)

	def __getitem__(self, item: str) -> Node_Visitor:
		if item in self.funcs:
			return self.funcs[item]
		else:
			raise KeyError(f"Visitor class does not have key {item}")

	def __contains__(self, item:str):
		return item in self.funcs


NT = TypeVar("NT",bound="Node")
Node_Visitor_Type = Callable[[Visitor, NT, dict[str, Any]], Any]

Node_Types = Union[Grammar, Choice, Sequence, Expression]
Node_Visitor = Union[
	Node_Visitor_Type[Grammar],
	Node_Visitor_Type[Choice],
	Node_Visitor_Type[Sequence],
	Node_Visitor_Type[Expression],
	Node_Visitor_Type[Code],
	Node_Visitor_Type[Class],
	Node_Visitor_Type[st_Any],
	Node_Visitor_Type[Rule],
	Node_Visitor_Type[Rule_Ref],
	Node_Visitor_Type[Literal],
	Node_Visitor_Type[Action],
	Node_Visitor_Type[Labeled],
]