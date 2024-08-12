from typing import Dict, Any

def ReturnStatement(node: Dict[str, Any]) -> Dict[str, Any]:
    argument = node.pop('argument', None)  # argument를 가져오고 원본에서 제거
    
    if argument is None:
        node['content'] = 'return'
    else:
        # argument가 있는 경우, 그 값을 적절히 처리
        if isinstance(argument, dict):
            if 'type' in argument and argument['type'] == 'Literal':
                node['content'] = f"{repr(argument.get('value', ''))} 반환"
            else:
                node['content'] = f"{str(argument)} 반환"
        else:
            node['content'] = f"{str(argument)} 반환"
    
    return node
