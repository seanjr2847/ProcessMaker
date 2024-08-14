import py_mini_racer
import re

def open_esprima():
    """
    자바스크립트를 파이썬 환경에서 구동시키기 위한 esprima 코드를 실행시킵니다.    
    """
    with open('esprima.js', 'r', encoding='utf-8') as file:
        esprima_code = file.read()

    # JavaScript 코드를 AST로 변환하는 함수 정의
    parse_code_js = """
    function parseCode(js_code) {
        return esprima.parseScript(js_code, { tolerant: true, range: true });
    }
    """
    return esprima_code, parse_code_js

def nexa_js_convert(code:str) -> str:
    """
    넥사크로 format에서 js와 다른 분들을 제외합니다.
    """
    # 함수 선언부 변환
    code = re.sub(r'function\s+(\w+)\s*\((.*?)\)', lambda m: f"function {m.group(1)}({', '.join(param.split(':')[0].strip() for param in m.group(2).split(','))})", code)
    
    # gf_trim 함수를 임시로 String.prototype.trim()으로 대체
    code = code.replace('gf_trim(', '(')
    
    # 객체 접근 방식 변환 (예: CMCalMonth01.med_cal.value -> CMCalMonth01["med_cal"]["value"])
    code = re.sub(r'(\w+)\.(\w+)\.(\w+)', r'\1["\2"]["\3"]', code)
    
    # ds_input.setColumn을 가상의 함수로 변환
    code = re.sub(r'ds_input\.setColumn\s*\(\s*(\d+)\s*,\s*"([^"]*)"\s*,\s*([^)]*)\)', r'setColumn(\1, "\2", \3)', code)
    
    # getHREmpEduMngSel 함수 호출을 가상의 함수로 변환
    code = code.replace('getHREmpEduMngSel()', 'getHREmpEduMngSel()')
    
    # ds_input.addRow()를 가상의 함수로 변환
    code = code.replace('ds_input.addRow()', 'addRow()')
    
    return code

def nexa_to_js(nexacro_code: str) -> dict:
    """
    넥사크로 함수를 esprima 추상 구문 트리로 변환시킵니다.
    """
    try:
        js_code = nexa_js_convert(nexacro_code)
        
        esprima_code, parse_code_js = open_esprima()

        # py_mini_racer를 사용하여 Esprima 로드 및 JavaScript 코드 실행
        ctx = py_mini_racer.MiniRacer()
        ctx.eval(esprima_code)
        ctx.eval(parse_code_js)

        # dict
        ast = ctx.call("parseCode", js_code)
        return ast
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}