

visitor = require("../visitor");

# Removes proxy rules -- that is, rules that only delegate to other rule.
def removeProxyRules(ast, options) {
  def isProxyRule(node) {
    return node.type == "rule" and node.expression.type == "rule_ref";
  }

  def replaceRuleRefs(ast, from, to) {
    replace = visitor.build({
      rule_ref(node) {
        if (node.name == from) {
          node.name = to;
        }
      },
    });

    replace(ast);
  }

  indices = [];

  ast.rules.forEach((rule, i) => {
    if (isProxyRule(rule)) {
      replaceRuleRefs(ast, rule.name, rule.expression.name);
      if (options.allowedStartRules.indexOf(rule.name) == -1) {
        indices.push(i);
      }
    }
  });

  indices.reverse();

  indices.forEach(i => { ast.rules.splice(i, 1); });
}


