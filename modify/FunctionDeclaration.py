from typing import Dict, List, Any

def format_params(params):
    return ', '.join(param['name'] for param in params if 'name' in param)

def FunctionDeclaration(node: Dict[str, Any], function_name: str) -> Dict[str, Any]:
    
    if isinstance(node.get('parent_id'), list):
        node['parent_id'].clear()

    # 각 아래조건은 특수함수고, 현재로선 대응하지 않음. 향후 대비하기 위해서 로그만 남겨놓는다.
    if node.get('generator') == False:
        del node['generator']
    else:
        print("함수 종류가 예상과 다름!! generator임")
        return None
    
    if node.get('async') == False:
        del node['async']
    else:
        print("함수 종류가 예상과 다름!! async임")
        return None
    
    if node.get('expression') == False:
        del node['expression']
    else:
        print("함수 종류가 예상과 다름!! expression임")
        return None

    # content 생성 부분
    params = format_params(node.get('params', []))
    
    body = node.get('body', [])
    body_content = ''
    if body and isinstance(body[0], dict) and body[0].get('type') == 'BlockStatement':
        # 실제 구현에서는 BlockStatement의 내용을 처리해야 합니다.
        # 여기서는 간단히 빈 중괄호로 표현합니다.
        body_content = '{}'
    
    # function_name을 함수 이름으로 사용
    node['content'] = f"function {function_name}({params}) {body_content}"
    
    # 불필요한 키 제거
    keys_to_remove = ['body', 'params']
    for key in keys_to_remove:
        if key in node:
            del node[key]

    return node