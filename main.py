from py_mini_racer import py_mini_racer
from making_js import nexa_to_js



# 넥사크로 코드 (예제)
nexacro_code = """
function cmb_cntrKindCd_onitemchanged(obj:Combo, e:ItemChangeEventInfo)
{
    //제휴사정보 
    if (gf_trim(obj.value) == "") {
        ds_codeAfcrNo.filter("AFCR_NM == '전체'");        
    } else if (gf_trim(obj.value) == "01") {
        ds_codeAfcrNo.filter("AFCR_NM == '전체' || AFCR_CLSF_CD == '10'");        
    } else {
        ds_codeAfcrNo.filter("AFCR_NM == '전체' || AFCR_CLSF_CD == '20'");
    }
    cmb_afcrNo.index = 0;
}
"""
ast = nexa_to_js(nexacro_code)


print(ast)

#print(ast)
#print(type(ast))
# JSON 형식으로 변환
#nodes_json = [node.to_dict() for node in nodes]
#print(json.dumps(nodes_json, indent=2, ensure_ascii=False))





##print(dd)
