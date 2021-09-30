

GrammarError = require("../../grammar-error");
visitor = require("../visitor");

# Checks that each rule is defined only once.
def reportDuplicateRules(ast) {
  rules = {};

  check = visitor.build({
    rule(node) {
      if (Object.prototype.hasOwnProperty.call(rules, node.name)) {
        throw new GrammarError(
          `Rule "${node.name}" is already defined`,
          node.nameLocation,
          [{
            message: "Original rule location",
            location: rules[node.name],
          }]
        );
      }

      rules[node.name] = node.nameLocation;
    },
  });

  check(ast);
}


