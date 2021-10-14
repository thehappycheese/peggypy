
from typing import Any, cast
from ..grammar_error import GrammarError
from .utils_and_types.visitor import Visitor
from .utils_and_types.syntax_tree import (
	Choice,
	Class,
	Expression,
	Grammar,
	Node,
	Rule,
	MATCH,
	Rule_Ref,
	Simple_Not,
	Literal
)
from .utils_and_types import syntax_tree


def _sometimesMatch(self:Visitor, node:Node, options:dict[str, Any]) -> MATCH:
	node.match = MATCH.SOMETIMES
	return MATCH.SOMETIMES


def _alwaysMatch(self:Visitor, node:Expression, options:dict[str, Any]) -> MATCH:
	self.visit(node.expression, options)
	node.match = MATCH.ALWAYS
	return node.match


def _inferenceExpression(self:Visitor, node:Expression, options:dict[str, Any]) -> MATCH:
	node.match = self.visit(node.expression, options)
	return node.match


def _choice(self:Visitor, node:Choice, options:dict[str, Any]) -> MATCH:
	length = len(node.alternatives)
	always = 0
	never = 0
	for element in node.alternatives:
		result = self.visit(element, options)
		if result == MATCH.ALWAYS:
			always+=1
		if result == MATCH.NEVER:
			never+=1
	if always == length:
		node.match = MATCH.ALWAYS
	else:
		node.match = MATCH.NEVER if never == length else MATCH.SOMETIMES
	return node.match


def _sequence(self:Visitor, node:syntax_tree.Sequence, options:dict[str, Any]) -> MATCH:
	length = len(node.elements)
	always = 0
	never = 0
	for element in node.elements:
		result = self.visit(element, options)
		if result == MATCH.ALWAYS:
			always+=1
		if result == MATCH.NEVER:
			never+=1
	if always == length:
		node.match = MATCH.ALWAYS
	else:
		node.match = MATCH.NEVER if never > 0 else MATCH.SOMETIMES
	return node.match


def _rule(self:Visitor, node:Rule, options:dict[str, Any]) -> MATCH:
	oldResult:MATCH
	count = 0

	# If property not yet calculated, do that
	if node.match is None:
		node.match = MATCH.SOMETIMES
		while True:
			oldResult = node.match
			node.match = self.visit(node.expression, options)
			# 6 == 3! -- permutations count for all transitions from one match
			# state to another.
			# After 6 iterations the cycle with guarantee begins
			# For example, an input of `start = [] start` will generate the
			# sequence: 0 -> -1 -> -1 (then stop)
			#
			# A more complex grammar theoretically would generate the
			# sequence: 0 -> 1 -> 0 -> -1 -> 0 -> 1 -> ... (then cycle)
			# but there are no examples of such grammars yet (possible, they
			# do not exist at all)

			# istanbul ignore next  This is canary test, shouldn't trigger in real life
			count+=1
			if count > 6:
				raise GrammarError(
					"Infinity cycle detected when trying to evaluate node match result",
					node.location
				)
			if oldResult == node.match:
				break
	return node.match


def _simple_not(self:Visitor, node:Simple_Not, options:dict[str, Any]) -> MATCH:
	node.match = cast(MATCH, self.visit(node.expression, options)).invert()
	return node.match
	

def _rule_ref(self:Visitor, node:Rule_Ref, options:dict[str, Any]) -> MATCH:
	rule = cast(Grammar, options["grammar"]).findRule(node.name)

	node.match = self.visit(rule, options)
	return node.match

def _literal(self:Visitor, node:Literal, options:dict[str, Any]) -> MATCH:
	# Empty literal always match on any input
	node.match = MATCH.ALWAYS if len(node.value) == 0 else MATCH.SOMETIMES
	return node.match

def _class(self:Visitor, node:Class, options:dict[str, Any]) -> MATCH:
	# Empty character class never match on any input
	node.match = MATCH.NEVER if len(node.parts) == 0 else MATCH.SOMETIMES
	return node.match


inference_match_result_visitor = Visitor({
		"rule"         : _rule,
		"named"        : _inferenceExpression,
		"choice"       : _choice,
		"action"       : _inferenceExpression,
		"sequence"     : _sequence,
		"labeled"      : _inferenceExpression,
		"text"         : _inferenceExpression,
		"simple_and"   : _inferenceExpression,
		"simple_not"   : _simple_not,
		"optional"     : _alwaysMatch,
		"zero_or_more" : _alwaysMatch,
		"one_or_more"  : _inferenceExpression,
		"group"        : _inferenceExpression,
		"semantic_and" : _sometimesMatch,
		"semantic_not" : _sometimesMatch,
		"rule_ref"     : _rule_ref,
		"literal"      : _literal,
		"class"        : _class,
		"any"          : _sometimesMatch,
	})


def inference_match_result(grammar:Grammar, options:dict[str, Any]) -> None:
	"""
	Inference match result of the each node. Can be:
	-1: negative result, matching of that node always fails
	 0: neutral result, may be fail, may be match
	 1: positive result, always match
	"""
	inference_match_result_visitor.visit(grammar, {**options, "grammar":grammar})



