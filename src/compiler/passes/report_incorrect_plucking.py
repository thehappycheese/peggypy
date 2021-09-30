

GrammarError = require("../../grammar-error");
visitor = require("../visitor");

#
# Compiler pass to ensure the following are enforced:
#
#   - plucking can not be done with an action block
#
def reportIncorrectPlucking(ast) {
  check = visitor.build({
    action(node) {
      check(node.expression, node);
    },

    labeled(node, action) {
      if (node.pick) {
        if (action) {
          throw new GrammarError(
            "\"@\" cannot be used with an action block",
            node.labelLocation,
            [{
              message: "Action block location",
              location: action.codeLocation,
            }]
          );
        }
      }

      check(node.expression);
    },
  });

  check(ast);
}


