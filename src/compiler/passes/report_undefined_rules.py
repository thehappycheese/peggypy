

GrammarError = require("../../grammar-error");
asts = require("../asts");
visitor = require("../visitor");

# Checks that all referenced rules exist.
def reportUndefinedRules(ast) {
  check = visitor.build({
    rule_ref(node) {
      if (!asts.findRule(ast, node.name)) {
        throw new GrammarError(
          `Rule "${node.name}" is not defined`,
          node.location
        );
      }
    },
  });

  check(ast);
}


