
from ...grammar_error import GrammarError
from .. import asts
from ..visitor import Visitor

def reportInfiniteRepetition(ast, *args):

	def zero_or_more(self, node, *args):
		if not asts.alwaysConsumesOnSuccess(ast, node.expression):
			raise GrammarError(
				"Parser would loop infinitely on some inputs: Zero or more repetitions (`*`) of a pattern that may not consume any input",
				node.location
			)

	def one_or_more(self, node, *args):
		if not asts.alwaysConsumesOnSuccess(ast, node.expression):
			raise GrammarError(
				"Parser would loop infinitely on some inputs: One or more repetitions (`+`) of a pattern that may not consume any input",
				node.location
			)

	Visitor(
		zero_or_more=zero_or_more,
		one_or_more=one_or_more
	).visit(ast)
