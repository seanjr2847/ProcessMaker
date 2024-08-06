from typing import Dict, List, Any

def remove_range_from_nodes(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    노드 리스트에서 각 딕셔너리에서 'range' 키를 제거합니다.
    """
    for node in nodes:
        if 'range' in node:
            del node['range']
    return nodes