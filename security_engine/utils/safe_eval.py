import ast
import operator
from typing import Any, Dict, List, Mapping


class UnsafeExpressionError(ValueError):
    """Raised when a rule expression uses syntax outside the supported language."""


class _SafeExpressionEvaluator(ast.NodeVisitor):
    _SAFE_BUILTINS = {
        'all': all,
        'any': any,
        'bool': bool,
    }
    _BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
    }
    _COMPARISON_OPERATORS = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.In: lambda left, right: left in right,
        ast.NotIn: lambda left, right: left not in right,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
    }

    def __init__(self, variables: Mapping[str, Any]) -> None:
        self.variables = dict(variables)

    def visit_Expression(self, node: ast.Expression) -> Any:
        return self.visit(node.body)

    def visit_Constant(self, node: ast.Constant) -> Any:
        return node.value

    def visit_Name(self, node: ast.Name) -> Any:
        if node.id in self.variables:
            return self.variables[node.id]
        if node.id in self._SAFE_BUILTINS:
            return self._SAFE_BUILTINS[node.id]
        raise UnsafeExpressionError('Unknown name: {}'.format(node.id))

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if node.attr.startswith('_'):
            raise UnsafeExpressionError('Private attributes are not allowed')
        value = self.visit(node.value)
        try:
            return getattr(value, node.attr)
        except AttributeError as error:
            raise UnsafeExpressionError(
                'Attribute does not exist: {}'.format(node.attr)
            ) from error

    def visit_Subscript(self, node: ast.Subscript) -> Any:
        value = self.visit(node.value)
        index = self.visit(node.slice)
        try:
            return value[index]
        except (IndexError, KeyError, TypeError) as error:
            raise UnsafeExpressionError('Invalid subscript') from error

    def visit_Index(self, node: ast.Index) -> Any:
        return self.visit(node.value)

    def visit_List(self, node: ast.List) -> List[Any]:
        return [self.visit(element) for element in node.elts]

    def visit_Tuple(self, node: ast.Tuple) -> tuple:
        return tuple(self.visit(element) for element in node.elts)

    def visit_Set(self, node: ast.Set) -> set:
        return {self.visit(element) for element in node.elts}

    def visit_Dict(self, node: ast.Dict) -> Dict[Any, Any]:
        return {
            self.visit(key): self.visit(value)
            for key, value in zip(node.keys, node.values)
        }

    def visit_BoolOp(self, node: ast.BoolOp) -> Any:
        if isinstance(node.op, ast.And):
            result = True
            for value in node.values:
                result = self.visit(value)
                if not result:
                    return result
            return result
        if isinstance(node.op, ast.Or):
            result = False
            for value in node.values:
                result = self.visit(value)
                if result:
                    return result
            return result
        raise UnsafeExpressionError('Unsupported boolean operator')

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Any:
        operand = self.visit(node.operand)
        if isinstance(node.op, ast.Not):
            return not operand
        if isinstance(node.op, ast.USub):
            return -operand
        if isinstance(node.op, ast.UAdd):
            return +operand
        raise UnsafeExpressionError('Unsupported unary operator')

    def visit_BinOp(self, node: ast.BinOp) -> Any:
        operator_fn = self._BINARY_OPERATORS.get(type(node.op))
        if operator_fn is None:
            raise UnsafeExpressionError('Unsupported binary operator')
        return operator_fn(self.visit(node.left), self.visit(node.right))

    def visit_Compare(self, node: ast.Compare) -> bool:
        left = self.visit(node.left)
        for operator_node, comparator in zip(node.ops, node.comparators):
            operator_fn = self._COMPARISON_OPERATORS.get(type(operator_node))
            if operator_fn is None:
                raise UnsafeExpressionError('Unsupported comparison operator')
            right = self.visit(comparator)
            if not operator_fn(left, right):
                return False
            left = right
        return True

    def visit_Call(self, node: ast.Call) -> Any:
        if not isinstance(node.func, ast.Name):
            raise UnsafeExpressionError('Only named functions may be called')
        function_name = node.func.id
        if function_name.startswith('_'):
            raise UnsafeExpressionError('Private functions are not allowed')
        function = self.visit(node.func)
        if not callable(function):
            raise UnsafeExpressionError(
                '{} is not callable'.format(function_name)
            )
        if node.keywords:
            raise UnsafeExpressionError('Keyword arguments are not allowed')
        return function(
            *(self.visit(argument) for argument in node.args)
        )

    def visit_ListComp(self, node: ast.ListComp) -> List[Any]:
        if len(node.generators) != 1:
            raise UnsafeExpressionError('Nested comprehensions are not allowed')
        generator = node.generators[0]
        if generator.is_async or generator.ifs:
            raise UnsafeExpressionError('Filtered comprehensions are not allowed')
        if not isinstance(generator.target, ast.Name):
            raise UnsafeExpressionError('Only simple comprehension targets are allowed')

        iterable = self.visit(generator.iter)
        results = []
        for item in iterable:
            previous = self.variables.get(generator.target.id, None)
            had_previous = generator.target.id in self.variables
            self.variables[generator.target.id] = item
            try:
                results.append(self.visit(node.elt))
            finally:
                if had_previous:
                    self.variables[generator.target.id] = previous
                else:
                    self.variables.pop(generator.target.id, None)
        return results

    def generic_visit(self, node: ast.AST) -> Any:
        raise UnsafeExpressionError(
            'Unsupported expression node: {}'.format(type(node).__name__)
        )


def safe_eval(expression: str, variables: Mapping[str, Any]) -> Any:
    """Evaluate the supported rule-expression subset without Python builtins."""
    if not isinstance(expression, str) or not expression.strip():
        raise UnsafeExpressionError('Expression must be a non-empty string')

    try:
        parsed = ast.parse(expression, mode='eval')
    except SyntaxError as error:
        raise UnsafeExpressionError('Invalid expression syntax') from error

    return _SafeExpressionEvaluator(variables).visit(parsed)
