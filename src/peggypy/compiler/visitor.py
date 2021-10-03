
from __future__ import annotations
from typing import Any, Protocol
from dataclasses import dataclass

from peggypy.node import Node


# TODO: this should be the future node visitor class:
# class Node_Visitor(Protocol):
# 	def __call__(self, node, root_ast, *args: Any, **kwds: Any) -> Any: ...


class Node_Visitor(Protocol):
	def __call__(node: Any, *args: Any, **kwargs:Any) -> Any: ...


def visitNop(self:Visitor, node:Node, *args:Any, **kwargs:Any) -> None:
	pass


def visitExpression(self:Visitor, node:Node, *args:Any, **kwargs:Any) -> None:
	return self.visit(node.expression, *args, **kwargs)


def visitAlternatives(self:Visitor, node:Node, *args:Any, **kwargs:Any):
	for child in node.alternatives:
		self.visit(child, *args, **kwargs)

	
def visitElements(self:Visitor, node:Node, *args:Any, **kwargs:Any):
	for child in node.elements:
		self.visit(child, *args, **kwargs)


def grammar(self:Visitor, node:Node, *args:Any, **kwargs:Any):
	if node.topLevelInitializer is not None:
		self.visit(node.topLevelInitializer, *args, **kwargs)

	if node.initializer is not None:
		self.visit(node.initializer, *args, **kwargs)

	for rule in node.rules:
		self.visit(rule, *args, **kwargs)


@dataclass
class Visitor:
	top_level_initializer: Node_Visitor = visitNop  # used?
	initializer: Node_Visitor           = visitNop  # used?
	grammar: Node_Visitor               = grammar
	rule: Node_Visitor                  = visitExpression
	named: Node_Visitor                 = visitExpression
	choice: Node_Visitor                = visitAlternatives
	action: Node_Visitor                = visitExpression
	sequence: Node_Visitor              = visitElements
	labeled: Node_Visitor               = visitExpression
	text: Node_Visitor                  = visitExpression
	simple_and: Node_Visitor            = visitExpression
	simple_not: Node_Visitor            = visitExpression
	optional: Node_Visitor              = visitExpression
	zero_or_more: Node_Visitor          = visitExpression
	one_or_more: Node_Visitor           = visitExpression
	group: Node_Visitor                 = visitExpression
	semantic_and: Node_Visitor          = visitNop
	semantic_not: Node_Visitor          = visitNop
	rule_ref: Node_Visitor              = visitNop
	literal: Node_Visitor               = visitNop
	_class: Node_Visitor                = visitNop  # TODO: original variable name was `class`
	_any: Node_Visitor                  = visitNop  # TODO: original variable name was `any`

	def visit(self, node:list[Node], *args:Any, **kwargs:Any):
		# TODO: modify all calls to visit, and all of this classes members, such that they accept self, node, root_ast, *args, **kwargs
		if node.type not in self:
			raise KeyError(f"Could not visit {node.type=}")
		return self[node.type](node, *args, **kwargs)

	def __getitem__(self, item: str) -> Node_Visitor:
		if item in self.__dict__[item]:
			return self.__dict__[item]
		else:
			raise KeyError(f"Visitor class does not have key {item}")

	def __contains__(self, item:str):
		raise Exception("is this __contains__ needed?")
		return item in self.__dict__