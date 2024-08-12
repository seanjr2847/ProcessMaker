from typing import List, Dict, Any, Tuple

def assign_coordinates(nodes):
    node_dict = {node['id']: node for node in nodes}
    
    def get_children(node_id):
        node = node_dict[node_id]
        children = []
        if 'body' in node:
            if isinstance(node['body'], list):
                children = [item['id'] for item in node['body'] if isinstance(item, dict) and 'id' in item]
            elif isinstance(node['body'], dict) and 'id' in node['body']:
                children = [node['body']['id']]
        return children
    
    def get_all_children(node_id, visited=None):
        if visited is None:
            visited = set()
        if node_id in visited:
            return []
        visited.add(node_id)
        children = get_children(node_id)
        all_children = children[:]
        for child in children:
            all_children.extend(get_all_children(child, visited))
        return all_children
    
    # Find root node
    all_nodes = set(node_dict.keys())
    child_nodes = set()
    for node_id in all_nodes:
        child_nodes.update(get_children(node_id))
    roots = list(all_nodes - child_nodes)
    if not roots:
        roots = [nodes[0]['id']]
    
    # Calculate depths
    depths = {}
    def calculate_depth(node_id, depth=0, visited=None):
        if visited is None:
            visited = set()
        if node_id in visited:
            return
        visited.add(node_id)
        depths[node_id] = depth
        for child in get_children(node_id):
            calculate_depth(child, depth + 1, visited)
    
    for root in roots:
        calculate_depth(root)
    
    def assign_xy(node_id, x=0, visited=None):
        if visited is None:
            visited = set()
        if node_id in visited:
            return x
        visited.add(node_id)
        
        node = node_dict[node_id]
        y = depths[node_id]
        
        # Ensure unique x position for each node at the same depth
        while (y, x) in [(depths[n], node_dict[n]['XY'][0]) for n in node_dict if 'XY' in node_dict[n]]:
            x += 1
        
        node['XY'] = (x, y)
        
        children = get_children(node_id)
        for child in children:
            x = assign_xy(child, x, visited)
        
        return x + 1
    
    for root in roots:
        assign_xy(root)
    
    return nodes



def make_diagram(input_list: List[Dict[str, Any]]) -> str:
    # Initialize code
    results = ["""
import drawpyo
import os

file = drawpyo.File()
file.file_path = "D://Projects//ProcessMaker"
file.file_name = "111.drawio"
page = drawpyo.Page(file=file)

row_h = 120
col_pos = page.width / 2 - 200
col_h = 200 
row_margin = 60

# Create template objects
process = drawpyo.diagram.object_from_library(
    library="flowchart",
    obj_name="process",
    width=140,
    height=70,
)

decision = drawpyo.diagram.object_from_library(
    library="flowchart",
    obj_name="decision",
    width=120,
    height=70,
)
"""]

    def create_node(node_id: str, node_type: str, content: str, x: int, y: int) -> str:
        """Create a node based on its type and properties."""
        if node_type == "function":
            return f'''
{node_id} = drawpyo.diagram.object_from_library(
    library="flowchart", obj_name="terminator", value={repr(content)}, page=page
)
{node_id}.center_position = (col_pos + {x} * col_h, row_margin + row_h * {y})
'''
        elif node_type == "decision":
            template = "decision"
        else:
            template = "process"
        
        return f'''
{node_id} = drawpyo.diagram.Object(
    template_object={template},
    value={repr(content)},
    page=page,
)
{node_id}.center_position = (col_pos + {x} * col_h, row_margin + row_h * {y})
'''

    # Create nodes
    for input_data in input_list:
        try:
            node_id = input_data['id']
            node_type = input_data['type']
            content = input_data.get('content', "")
            x, y = input_data.get('XY', (0, 0))
            results.append(create_node(node_id, node_type, content, x, y))
        except KeyError as e:
            print(f"Error: Missing required key {e} in input data")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    # Create edges
    for input_data in input_list:
        source_id = input_data.get('id')
        
        # Create edges for parent-child relationships
        if 'body' in input_data and isinstance(input_data['body'], list):
            for i, child in enumerate(input_data['body']):
                if isinstance(child, dict) and 'id' in child:
                    target_id = child['id']
                    edge_code = f'''
edge_{source_id}_{target_id} = drawpyo.diagram.Edge(
    source={source_id},
    target={target_id},
    page=page,
)
'''
                    results.append(edge_code)
        
        # Create edges for parent_id relationships
        parent_ids = input_data.get('parent_id', [])
        for parent_id in parent_ids:
            if parent_id != source_id:  # Avoid self-referencing edges
                edge_code = f'''
edge_{parent_id}_{source_id} = drawpyo.diagram.Edge(
    source={parent_id},
    target={source_id},
    page=page,
)
'''
                results.append(edge_code)

    # Write the file
    results.append("""
# Write the file
file.write()""")

    return "".join(results)