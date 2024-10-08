from typing import Dict, List, Any


def BinaryExpression(node: Dict[str, Any]) -> Dict[str, Any]:
    operator = node.pop('operator', '')
    left = node.pop('left', {})
    right = node.pop('right', {})
    
    def format_operand(operand):
        if isinstance(operand, dict):
            if operand['type'] == 'Identifier':
                return operand.get('name', '')
            elif operand['type'] == 'Literal':
                return repr(operand.get('value', ''))
            elif operand['type'] == 'UnaryExpression':
                return f"{operand['operator']}{format_operand(operand['argument'])}"
            elif operand['type'] == 'MemberExpression':
                object_part = format_operand(operand['object'])
                property_part = format_operand(operand['property'])
                return f"{object_part}.{property_part}"
            else:
                return str(operand)
        else:
            return str(operand)
    
    left_str = format_operand(left)
    right_str = format_operand(right)
    
    node['content'] = f"{left_str} {operator} {right_str}"
    
    return node
