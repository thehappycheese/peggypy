
from typing import Any
from .always_consumes_on_success import always_consumes_on_success
from .utils_and_types.syntax_tree import Expression, Grammar
from .utils_and_types.visitor import Visitor
from ..grammar_error import GrammarError

def reportInfiniteRepetition(grammar:Grammar, options:dict[str, Any]):

	def zero_or_more(self:Visitor, node:Expression, options:dict[str, Any]):
		if not always_consumes_on_success(grammar, node.expression, options):
			raise GrammarError(
				"Parser would loop infinitely on some inputs: Zero or more repetitions (`*`) of a pattern that may not consume any input",
				node.location
			)

	def one_or_more(self:Visitor, node:Expression, options:dict[str, Any]):
		if not always_consumes_on_success(grammar, node.expression, options):
			raise GrammarError(
				"Parser would loop infinitely on some inputs: One or more repetitions (`+`) of a pattern that may not consume any input",
				node.location
			)

	Visitor({
		"zero_or_more" : zero_or_more,
		"one_or_more"  : one_or_more
	}).visit(grammar, options)
