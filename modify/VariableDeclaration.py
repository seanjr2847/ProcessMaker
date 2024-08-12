from typing import Dict, Any

def VariableDeclaration(node: Dict[str, Any]) -> Dict[str, Any]:
    """
    type이 VariableDeclaration일 경우, declarations의 내용을 간략화시킵니다.
    """
    declarations = node.get('declarations', [])
    kind = node.get('kind', 'var')
    
    transformed_declarations = []
    
    for declaration in declarations:
        var_name = declaration.get('id', {}).get('name', 'name')
        init_value = declaration.get('init', {}).get('raw', 'undefined')
        transformed_declaration = f"{kind} {var_name} = {init_value};"
        transformed_declarations.append(transformed_declaration)

    modified_declaration = ' '.join(transformed_declarations)
    
    # 새로운 'content' 키에 modified_declaration 값을 할당
    node['content'] = modified_declaration
    
    # 'kind' 키 삭제
    del node['kind']
    del node['declarations']
    
    # 'body' 키 유지 (이미 존재한다고 가정)
    # 만약 'body' 키가 없다면, 다음 줄의 주석을 해제하여 빈 딕셔너리를 할당할 수 있습니다
    # node['body'] = node.get('body', {})
    
    return node
