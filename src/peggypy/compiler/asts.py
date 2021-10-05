
from typing import Any
from peggypy.node import Node
from .visitor import Visitor


def findRule(ast, name):
	for rule in ast.rules:
		if rule.name == name:
			return rule
	return None


def indexOfRule(ast, name):
	for index, rule in enumerate(ast.rules):	
		if rule.name == name:
			return index
	return -1


def consumesTrue(self:Visitor, node:Node, *args:Any, **kwargs:Any) -> bool:
	return True


def consumesFalse(self:Visitor, node:Node, *args:Any, **kwargs:Any) -> bool:
	return False


def consumesAlternatives_All(self:Visitor, node:Node, *args:Any, **kwargs:Any):
	return all(self.visit(alternative) for alternative in node.alternatives)


def consumesElements_Any(self:Visitor, node:Node, *args:Any, **kwargs:Any):
	return any(self.visit(element) for element in node.elements)


def consumesLiteral(self:Visitor, node:Node, *args:Any, **kwargs:Any):
	return node.value != ""



def alwaysConsumesOnSuccess(ast, node):

	# TODO: if the visit functions of the Visitor class were designed to accept `ast`
	#   as a parameter then this closure would not be needed
	def consumesRuleRef(self:Visitor, node:Node, *args:Any, **kwargs:Any):
		return self.visit(findRule(ast, node.name))

	consumes = Visitor(
		choice       = consumesAlternatives_All,
		sequence     = consumesElements_Any,
		simple_and   = consumesFalse,
		simple_not   = consumesFalse,
		optional     = consumesFalse,
		zero_or_more = consumesFalse,
		semantic_and = consumesFalse,
		semantic_not = consumesFalse,
		rule_ref     = consumesRuleRef,
		literal      = consumesLiteral,
		_class       = consumesTrue,
		_any         = consumesTrue,
	).visit(node)
