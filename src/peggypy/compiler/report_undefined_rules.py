from typing import Any

from .utils_and_types.syntax_tree import Grammar, Rule_Ref
from .utils_and_types.visitor import Visitor
from ..grammar_error import GrammarError


def rule_ref (self:Visitor, node:Rule_Ref, options:dict[str,Any]):
	if options["grammar"].findRule(node.name) is None:
		raise  GrammarError(
			f'Rule "{node.name=}" is not defined',
			node.location
		)


report_undefined_rules_visitor = Visitor({
	"rule_ref":rule_ref
})


def report_undefined_rules(grammar:Grammar, options:dict[str, Any]):
	"""Check that all referenced rules exist."""
	report_undefined_rules_visitor.visit(grammar, {**options, "grammar":grammar})


