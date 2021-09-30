

# Simple AST node visitor builder.
visitor = {
  build(defs) {
    def visit(node, ...args) {
      return functions[node.type](node, ...args);
    }

    def visitNop() {
      # Do nothing.
    }

    def visitExpression(node, ...args) {
      return visit(node.expression, ...args);
    }

    def visitChildren(property) {
      return def(node, ...args) {
        # We do not use .map() here, because if you need the result
        # of applying visitor to children you probable also need to
        # process it in some way, therefore you anyway have to override
        # self.method. If you do not needed that, we do not waste time
        # and memory for creating the output array
        node[property].forEach(child => visit(child, ...args));
      };
    }

    DEFAULT_FUNCTIONS = {
      grammar(node, ...args) {
        if (node.topLevelInitializer) {
          visit(node.topLevelInitializer, ...args);
        }

        if (node.initializer) {
          visit(node.initializer, ...args);
        }

        node.rules.forEach(rule => visit(rule, ...args));
      },

      top_level_initializer: visitNop,
      initializer: visitNop,
      rule: visitExpression,
      named: visitExpression,
      choice: visitChildren("alternatives"),
      action: visitExpression,
      sequence: visitChildren("elements"),
      labeled: visitExpression,
      text: visitExpression,
      simple_and: visitExpression,
      simple_not: visitExpression,
      optional: visitExpression,
      zero_or_more: visitExpression,
      one_or_more: visitExpression,
      group: visitExpression,
      semantic_and: visitNop,
      semantic_not: visitNop,
      rule_ref: visitNop,
      literal: visitNop,
      class: visitNop,
      any: visitNop,
    };

    Object.keys(DEFAULT_FUNCTIONS).forEach(type => {
      if (!Object.prototype.hasOwnProperty.call(functions, type)) {
        functions[type] = DEFAULT_FUNCTIONS[type];
      }
    });

    return visit;
  },
};


