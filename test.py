def validate_parent_relationships(node_list):
    all_ids = set()
    id_to_node = {}
    root_nodes = set()

    # 첫 번째 패스: 모든 ID 수집 및 기본 유효성 검사
    for node in node_list:
        node_id = node.get('id')
        if isinstance(node_id, dict):
            node_id = node_id.get('name')
        if not node_id:  # 빈 문자열 또는 None 체크
            return False, "빈 ID를 가진 노드가 있습니다."
        if node_id in all_ids:
            return False, f"중복된 ID '{node_id}'가 발견되었습니다."
        all_ids.add(node_id)
        id_to_node[node_id] = node
        
        parent_ids = node.get('parent_id', [])
        if not isinstance(parent_ids, list):
            parent_ids = [parent_ids]
        if not parent_ids:
            root_nodes.add(node_id)
        elif len(parent_ids) > 1:
            return False, f"노드 '{node_id}'가 여러 부모를 가지고 있습니다."

    if not root_nodes:
        return False, "루트 노드가 없습니다."

    # 두 번째 패스: 부모-자식 관계 검증
    for node in node_list:
        node_id = node.get('id')
        if isinstance(node_id, dict):
            node_id = node_id.get('name')
        parent_id = node.get('parent_id')
        
        if parent_id:
            if isinstance(parent_id, list):
                parent_id = parent_id[0]  # 단일 부모만 허용
            if parent_id not in all_ids:
                return False, f"노드 '{node_id}'의 부모 ID '{parent_id}'가 존재하지 않습니다."
            
            # 실제 부모 노드 존재 여부 확인
            parent_node = id_to_node.get(parent_id)
            if not parent_node:
                return False, f"노드 '{node_id}'의 부모 ID '{parent_id}'에 해당하는 실제 노드가 존재하지 않습니다."
            
            # 부모 노드의 자식 목록에 현재 노드가 포함되어 있는지 확인
            children = parent_node.get('body', [])
            child_ids = [child.get('id') for child in children if isinstance(child, dict)]
            if node_id not in child_ids:
                return False, f"노드 '{node_id}'가 부모 노드 '{parent_id}'의 자식 목록에 포함되어 있지 않습니다."


    # 순환 참조 검사 (반복적 접근)
    def detect_cycle(start_id):
        visited = set()
        stack = [(start_id, [start_id])]
        while stack:
            node_id, path = stack.pop()
            if node_id in visited:
                continue
            visited.add(node_id)
            node = id_to_node[node_id]
            parent_id = node.get('parent_id')
            if parent_id:
                if isinstance(parent_id, list):
                    parent_id = parent_id[0]
                if parent_id in path:
                    return path[path.index(parent_id):] + [parent_id]
                stack.append((parent_id, path + [parent_id]))
        return None

    for node_id in all_ids:
        cycle = detect_cycle(node_id)
        if cycle:
            cycle_str = " -> ".join(cycle)
            return False, f"순환 참조가 발견되었습니다: {cycle_str}"

    return True, "모든 부모-자식 관계가 올바르게 설정되었습니다."
