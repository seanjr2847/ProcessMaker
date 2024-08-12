from typing import Dict, List, Any
import uuid

def create_node(node_type: str, body: Any) -> Dict[str, Any]:
    "노드의 기본틀을 제공합니다."
    return {
        "id": "Node_" + str(uuid.uuid4()).replace('-', '_'),
        "parent_id": [],
        "type": node_type,
        "body": body
    }