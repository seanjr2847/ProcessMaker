import uuid
from typing import Dict, List, Any
from common import create_node


def process_node(node: Dict[str, Any], nodes: Dict[str, Dict[str, Any]]) -> str:
    try:
        new_node = create_node(node['type'], None)
        node_id = new_node['id']
        nodes[node_id] = new_node

        new_body = []

        if node['type'] == 'IfStatement':
            # test 부분 처리
            if 'test' in node and isinstance(node['test'], dict):
                test_id = process_node(node['test'], nodes)
                new_node['child_ids'].append(test_id)
                nodes[test_id]['parent_id'].append(node_id)
                new_body.append({'type': 'test', 'id': test_id})

            # consequent 부분 처리
            if 'consequent' in node and isinstance(node['consequent'], dict):
                consequent_id = process_node(node['consequent'], nodes)
                new_node['child_ids'].append(consequent_id)
                nodes[consequent_id]['parent_id'].append(node_id)
                new_body.append({'type': 'consequent', 'id': consequent_id})

            # alternate 부분 처리
            if 'alternate' in node and isinstance(node['alternate'], dict):
                alternate_id = process_node(node['alternate'], nodes)
                new_node['child_ids'].append(alternate_id)
                nodes[alternate_id]['parent_id'].append(node_id)
                new_body.append({'type': 'alternate', 'id': alternate_id})

        elif 'body' in node:
            # 기존의 body 처리 로직
            if isinstance(node['body'], list):
                for item in node['body']:
                    if isinstance(item, dict) and 'type' in item:
                        child_id = process_node(item, nodes)
                        new_node['child_ids'].append(child_id)
                        nodes[child_id]['parent_id'].append(node_id)
                        new_body.append({'type': item['type'], 'id': child_id})
            elif isinstance(node['body'], dict) and 'type' in node['body']:
                child_id = process_node(node['body'], nodes)
                new_node['child_ids'].append(child_id)
                nodes[child_id]['parent_id'].append(node_id)
                new_body.append({'type': node['body']['type'], 'id': child_id})

        new_node['body'] = new_body
        for key, value in node.items():
            if key not in ['type', 'body', 'test', 'consequent', 'alternate']:
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