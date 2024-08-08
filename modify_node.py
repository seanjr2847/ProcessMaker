from typing import Dict, List, Any
from common import create_node
from making_node import process_node

def modify_IfStatement_Test(test: Dict[str, Any])-> str:
    child_id: str = "11"
    return child_id

def modify_if_consequent(test: Dict[str, Any]):
    return test

def modify_if_alternate(test: Dict[str, Any]):
    return test

def modify_IfStatement(node: Dict[str, Any], nodes: Dict[str, Dict[str, Any]]) -> list:
    new_body = []
    if 'test' in node:
        if isinstance(node['test'], dict):
            #해당 함수에서 이를 nodeformat으로 만든다.
            if_test_node = create_node('IfStatementTest', None)  # body를 나중에 채웁니다
            #child_id = modify_IfStatement_Test(node['test'])
            test_node_id = if_test_node['id']
            #test_node['child_ids'].append(child_id)
            if_test_node['parent_id'].append(node['id'])
            nodes.append(if_test_node)
            #print(if_test_node)
        else:
            print("if 구문에서 test 파싱하는 과정에서 에러 발생")

    if 'consequent' in node:
        if isinstance(node['consequent'], dict):
            input_consequent: dict = node['consequent']
            consequent_nodes = {}
            hi = process_node(input_consequent, consequent_nodes)
            
            modify_if_consequent(node['consequent'])
        else:
            print("if 구문에서 consequent 파싱하는 과정에서 에러 발생")
    
    if 'alternate' in node:
        if node['alternate'] != None:
            modify_if_alternate(node['alternate'])
        elif node['alternate'] == None:
            del node['alternate']
        else:
            print("if 구문에서 alternate 파싱하는 과정에서 에러 발생")
    """
    4. 값 저장
    body에 이전의 내용을 저장한다.
    각 type마다 키의 종류가 다르기 때문에, type과 body를 제외한 모든 키-밸류를 저장한다.
    """
    # new_node['body'] = new_body
    # for key, value in node.items():
    #     if key not in ['type', 'body']:
    #         new_node[key] = value
    
    return 


def ExpressionStatement(node: Dict[str, Any]) -> Dict[str, Any]:
    expression = node['expression']
    expression_type = expression['type']
    
    #del expression['range']
    
    if expression_type == 'CallExpression':
        #호출하는 대상을 가져온다.
        # 'name' 키 확인 및 처리
        callee = expression.get('callee', {})
        if isinstance(callee, dict):
            name = callee.get('name', '???')
        else:
            name = str(callee)  # 또는 다른 적절한 처리

        expression['callee'] = name
        
        #호출하는 대상의 파라미터를 가져온다.
        try:
            if expression.get('arguments') is not None:
                arguments = [arg.get('value', None) if arg is not None else None for arg in expression['arguments']]
            else:
                arguments = []
        except Exception as e:
            print(f"Error processing arguments: {e}")
        arguments = []

        expression['arguments'] = arguments
        
        #노드 타입을 변경한다.
        node['type'] = 'CallExpressionStatement'
        
        formatted_arguments = ', '.join(map(str, expression['arguments']))
        node['expression'] = f'{expression["callee"]}({formatted_arguments})'

    elif expression_type == '추가로 등장하는 expression 기입':
        return node
    else:
        print(f"해결 못한 조건 발견:{expression_type}")
        return node
    
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
    #리턴 결과용
    simplified_nodes = []
    
    #FunctionDeclaration 아이디 부여용
    function_id = ""
    # if statement 재귀함수 부여용
    if_nodes = []
    for node in nodes:
        del node['range']
        a = node.get('type')
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
        #elif node.get('type') == 'IfStatement':
            #simplified_nodes.append(modify_IfStatement(node,if_nodes))
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