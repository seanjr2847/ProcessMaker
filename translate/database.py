import sqlite3

def query_database(table_name, column_name, condition_column, condition_value):
    """
    특정 테이블에서 조건에 맞는 단일 값을 조회하여 반환합니다.
    :param table_name: 조회할 테이블 이름
    :param column_name: 반환할 컬럼 이름
    :param condition_column: 조건을 적용할 컬럼 이름
    :param condition_value: 조건 값
    :return: 조회된 단일 값 또는 None (결과가 없는 경우)
    """
    db_name = 'translate.sqlite'
    try:
        # 데이터베이스 연결
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # SQL 쿼리 실행
        query = f"SELECT {column_name} FROM {table_name} WHERE {condition_column} = ?"
        cursor.execute(query, (condition_value,))
        
        # 결과 가져오기
        result = cursor.fetchone()
        
        # 연결 종료
        conn.close()
        
        # 결과 반환 (단일 값 또는 None)
        return result[0] if result else None
    
    except sqlite3.Error as e:
        print(f"데이터베이스 오류: {e}")
        return None
    except Exception as e:
        print(f"예외 발생: {e}")
        return None


def gen_query(type:str, query_params:str):
    """
    조회할 데이터 타입과 원하는 파라미터를 입력할 시, 조회결과를 반환해줍니다.
    """
    if type == 'commsg':
        table_name = 'TB_COMMSG_INFO'
        column_name = 'value'
        condition_column = 'key'
        condition_value = query_params
    elif type == 'comcode':
        table_name = 'comcode'
        column_name = 'value'
        condition_column = 'key'
        condition_value = query_params
    
    result = query_database(table_name, column_name, condition_column, condition_value)
    
    return result


print(gen_query('commsg','CME0002'))
