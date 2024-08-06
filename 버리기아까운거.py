from main import ast

def find_deepest_nodes_with_parent(node, parent=None, depth=0, max_depth_info=None):
    if max_depth_info is None:
        max_depth_info = {"max_depth": 0, "nodes": [], "parents": []}
    
    if not isinstance(node, dict):
        return max_depth_info
    
    if depth > max_depth_info["max_depth"]:
        max_depth_info["max_depth"] = depth
        max_depth_info["nodes"] = [node]
        max_depth_info["parents"] = [parent]
    elif depth == max_depth_info["max_depth"]:
        max_depth_info["nodes"].append(node)
        max_depth_info["parents"].append(parent)
    
    for key, value in node.items():
        if isinstance(value, dict):
            find_deepest_nodes_with_parent(value, node, depth + 1, max_depth_info)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    find_deepest_nodes_with_parent(item, node, depth + 1, max_depth_info)
    
    return max_depth_info


def find_parent_with_body(deepest_nodes, deepest_parents, ast):
    parents_with_body = []

    def find_parent(node, target_node):
        """ 재귀적으로 부모 노드를 찾는 함수 """
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, list):
                    for item in value:
                        if item is target_node:
                            return node
                        parent = find_parent(item, target_node)
                        if parent:
                            return parent
                elif isinstance(value, dict):
                    if value is target_node:
                        return node
                    parent = find_parent(value, target_node)
                    if parent:
                        return parent
        return None

    for node, parent in zip(deepest_nodes, deepest_parents):
        current_node = node
        current_parent = parent
        while current_parent is not None:
            if "body" in current_parent:
                parents_with_body.append(current_parent)
                break
            current_node = current_parent
            current_parent = find_parent(ast, current_node)
    
    return parents_with_body




def simplify_node(node):
    # 예시 간략화: 모든 리프 노드를 타입만 남기고 간략화
    simplified_node = {"type": node.get("type", "Unknown")}
    return simplified_node

def update_parent_with_simplified_node(parent, target_node, simplified_node):
    if isinstance(parent, dict):
        for key, value in parent.items():
            if isinstance(value, list):
                for i, item in enumerate(value):
                    if item is target_node:
                        parent[key][i] = simplified_node
                        return True
                    if update_parent_with_simplified_node(item, target_node, simplified_node):
                        return True
            elif isinstance(value, dict):
                if value is target_node:
                    parent[key] = simplified_node
                    return True
                if update_parent_with_simplified_node(value, target_node, simplified_node):
                    return True
    return False



def main(ast):
    # 하위 노드 찾기
    deepest_nodes_info = find_deepest_nodes_with_parent(ast)
    deepest_nodes = deepest_nodes_info["nodes"]
    deepest_parents = deepest_nodes_info["parents"]

    # body 키를 가진 부모 노드 찾기
    parent_child_pairs = find_parent_with_body(deepest_nodes, deepest_parents, ast)

    # 중복값 제거
    unique_parent_child_pairs = list({id(pair): pair for pair in parent_child_pairs}.values())

    # 디버깅 출력


    return unique_parent_child_pairs







# AST 간략화 예제
result = main(ast)
print(result)