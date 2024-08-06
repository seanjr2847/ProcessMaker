def extract_first_depth_types(data):
    types = []
    
    def traverse_first_depth(node):
        if isinstance(node, dict):
            # 첫 번째 depth의 type을 추출
            if "type" in node:
                types.append(node["type"])
            # 첫 번째 depth의 모든 key에 대해 탐색
            for key, value in node.items():
                if isinstance(value, dict):
                    if "type" in value:
                        types.append(value["type"])
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict) and "type" in item:
                            types.append(item["type"])

    traverse_first_depth(data)
    return types


def extract_inner_depth_dicts(data):
    dicts = []
    
    def traverse_inner_depth(node):
        if isinstance(node, dict):
            # 첫 번째 depth의 모든 value에 대해 탐색
            for key, value in node.items():
                if isinstance(value, dict):
                    # 두 번째 depth의 딕셔너리를 수집
                    dicts.append(value)
                    # 두 번째 depth의 딕셔너리의 모든 key에 대해 탐색
                    for subkey, subvalue in value.items():
                        if isinstance(subvalue, dict):
                            dicts.append(subvalue)
                        elif isinstance(subvalue, list):
                            for item in subvalue:
                                if isinstance(item, dict):
                                    dicts.append(item)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            # 두 번째 depth의 딕셔너리를 수집
                            dicts.append(item)
                            # 두 번째 depth의 리스트 요소의 모든 key에 대해 탐색
                            for subkey, subvalue in item.items():
                                if isinstance(subvalue, dict):
                                    dicts.append(subvalue)
                                elif isinstance(subvalue, list):
                                    for subitem in subvalue:
                                        if isinstance(subitem, dict):
                                            dicts.append(subitem)

    traverse_inner_depth(data)
    return dicts
