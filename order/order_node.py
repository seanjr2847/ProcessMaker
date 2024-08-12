def order_BlockStatement(nodes):
    block_replacements = {}
    node_map = {node['id']: node for node in nodes}

    def collect_block_replacements(node):
        if node['type'] == 'BlockStatement' and 'body' in node and node['body']:
            first_child = node['body'][0]
            if isinstance(first_child, dict):
                first_child_id = first_child['id']
            else:
                first_child_id = first_child
            block_replacements[node['id']] = first_child_id

    def deep_replace(item):
        if isinstance(item, dict):
            for key, value in item.items():
                if key == 'id' and value in block_replacements:
                    item[key] = block_replacements[value]
                else:
                    item[key] = deep_replace(value)
            return item
        elif isinstance(item, list):
            return [deep_replace(element) for element in item]
        else:
            return block_replacements.get(item, item) if isinstance(item, str) else item

    # First pass: collect all block replacements
    for node in nodes:
        collect_block_replacements(node)

    # Second pass: apply replacements deeply
    updated_nodes = []
    for node in nodes:
        if node['type'] != 'BlockStatement' or node['id'] not in block_replacements:
            updated_node = deep_replace(node)
            updated_nodes.append(updated_node)

    return updated_nodes


def order_ifStatement(nodes):
    for node in nodes:
        if node['type'] == 'IfStatement':
            test_node = next((n for n in nodes if n['id'] == node['body'][0]['id']), None)
            if test_node and test_node['type'] == 'BinaryExpression':
                # test 노드의 내용을 IfStatement 노드로 옮깁니다
                node['content'] = test_node['content']
                # body에서 test 항목을 제거합니다
                node['body'] = [item for item in node['body'] if item['type'] != 'test']
                # nodes 리스트에서 test 노드를 제거합니다
                nodes = [n for n in nodes if n['id'] != test_node['id']]
    return nodes


def order_node(nodes:dict):
    "BlockStatement와 IfStatement의 부모관계를 재배열합니다."
    result = order_BlockStatement(nodes)
    #result = order_ifStatement(nodes)
    return result