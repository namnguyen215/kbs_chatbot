
import pandas as pd  
import mysql.connector
from cbr_tieuhoa import TuVan


tv = TuVan()


stop = False
while stop==False:
    #Bắt đầu quá trình tư vấn
    start = tv.start_turn()


    if tv.id_question!='Q_error':
        tv.list_id_question.append(tv.id_question)

    # đưa ra câu hỏi , và list option:
    tv.get_list_answer()
    tv.get_cauHoi()
    cauhoi = tv.cauHoi
    list_answer = tv.list_option
    print('[CHATBOT]: '+ str(cauhoi))
    print(list_answer)
    

    #nhập input
    input_user = input("[USER]: ")


    if input_user.lower()=='stop':
        stop = True
        break
    
    # đưa ra chuẩn đoán, nếu chưa ra được chuẩn đoán thì đã cập nhật câu hỏi tiếp theo rồi

    chuanDoan = tv.process(input_user)
    if chuanDoan!= None:
        print(chuanDoan)
   