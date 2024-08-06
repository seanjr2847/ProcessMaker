import uuid
import json
from typing import Dict, List, Any
from main import ast

def create_node(node_type: str, body: Any) -> Dict[str, Any]:
    "노드의 기본틀을 제공합니다."
    return {
        "id": str(uuid.uuid4()),
        "parent_id": [],
        "child_ids": [],
        "type": node_type,
        "body": body
    }

def transform_body(body: Any) -> Any:
    """
    body의 fomat을 바꿉니다. 
    현재는 일부분만 짤라서 반환하도록 만듬.
    """
    # if isinstance(body, list) and body:
    #     return [body[0]]
    # elif isinstance(body, dict):
    #     return {k: v for k, v in body.items() if k != 'body'}
    # else:
    return body

def process_node(node: Dict[str, Any], nodes: Dict[str, Dict[str, Any]]) -> str:
    """
    ast에서 노드를 분리합니다.
    """
    try:
        new_node = create_node(node['type'], None)  # body를 나중에 채웁니다
        node_id = new_node['id']
        nodes[node_id] = new_node
        
        new_body = []
        if 'body' in node:
            if isinstance(node['body'], list):
                for item in node['body']:
                    if isinstance(item, dict) and 'type' in item:
                        child_id = process_node(item, nodes)
                        new_node['child_ids'].append(child_id)
                        nodes[child_id]['parent_id'].append(node_id)
                        new_body.append({"child_node_id": child_id})
                    else:
                        new_body.append(transform_body(item))
            elif isinstance(node['body'], dict):
                if 'type' in node['body']:
                    child_id = process_node(node['body'], nodes)
                    new_node['child_ids'].append(child_id)
                    nodes[child_id]['parent_id'].append(node_id)
                    new_body = {"child_node_id": child_id}
                else:
                    new_body = transform_body(node['body'])
            else:
                new_body = transform_body(node['body'])
        else:
            new_body = transform_body(node)
        
        new_node['body'] = new_body
        
        # body 외의 다른 키들도 보존
        for key, value in node.items():
            if key not in ['type', 'body']:
                new_node[key] = value
        
        return node_id
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return ""

def split_ast(ast: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    노드를 분리한 후, 각각의 노드를 딕셔너리 형태에 저장합니다.
    """
    nodes = {}
    process_node(ast, nodes)
    return nodes

# 메인 함수
def main(ast: Dict[str, Any]) -> str:
    """
    노드 분리 메인 함수
    """
    split_nodes = split_ast(ast)
    return json.dumps(split_nodes, indent=2, ensure_ascii=False)

# 예시 사용 (실제 AST 입력은 제공되지 않음)
result = main(ast)
print(result)