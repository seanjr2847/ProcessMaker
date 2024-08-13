from .BlockStatement import order_BlockStatement

def update_parent_id(dict_list):
    if len(dict_list) < 2:
        return dict_list  # 리스트에 딕셔너리가 2개 미만이면 변경 없이 반환

    # 첫 번째 딕셔너리의 'id' 값 가져오기
    first_id = dict_list[0].get('id')

    if first_id is not None:
        # 두 번째 딕셔너리의 'parent_id' 리스트에 첫 번째 딕셔너리의 'id' 값 추가
        if 'parent_id' not in dict_list[1]:
            dict_list[1]['parent_id'] = []
        dict_list[1]['parent_id'].append(first_id)

    # 첫 번째 딕셔너리에 'body' 키 추가
    dict_list[0]['body'] = [{
        "type": dict_list[1].get('type', ''),
        "id": dict_list[1].get('id', '')
    }]

    return dict_list




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
    result = update_parent_id(nodes)
    result = order_ifStatement(result)
    result = order_BlockStatement(result)
    return result