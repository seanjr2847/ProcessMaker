from typing import Dict, List, Any
import uuid

def create_node(node_type: str, body: Any) -> Dict[str, Any]:
    "노드의 기본틀을 제공합니다."
    return {
        "id": str(uuid.uuid4()),
        "parent_id": [],
        "child_ids": [],
        "type": node_type,
        "body": body
    }