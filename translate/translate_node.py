from typing import Dict, List, Any

from .kr_ExpressionStatement import kr_ExpressionStatement
from .kr_FunctionDeclaration import kr_FunctionDeclaration
from .kr_VariableDeclaration import kr_VariableDeclaration
from .kr_ReturnStatement import kr_ReturnStatement
from .kr_BinaryExpression import kr_BinaryExpression



def simplify_nodes(nodes: List[Dict[str, Any]], function_name: str) -> List[Dict[str, Any]]:
    """
    type이 kr_VariableDeclaration일 경우, declarations의 내용을 간략화시킵니다.
    """
    
    #리턴 결과용
    simplified_nodes = []
    # for node in nodes:
    #     if node.get('type') == 'Program':
    #         function_id = node.get('id')
    #         continue
    #kr_FunctionDeclaration 아이디 부여용
    # print(function_id)
    for node in nodes:
        #range삭제 
        del node['range']
        #가장 상위 아이디 가져오기
        #Params 보강 필요
        if node.get('type') == 'FunctionDeclaration':
            # print(function_id)
            simplified_nodes.append(kr_FunctionDeclaration(node,function_name))
        #끝
        elif node.get('type') == 'VariableDeclaration':
            simplified_nodes.append(kr_VariableDeclaration(node))
        #content 보강 필요
        elif node.get('type') == 'BlockStatement':
            simplified_nodes.append(node)
        elif node.get('type') == 'ExpressionStatement':
            simplified_nodes.append(kr_ExpressionStatement(node))
        elif node.get('type') == 'ReturnStatement':
            simplified_nodes.append(kr_ReturnStatement(node))
        elif node.get('type') == 'BinaryExpression':
            simplified_nodes.append(kr_BinaryExpression(node))
        elif node.get('type') == 'IfStatement':
            simplified_nodes.append(node)
        elif node.get('type') == 'Program':
            continue
        elif node.get('type') == 'CallExpression':
            simplified_nodes.append(kr_ExpressionStatement(node))
        else:
            print(f"예상치 못한 타입{node['type']} 발생")
            simplified_nodes.append(node)
            
    return simplified_nodes


def translate_main(nodes: List[Dict[str, Any]],function_name:str) -> List[Dict[str, Any]]:
    """
    노드의 형태를 동일한 형태로 변경합니다.
    """
    "Variable Declration 변환"
    modified_nodes = simplify_nodes(nodes, function_name)

    return modified_nodes