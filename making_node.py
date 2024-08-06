import uuid
import json
from typing import Dict, List, Any

def create_node(node_type: str, body: Any) -> Dict[str, Any]:
    "노드의 기본틀을 제공합니다."
    return {
        "id": str(uuid.uuid4()),
        "parent_id": [],
        "child_ids": [],
        "type": node_type,
        "body": body
    }

def process_node(node: Dict[str, Any], nodes: Dict[str, Dict[str, Any]]) -> str:
    """
    ast에서 노드를 분리합니다.
    """
    try:
        """
        1. 새로운 노드 생성
        create_node 함수를 호출하고, 새로운 노드 아이디를 부여한다.
        """
        new_node = create_node(node['type'], None)  # body를 나중에 채웁니다
        node_id = new_node['id']
        nodes[node_id] = new_node
        
        """
        2. 새로운 body 생성
        각 body에 자식 노드가 존재한다.
        자식 노드가 복수일 경우 리스트, 단수일 경우 딕셔너리로  존재하기 때문에 isinstance로 분기를 나눈다.
        """
        new_body = []
        if 'body' in node:
            if isinstance(node['body'], list):
                for item in node['body']:
                    if isinstance(item, dict) and 'type' in item:
                        """
                        3. 노드관계 및 자식노드 부여
                        body와 type을 노드의 가장 작은 단위로 설계한다.
                        노드가 아니게 될 때 까지 함수를 재귀호출하여 child-parent 관계를 설정한다.
                        """
                        child_id = process_node(item, nodes)
                        new_node['child_ids'].append(child_id)
                        nodes[child_id]['parent_id'].append(node_id)
                        
                        #이전 설계 잔재, 필요 없어지면 삭제할 예정
                        #new_body.append({"child_node_id": child_id})
            elif isinstance(node['body'], dict):
                if 'type' in node['body']:
                    child_id = process_node(node['body'], nodes)
                    new_node['child_ids'].append(child_id)
                    nodes[child_id]['parent_id'].append(node_id)
                    #이전 설계 잔재, 필요 없어지면 삭제할 예정
                    #new_body = {"child_node_id": child_id}
        """
        4. 값 저장
        body에 이전의 내용을 저장한다.
        각 type마다 키의 종류가 다르기 때문에, type과 body를 제외한 모든 키-밸류를 저장한다.
        """
        new_node['body'] = new_body
        for key, value in node.items():
            if key not in ['type', 'body']:
                new_node[key] = value
        
        return node_id
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return ""

def split_ast(ast: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    노드를 분리한 후, 각각의 노드를 딕셔너리 형태에 저장한다.
    """
    nodes = {}
    process_node(ast, nodes)
    return nodes

# 메인 함수
def node_main(ast: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    노드 분리 메인 함수
    """
    split_nodes = split_ast(ast)
    
    # 딕셔너리의 값들을 리스트로 변환
    nodes_list = list(split_nodes.values())
    
    return nodes_list