from typing import Dict, List, Any

from .ExpressionStatement import ExpressionStatement
from .FunctionDeclaration import FunctionDeclaration
from .VariableDeclaration import VariableDeclaration
from .ReturnStatement import ReturnStatement
from .BinaryExpression import BinaryExpression



def simplify_nodes(nodes: List[Dict[str, Any]], function_name: str) -> List[Dict[str, Any]]:
    """
    type이 VariableDeclaration일 경우, declarations의 내용을 간략화시킵니다.
    """
    
    #리턴 결과용
    simplified_nodes = []
    # for node in nodes:
    #     if node.get('type') == 'Program':
    #         function_id = node.get('id')
    #         continue
    #FunctionDeclaration 아이디 부여용
    # print(function_id)
    for node in nodes:
        #range삭제 
        del node['range']
        #가장 상위 아이디 가져오기
        #Params 보강 필요
        if node.get('type') == 'FunctionDeclaration':
            # print(function_id)
            simplified_nodes.append(FunctionDeclaration(node,function_name))
        #끝
        elif node.get('type') == 'VariableDeclaration':
            simplified_nodes.append(VariableDeclaration(node))
        #content 보강 필요
        elif node.get('type') == 'BlockStatement':
            simplified_nodes.append(node)
        elif node.get('type') == 'ExpressionStatement':
            simplified_nodes.append(ExpressionStatement(node))
        elif node.get('type') == 'ReturnStatement':
            simplified_nodes.append(ReturnStatement(node))
        elif node.get('type') == 'BinaryExpression':
            simplified_nodes.append(BinaryExpression(node))
        elif node.get('type') == 'IfStatement':
            simplified_nodes.append(node)
        elif node.get('type') == 'Program':
            continue
        else:
            print(f"예상치 못한 타입{node['type']} 발생")
            simplified_nodes.append(node)
            
    return simplified_nodes


def modify_main(nodes: List[Dict[str, Any]],function_name:str) -> List[Dict[str, Any]]:
    """
    ast 형태를 가다듬습니다.
    """
    "Variable Declration 변환"
    modified_nodes = simplify_nodes(nodes, function_name)

    return modified_nodes