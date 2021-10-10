
from typing import Any
from peggypy.compiler.utils_and_types.syntax_tree import Action, Grammar, Labeled
from ..grammar_error import GrammarError, Diagnostic
from .utils_and_types.visitor import Visitor


def action(self:Visitor, node:Action, options:dict[str, Any]):
	self.visit(node.expression, {**options, "action":node})

def labeled(self:Visitor, node:Labeled, options:dict[str, Any]):
	if node.pick:
		if action:
			raise GrammarError(
				"\"@\" cannot be used with an action block",
				node.labelLocation,
				[Diagnostic(
					message = "Action block location",
					location = options["action"].codeLocation,
				)]
			)

	self.visit(node.expression, options)

def reportIncorrectPlucking(grammar:Grammar, options:dict[str, Any]):
	"""Check that plucking `@` is not attempted with an Action `{}` block (eg the following is forbidden: `SomeRule = "SomeLiteral" @SomePattern {...code}`)"""
	Visitor({
		"action"  : action,
		"labeled" : labeled
	}).visit(grammar, options)


