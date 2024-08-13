def order_BlockStatement(nodes):

    iteration = 1
    while True:
        block_statements = find_block_statements(nodes)
        if not block_statements:
            break

        print(f"\n반복 {iteration} 시작:")
        for block in block_statements:
            block_id = block['id']
            first_child_id = get_first_child_id(block)

            print(f"\nBlockStatement 처리: {block_id}")
            print(f"첫 번째 자식 ID: {first_child_id}")

            if first_child_id:
                # 블록의 모든 자식들의 parent_id 업데이트
                update_child_parent_ids(nodes, block_id, first_child_id)

                # 부모 노드들의 body 업데이트
                update_parent_body(nodes, block_id, first_child_id)

                # BlockStatement에서 첫 번째 자식으로 parent_id 전달
                first_child = next((n for n in nodes if n['id'] == first_child_id), None)
                if first_child:
                    if 'parent_id' in block:
                        if 'parent_id' not in first_child:
                            first_child['parent_id'] = []
                        first_child['parent_id'].extend(block['parent_id'])
                        first_child['parent_id'] = list(set(first_child['parent_id']))  # 중복 제거

                    # BlockStatement에서 첫 번째 자식으로 body 전달
                    if 'body' in block:
                        if 'body' not in first_child:
                            first_child['body'] = []
                        first_child['body'].extend([item for item in block['body'][1:] if item != first_child_id])
                else:
                    print(f"경고: 첫 번째 자식 노드 {first_child_id}를 노드 목록에서 찾을 수 없습니다.")

                # BlockStatement를 부모로 가진 모든 노드들의 parent_id 업데이트
                for node in nodes:
                    if 'parent_id' in node and block_id in node['parent_id']:
                        node['parent_id'] = [first_child_id if pid == block_id else pid for pid in node['parent_id']]

            # BlockStatement 노드 제거
            nodes = [node for node in nodes if node['id'] != block_id]

            # 모든 자식들이 부모의 body에 있는지 확인
            ensure_child_in_parent_body(nodes)



        iteration += 1



    return nodes


def find_block_statements(nodes):
    return [node for node in nodes if node.get('type') == 'BlockStatement']

def get_first_child_id(block_node):
    if 'body' in block_node and block_node['body']:
        return block_node['body'][0].get('id') if isinstance(block_node['body'][0], dict) else block_node['body'][0]
    return None

def update_parent_body(nodes, old_id, new_id):
    for node in nodes:
        if 'body' in node:
            node['body'] = [
                {'id': new_id} if (item == old_id or (isinstance(item, dict) and item.get('id') == old_id))
                else item
                for item in node['body']
            ]

def update_child_parent_ids(nodes, old_parent_id, new_parent_id):
    for node in nodes:
        if 'parent_id' in node:
            node['parent_id'] = [new_parent_id if pid == old_parent_id else pid for pid in node['parent_id']]


def ensure_child_in_parent_body(nodes):
    for node in nodes:
        if 'parent_id' in node:
            for parent_id in node['parent_id']:
                parent = next((p for p in nodes if p['id'] == parent_id), None)
                if parent and 'body' in parent:
                    if node['id'] not in [item.get('id') if isinstance(item, dict) else item for item in parent['body']]:
                        parent['body'].append({'id': node['id']})