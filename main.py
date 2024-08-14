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
	
		// 조회 성공에 대한 Callback 처리.
		if (svcid == "HREduTargSel_sel") {	
			if (ds_eduInfo.rowcount < 1) {
				gf_messageCtl("CMI0007");
				return;
			}  else {
				gf_messageCtl("CMI0009");
			}
			return;
			
		// 콤보 처리
		} else if ( svcid == "COMBO" ) {
			gf_insertDefaultRowForCombo( ds_eduCat, "전체", "", 0, "CD_NM", "DTL_CD");	//교육구분
			cmb_eduCat.index = 0;
			
			// 기준조직정보 조회
			fn_getStdOrgInfo();
			
			return;
		// 기준조직정보 조회
		} else if(svcid == "ALStdOrgInfo_sel") {
			// 권한이 전체인경우 그룹변경가능, 이외에는 선택불가
			if(gds_userInfos.getColumn(0, "AUTH_LVL_CD") == "10"){
				cmb_stdOrg.value = gf_getStdOrgCd();
				cmb_stdOrg.enable = true;
			} else {
				cmb_stdOrg.value = gds_userInfos.getColumn(0, "GRP_CD");
				cmb_stdOrg.enable = false;
			}
			
			//자동 조회
			//btn_CQ_onclick();
			
			return;		
		// 메인 재승인요청처리
		} else if ( svcid == "HRRctAppInfoReApprUpt" ) {
			gf_alertMessage( "CMI0001" ); // 처리완료	
			//btn_CQ_onclick(); // 재조회
		}
	}
}
"""

	#넥사크로 코드를 ast로 변환합니다.
	ast = nexa_to_js(nexacro_code)


	#함수 이름을 추출합니다. (미완성)
	function_name = "fn_callBack"

	#ast를 노드의 형태로 반환합니다.
	nodes = node_main(ast)
	print(nodes)
	#노드 간략화 시킴
	modified_nodes = modify_main(nodes, function_name)


	#노드 정렬함
	ordered_nodes = order_node(modified_nodes)
	

	node_coordinates = assign_coordinates(ordered_nodes)

	test = make_diagram(node_coordinates)

	exec(test)

main()