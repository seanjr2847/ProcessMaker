from typing import Dict, List, Any

def ExpressionStatement(node: Dict[str, Any]) -> Dict[str, Any]:
    expression = node['expression']
    expression_type = expression['type']
    
    del expression['range']
    
    if expression_type == 'CallExpression':
        #호출하는 대상을 가져온다.
        name = expression['callee']['name']
        expression['callee'] = name
        
        #호출하는 대상의 파라미터를 가져온다.
        arguments = [arg['value'] for arg in expression['arguments']]
        expression['arguments'] = arguments
        
        #노드 타입을 변경한다.
        node['type'] = 'CallExpressionStatement'

        
    
    # 전체 변환된 선언들을 저장할 리스트
    transformed_declarations = []
    
    # # declaration에서 값 가져올거 탐색함
    # for declaration in declarations:
    #     var_name = declaration.get('id', {}).get('name', 'name')
    #     init_value = declaration.get('init', {}).get('raw', 'undefined')
    #     transformed_declaration = f"{kind} {var_name} = {init_value};"
    #     transformed_declarations.append(transformed_declaration)

    # # 변환된 선언들을 하나의 문자열로 결합 (변수 선언 여러개일수도 있으니까)
    # modified_declaration = ' '.join(transformed_declarations)
    
    # # node['declarations']를 변환된 문자열로 변경
    # node['declarations'] = modified_declaration
    
    # "기본 포맷으로 변경"
    # del node['body']
    # del node['kind']
    # node['body'] = node.pop('declarations')
    
    return node

def FunctionDeclaration(node: Dict[str, Any], function_id:str) -> Dict[str, Any]:
    # id 값을 function_id로 변경
    # id 값을 문자열로 변환하여 function_id에 저장
    if "id" in node:
        node["id"] = function_id
    
    if isinstance(node.get('parent_id'), list):
        node['parent_id'].clear()

    # 각 아래조건은 특수함수고, 현재로선 대응하지 않음. 향후 대비하기 위해서 로그만 남겨놓는다.
    if node.get('generator') == False:
        del node['generator']
    else:
        print("함수 종류가 예상과 다름!! generator임")
        return None
    
    if node.get('async') == False:
        del node['async']
    else:
        print("함수 종류가 예상과 다름!! async임")
        return None
    
    if node.get('expression') == False:
        del node['expression']
    else:
        print("함수 종류가 예상과 다름!! expression임")
        return None

    return node


def VariableDeclaration(node: Dict[str, Any]) -> Dict[str, Any]:
    """
    type이 VariableDeclaration일 경우, declarations의 내용을 간략화시킵니다.
    """
    declarations = node.get('declarations', [])
    # 해당 선언에서 var 가져옴
    kind = node.get('kind', 'var')
    
    # 전체 변환된 선언들을 저장할 리스트
    transformed_declarations = []
    
    # declaration에서 값 가져올거 탐색함
    for declaration in declarations:
        var_name = declaration.get('id', {}).get('name', 'name')
        init_value = declaration.get('init', {}).get('raw', 'undefined')
        transformed_declaration = f"{kind} {var_name} = {init_value};"
        transformed_declarations.append(transformed_declaration)

    # 변환된 선언들을 하나의 문자열로 결합 (변수 선언 여러개일수도 있으니까)
    modified_declaration = ' '.join(transformed_declarations)
    
    # node['declarations']를 변환된 문자열로 변경
    node['declarations'] = modified_declaration
    
    "기본 포맷으로 변경"
    del node['body']
    del node['kind']
    node['body'] = node.pop('declarations')
    
    return node

def simplify_nodes(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    type이 VariableDeclaration일 경우, declarations의 내용을 간략화시킵니다.
    """
    simplified_nodes = []
    function_id = ""
    for node in nodes:
        del node['range']
        
        if node.get('type') == 'Program':
            function_id = node.get('id')
            continue
        elif node.get('type') == 'FunctionDeclaration':
            simplified_nodes.append(FunctionDeclaration(node,function_id))
        elif node.get('type') == 'VariableDeclaration':
            simplified_nodes.append(VariableDeclaration(node))
        elif node.get('type') == 'BlockStatement':
            simplified_nodes.append(node)
        elif node.get('type') == 'ExpressionStatement':
            simplified_nodes.append(ExpressionStatement(node))
        # elif node.get('type') == 'IfStatement':
        #     simplified_nodes.append(VariableDeclaration(node))
        else:
            #print("예상치 못한 타입 발생")
            simplified_nodes.append(node)
            

    return simplified_nodes


def modify_main(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    ast 형태를 가다듬습니다.
    """
    "Variable Declration 변환"
    modified_nodes = simplify_nodes(nodes)

    return modified_nodes