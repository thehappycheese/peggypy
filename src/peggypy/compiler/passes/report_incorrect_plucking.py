
from ...diagnostic import Diagnostic
from ...grammar_error import GrammarError
from ..visitor import Visitor

#
# Compiler pass to ensure the following are enforced:
#
#   - plucking can not be done with an action block
#

def action(self, node, *args):
	self.visit(node.expression, node)

def labeled(self, node, action):
	if node.pick:
		if action:
			raise GrammarError(
				"\"@\" cannot be used with an action block",
				node.labelLocation,
				[Diagnostic(
					message = "Action block location",
					location = action.codeLocation,
				)]
			)

	self.visit(node.expression)

def reportIncorrectPlucking(ast, *args):
	Visitor(
		action  = action,
		labeled = labeled
	).visit(ast)


