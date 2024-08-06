import py_mini_racer

def open_esprima():
    with open('esprima.js', 'r', encoding='utf-8') as file:
        esprima_code = file.read()

    # JavaScript 코드를 AST로 변환하는 함수 정의
    parse_code_js = """
    function parseCode(js_code) {
        return esprima.parseScript(js_code, { tolerant: true, range: true });
    }
    """
    return esprima_code, parse_code_js

def nexa_js_convert(nexacro_code):
    # 넥사크로 코드를 JavaScript로 변환 (예제 변환)
    js_code = nexacro_code.replace(":Combo", "").replace(":ItemChangeEventInfo", "")
    return js_code

def nexa_to_js(nexacro_code):
    esprima_code, parse_code_js = open_esprima()

    js_code = nexa_js_convert(nexacro_code)

    # py_mini_racer를 사용하여 Esprima 로드 및 JavaScript 코드 실행
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(esprima_code)
    ctx.eval(parse_code_js)


    #dict
    ast = ctx.call("parseCode", js_code)
    return ast