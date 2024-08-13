def order_BlockStatement(nodes):
    nodes_to_remove = []
    for node in nodes:
        if node['type'] == 'BlockStatement' and 'body' in node:
            block = node
            body_items = block['body']
            
            if body_items:
                # Update parent's body to point to the first node of the chain
                for parent in nodes:
                    if 'body' in parent:
                        parent['body'] = [body_items[0] if item.get('id') == block['id'] else item for item in parent['body']]
                
                # Create a chain of all items in the body
                for i, body_item in enumerate(body_items):
                    current_node = next((n for n in nodes if n['id'] == body_item['id']), None)
                    if current_node:
                        if i == 0:
                            current_node['parent_id'] = block['parent_id']
                        else:
                            current_node['parent_id'] = [body_items[i-1]['id']]
                        
                        # Preserve the original body if it exists
                        original_body = current_node.get('body', [])
                        
                        # If this is not the last item, add the next item to its body
                        if i < len(body_items) - 1:
                            next_item = body_items[i+1]
                            if next_item['id'] not in [item['id'] for item in original_body]:
                                current_node['body'] = [next_item] + original_body
                        else:
                            current_node['body'] = original_body

                nodes_to_remove.append(block['id'])

    # Remove the BlockStatements
    nodes = [n for n in nodes if n['id'] not in nodes_to_remove]

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
    parent_node = next((node for node in nodes if node['id'] == new_parent_id), None)
    if not parent_node:
        print(f"Warning: Parent node {new_parent_id} not found.")
        return

    children = []
    for node in nodes:
        if 'parent_id' in node and old_parent_id in node['parent_id']:
            # Update parent_id
            node['parent_id'] = [new_parent_id if pid == old_parent_id else pid for pid in node['parent_id']]
            children.append(node['id'])

    # Sort children based on their original order in the old parent's body
    old_parent = next((node for node in nodes if node['id'] == old_parent_id), None)
    if old_parent and 'body' in old_parent:
        children.sort(key=lambda x: old_parent['body'].index(x) if x in old_parent['body'] else float('inf'))

    # Update parent's body
    if children:
        parent_node['body'] = children

    # Update parent-child relationships
    for i, child_id in enumerate(children):
        child_node = next((node for node in nodes if node['id'] == child_id), None)
        if child_node:
            if i == 0:
                # First child becomes the new parent for the rest
                child_node['parent_id'] = parent_node['parent_id']
                child_node['body'] = children[1:]
            else:
                # Other children get the first child as their parent
                child_node['parent_id'] = [children[0]]

    # Remove body from old parent
    if old_parent:
        old_parent.pop('body', None)



def ensure_child_in_parent_body(nodes):
    for node in nodes:
        if 'parent_id' in node:
            for parent_id in node['parent_id']:
                parent = next((p for p in nodes if p['id'] == parent_id), None)
                if parent and 'body' in parent:
                    if node['id'] not in [item.get('id') if isinstance(item, dict) else item for item in parent['body']]:
                        parent['body'].append({'id': node['id']})