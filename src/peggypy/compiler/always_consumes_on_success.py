
from typing import Any
from .utils_and_types.syntax_tree import (
	Choice,
	Grammar,
	Node,
	Rule_Ref,
	Sequence,
	Literal
)
from .utils_and_types.visitor import Visitor



def consumesTrue(self:Visitor, node:Node, options:dict[str, Any]) -> bool:
	return True


def consumesFalse(self:Visitor, node:Node, options:dict[str, Any]) -> bool:
	return False


def consumesAlternatives_All(self:Visitor, node:Choice, options:dict[str, Any]) -> bool:
	return all(self.visit(alternative, options) for alternative in node.alternatives)


def consumesElements_Any(self:Visitor, node:Sequence, options:dict[str, Any]) -> bool:
	return any(self.visit(element, options) for element in node.elements)


def consumesLiteral(self:Visitor, node:Literal, options:dict[str, Any]):
	return node.value != ""

def consumesRuleRef(self:Visitor, node:Rule_Ref, options:dict[str, Any]) -> bool:
		return self.visit(options["grammar"].findRule(node.name), options)


always_consumes_on_success_visitor = Visitor({
	"choice"       : consumesAlternatives_All,
	"sequence"     : consumesElements_Any,
	"simple_and"   : consumesFalse,
	"simple_not"   : consumesFalse,
	"optional"     : consumesFalse,
	"zero_or_more" : consumesFalse,
	"semantic_and" : consumesFalse,
	"semantic_not" : consumesFalse,
	"rule_ref"     : consumesRuleRef,
	"literal"      : consumesLiteral,
	"class"        : consumesTrue,
	"any"          : consumesTrue,
})


def always_consumes_on_success(grammar:Grammar, node:Node, options:dict[str, Any]) -> bool:
	return always_consumes_on_success_visitor.visit(node, {**options, "grammar":grammar})
