import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

database_username = 'root'
database_password = '12345678'
database_ip       = 'localhost'
database_name     = 'kbs_db'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

def get_danh_sach_benh():
    # chưa hiểu lắm
    query = "select * from benh"
    df = pd.read_sql_query(query, database_connection)
    return df

def get_id_benh_by_trieu_chung(trieu_chung):
    query = "select benh.id \
            from benh, trieuChung, trieuChungBenh \
            where benh.id = trieuChungBenh.idBenh \
                and trieuChung.id = của trieuChungBenh.idTrieuChung \
                and trieuChung.ten like '%{}%\
            order by trieuChungBenh.trongSo desc'".format(trieu_chung)
    print("Waiting for query...")
    results = database_connection.execute(text(query))
    return results
    # df = pd.read_sql_query(query, database_connection)
    # return df

def get_trieu_chung_by_benh(benhid: str):
    benhid = benhid.upper()
    query = "select trieuChung.ten \
            from benh, trieuChung, trieuChungBenh \
            where benh.id = trieuChungBenh.idBenh \
                and trieuChung.id = trieuChungBenh.idTrieuChung \
                and benh.id like '%{}%'".format(benhid)
    
    result = database_connection.execute(text(query))
    trieu_chung = result.mappings().all()
    trieu_chung_list = [x['ten'] for x in trieu_chung]
    return trieu_chung_list
# result = get_trieuchung_by_benh("B1")
# print(type(result))
# print(result)