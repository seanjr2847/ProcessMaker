from making_ast import nexa_to_js
from making_node import node_main
from modify.modify_type import modify_main
from make_diagram import assign_coordinates, make_diagram
from order.order_node import order_node
from test import validate_parent_relationships

def main():
	# 넥사크로 코드 (예시 input)
	nexacro_code = """
function fn_callBack(svcid,strErrCode,strErrMsg) 
{
	gf_showWaitImage(false);
	var sErrorcd  = "";
	var sErrormsg = "";
	
	if (strErrCode == -1000) {
		gf_sessionOut();
		return;
	} else if (strErrCode != 0) {
		gf_alertMessage( "CME0002", [strErrMsg] );
		return;
	} else {
		//조회처리
		if( svcid == "HREmpEduMngSel_sel" ) {
			//소속 정보 셋팅
			var objRetVal = new Array();
			var orgNm = "";
			CMOrgPop.edt_grpCd.value   = ds_eduInfo.getColumn(0,"GRP_CD");
			CMOrgPop.edt_hqCd.value    = ds_eduInfo.getColumn(0,"HQ_CD");
			CMOrgPop.edt_areaCd.value  = ds_eduInfo.getColumn(0,"AREA_CD");
			CMOrgPop.edt_brCd.value    = ds_eduInfo.getColumn(0,"BR_CD");
			CMOrgPop.edt_teamCd.value  = ds_eduInfo.getColumn(0,"TEAM_CD");
			objRetVal[0]     = ds_eduInfo.getColumn(0,"GRP_NM");
			objRetVal[1]     = ds_eduInfo.getColumn(0,"HQ_NM");
			objRetVal[2]     = ds_eduInfo.getColumn(0,"AREA_NM");
			objRetVal[3]     = ds_eduInfo.getColumn(0,"BR_NM");
			objRetVal[4]     = ds_eduInfo.getColumn(0,"TEAM_NM");
			
			//조직명설정
			var j = 0;
			for( var i=0; i<5; i++ ) {
				if(! gf_isNull( objRetVal[j] ) ) {
					orgNm = orgNm + objRetVal[j] + ">>";
				}
				j++;
			}	
			orgNm = orgNm.substring( 0, (orgNm.length - 2 ) );
			CMOrgPop.edt_orgNm.value = orgNm;
		
		}else if ( svcid == "HREduMngDtlInfo_ins" ) {
			gf_alertMessage("CMI0002");
			this.close(true);
		}
		
	}
}

"""

	#넥사크로 코드를 ast로 변환합니다.
	ast = nexa_to_js(nexacro_code)

	#해당 함수를 한글로 번역합니다. (미완성)


	#함수 이름을 추출합니다. (미완성)
	function_name = "fn_callBack"

	#ast를 노드의 형태로 반환합니다.
	nodes = node_main(ast)

	#노드 간략화 시킴
	modified_nodes = modify_main(nodes, function_name)


	#노드 정렬함
	ordered_nodes = order_node(modified_nodes)
	print(ordered_nodes)

	node_coordinates = assign_coordinates(ordered_nodes)

	test = make_diagram(node_coordinates)

	exec(test)

main()