from making_ast import nexa_to_js
from making_node import node_main
from modify_node import modify_main



# 넥사크로 코드 (예시 input)
nexacro_code = """
function fn_callBack(svcid, strErrCode, strErrMsg) 
{
	//alert(" strErrCode : " + strErrCode);
	var sErrorcd  = "";
	var sErrormsg = "";

	gf_showWaitImage(false);
	
	//세션체크
	if (strErrCode == -1000) {
		gf_sessionOut();
		return;
	}
	
	if (strErrCode != 0) {
		//alert("Error : " + strErrMsg);
		gf_alertMessage( "CME0002", [strErrMsg] );	
		return;
	} else {
		if(svcid == "COMBO_SET") {
			gf_insertDefaultRowForCombo(ds_codeCntrKindCd, "선택", "", 0, "CD_NM", "DTL_CD");	//계약종류
			ds_codeCntrKindCd.filter("DTL_CD==''||DTL_CD=='01'||DTL_CD=='02'");
			cmb_cntrKindCd.index = 0;

			gf_insertDefaultRowForCombo(ds_codeCntrStCd, "선택", "", 0, "CD_NM", "DTL_CD");		//계약상태
			
		//제휴사정보 구분코드 조회
		} else if (svcid == "CTGaAfcrMng_sel") {
			gf_insertDefaultRowForCombo(ds_codeAfcrNo, "전체", "", 0, "AFCR_NM", "AFCR_CLSF_CD");
			ds_codeAfcrNo.filter("AFCR_NM == '전체'");
			
			cmb_afcrNo.index = 0;
			return;
		} else if (svcid == "CTCntrStHis_sel01") {
			if (ds_cntrList.rowcount < 1 ) {
				gf_messageCtl("CMI0007");
			} else {
				gf_messageCtl("CMI0009");
			}
			return;
		} else if (svcid == "CTCntrStHis_sel02") {
			if (ds_cntrStList.rowcount < 1 ) {
				gf_messageCtl("CMI0007");
			} else {
				gf_messageCtl("CMI0009");
			}
			return;
		} else if (svcid == "CTCntrStHis_exe") {
			if (ds_cntrStList.rowcount < 1 ) {
				gf_messageCtl("CMS0006");
			} else {
				gf_messageCtl("CMI0002");
			}
			return;			
		
		//엑셀다운로드
		} else if (svcid == "ExlDownloadSC_sel") {
			gf_showWaitImage(true);
			gf_exportExcel(grd_cntrStList, CMNavi.stc_Navi.text + "_" + gf_today() + ".xls", this.titletext);
			gf_showWaitImage(false);
		}
	}
}
"""




#넥사크로 코드를 ast로 변환합니다.
ast = nexa_to_js(nexacro_code)

#ast를 노드의 형태로 반환합니다.
nodes = node_main(ast)

#노드 간략화 시킴
modified_nodes = modify_main(nodes)
#

#print(modified_nodes)


#테스트 타입 추출용
#test1 =  [node_test.get('type') for node_test in node_test]

