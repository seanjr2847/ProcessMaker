from typing import Dict, List, Any

def format_expression(expr):
    if isinstance(expr, dict):
        if expr['type'] == 'Identifier':
            return expr['name']
        elif expr['type'] == 'Literal':
            return expr['raw']
        elif expr['type'] == 'ArrayExpression':
            elements = [format_expression(elem) for elem in expr.get('elements', [])]
            return f"[{', '.join(elements)}]"
        elif expr['type'] == 'BinaryExpression':
            left = format_expression(expr['left'])
            right = format_expression(expr['right'])
            return f"({left} {expr['operator']} {right})"
        elif expr['type'] == 'MemberExpression':
            obj = format_expression(expr['object'])
            prop = format_expression(expr['property'])
            if expr.get('computed', False):
                return f"{obj}[{prop}]"
            else:
                return f"{obj}.{prop}"
        elif expr['type'] == 'CallExpression':
            callee = format_expression(expr['callee'])
            args = [format_expression(arg) for arg in expr.get('arguments', [])]
            return f"{callee}({', '.join(args)})"
        elif expr['type'] == 'ThisExpression':
            return 'this'
        else:
            return str(expr)
    else:
        return str(expr)

def ExpressionStatement(node: Dict[str, Any]) -> Dict[str, Any]:
    expression = node.get('expression')
    
    if expression and isinstance(expression, dict):
        expression_type = expression.get('type')
        
        if expression_type == 'CallExpression':
            callee = expression.get('callee', {})
            if isinstance(callee, dict) and callee.get('type') == 'Identifier':
                func_name = callee.get('name', '')
            else:
                func_name = format_expression(callee)
            
            arguments = expression.get('arguments', [])
            formatted_args = [format_expression(arg) for arg in arguments]
            
            node['content'] = f"{func_name}({', '.join(formatted_args)});"
            node['type'] = 'CallExpressionStatement'
        
        elif expression_type == 'AssignmentExpression':
            left = format_expression(expression.get('left', {}))
            right = format_expression(expression.get('right', {}))
            operator = expression.get('operator', '=')
            
            node['content'] = f"{left} {operator} {right};"
            node['type'] = 'AssignmentExpressionStatement'
        
        else:
            print(f"Unhandled expression type: {expression_type}")
            node['content'] = format_expression(expression) + ";"
    
    elif node.get('content') == "()":
        # content가 비어있는 경우 처리
        node['content'] = "// Empty expression"
    
    # 'expression' 키 제거
    if 'expression' in node:
        del node['expression']
    
    return node
