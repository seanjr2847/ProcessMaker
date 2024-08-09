#좌표 계산하는 함수
def assign_coordinates(node_list):
    # 노드 리스트를 딕셔너리로 변환
    nodes = {node['id']: node for node in node_list}
    
    def dfs(node_id, depth, x_pos):
        node = nodes[node_id]
        node['XY'] = (x_pos, depth)
        
        child_x = x_pos
        for child_id in node.get('child_ids', []):
            child_x = dfs(child_id, depth + 1, child_x)
            child_x += 1
        
        return max(x_pos, child_x - 1)

    # 루트 노드 찾기
    root = next(node for node in nodes.values() if not node['parent_id'])
    
    dfs(root['id'], 1, 1)
    node_coordinates = list(nodes.values())
    # 결과를 다시 리스트로 변환
    return node_coordinates

