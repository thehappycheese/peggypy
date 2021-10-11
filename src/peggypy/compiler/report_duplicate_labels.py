
from typing import Any
from .utils_and_types.syntax_tree import Choice, Expression, Labeled, Node, Rule
from ..grammar_error import GrammarError, Diagnostic
from .utils_and_types.visitor import Visitor



def checkExpressionWithClonedEnv(self:Visitor, node:Expression, options:dict[str, Any]):
	# clone `env` when visiting an expression
	self.visit(node.expression, {**options, "env":options["env"].copy()})


def rule(self:Visitor, node:Rule, options:dict[str, Any]):
	# reset `env` when visiting a rule
	# Because the scope of a label: is reset for each rule
	self.visit(node.expression, {**options, "env":{}})


def choice(self:Visitor, node:Choice, options:dict[str, Any]):
	# clone `env` for each choice when visiting a choice
	# because lables may be repeated in each choice, but may not repeat 
	# a lable previously defined in the parents of the Choice node?? TODO ?? is this correct?
	for alternative in node.alternatives:
		self.visit(alternative, {**options," env":options["env"].copy()})
	

def labeled(self:Visitor, node:Labeled, options:dict[str, Any]):
	# TODO: it is odd that node.label can be None
	if node.label is not None and node.label in options["env"]:
		raise GrammarError(
			f'Label "{node.label}" is already defined',
			node.labelLocation,
			[Diagnostic(
				message= "Original label location",
				location= options["env"][node.label],
			)]
		)
	self.visit(node.expression, options)
	if node.label is not None:
		options["env"][node.label] = node.labelLocation
	else:
		# TODO: not sure what to do in this situation the other branch would not be an error in javascript
		#       this is maybe a benign bug in the original code? or was it deliberate behaviour?
		raise KeyError("What do we do about this error? In the original javascript code `undefined` is a legal index. Python does not allow `None` to be used as an index.")


report_duplicate_labels_visitor = Visitor({
	"rule"         : rule,
	"choice"       : choice,
	"action"       : checkExpressionWithClonedEnv,
	"labeled"      : labeled,
	"text"         : checkExpressionWithClonedEnv,
	"simple_and"   : checkExpressionWithClonedEnv,
	"simple_not"   : checkExpressionWithClonedEnv,
	"optional"     : checkExpressionWithClonedEnv,
	"zero_or_more" : checkExpressionWithClonedEnv,
	"one_or_more"  : checkExpressionWithClonedEnv,
	"group"        : checkExpressionWithClonedEnv,
})


def report_duplicate_labels(grammar:Node, options:dict[str, Any]):
	"""
	Raises a GrammarError if a label is defined more than once within each scope.
	"""
	report_duplicate_labels_visitor.visit(grammar, {
		**options,
		"env":{},
		"grammar":grammar
	})



