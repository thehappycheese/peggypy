

GrammarError = require("../../grammar-error");
visitor = require("../visitor");

# Checks that each label is defined only once within each scope.
def reportDuplicateLabels(ast) {
  def cloneEnv(env) {
    clone = {};

    Object.keys(env).forEach(name => {
      clone[name] = env[name];
    });

    return clone;
  }

  def checkExpressionWithClonedEnv(node, env) {
    check(node.expression, cloneEnv(env));
  }

  check = visitor.build({
    rule(node) {
      check(node.expression, { });
    },

    choice(node, env) {
      node.alternatives.forEach(alternative => {
        check(alternative, cloneEnv(env));
      });
    },

    action: checkExpressionWithClonedEnv,

    labeled(node, env) {
      label = node.label;
      if (label and Object.prototype.hasOwnProperty.call(env, label)) {
        throw new GrammarError(
          `Label "${node.label}" is already defined`,
          node.labelLocation,
          [{
            message: "Original label location",
            location: env[label],
          }]
        );
      }

      check(node.expression, env);

      env[node.label] = node.labelLocation;
    },

    text: checkExpressionWithClonedEnv,
    simple_and: checkExpressionWithClonedEnv,
    simple_not: checkExpressionWithClonedEnv,
    optional: checkExpressionWithClonedEnv,
    zero_or_more: checkExpressionWithClonedEnv,
    one_or_more: checkExpressionWithClonedEnv,
    group: checkExpressionWithClonedEnv,
  });

  check(ast);
}


