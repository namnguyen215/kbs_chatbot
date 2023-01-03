import pandas as pd  
import mysql.connector

db =  mysql.connector.connect(user = 'root', database = 'kbs_db', passwd= '12345678')

class TuVan():
    def __init__(self ):
        self.dict_cbr = dict()
        self.df_benh = pd.read_sql_query('select id, ten, moTa, nguyenNhan, nganNgua from benh', con= db)
        self.df_trieuChung = pd.read_sql_query('select id, ten,idCauHoi from trieuchung', con= db)
        self.df_cauHoi = pd.read_sql_query('select id, noiDung from cauHoi', con= db)
        self.df_trieuChungBenh =  pd.read_sql_query('select idBenh, idTrieuChung,trongSo from trieuchungbenh', con= db)
        self.df_doTuongDong = pd.read_sql_query('select idTrieuChung1, idTrieuChung2, heSo from dotuongdong', con= db)
        self.list_id_question =[]
        self.dict_cbr = dict()
        self.new_turn = True
        self.id_question = 'Q1'
        self.cauHoi = ''
        self.list_option = []
        self.list_error = []

    def finish_turn(self):
        self.new_turn =True
      
    def start_turn(self):
        start_tuvan = None
        if  self.new_turn == True:
            self.new_turn = False
            self.list_id_question = []
            self.dict_cbr = dict()
            self.id_question = 'Q1'
            self.cauHoi = ''
            self.list_option = []
            self.list_error = []
            start_tuvan = ' Hãy trả lời các câu hỏi sau chúng tôi sẽ cho bạn lời tư vấn tốt nhất'
        return start_tuvan
        

    def process(self, input_user):
        # print(input_user)
        # if input_user=='Tư vấn bệnh':
        #     self.finish_turn()
        #     return None
        if(self.correct_input(input_user)=='Error'):
            self.id_question = 'Q_error'
            self.list_error.append(1)
            if(len(self.list_error)>1):
                self.finish_turn()
            return 'Error'
        else:
            self.list_error = []
            if input_user!='Tiếp tục' and input_user !='Kết thúc':
                if self.new_turn== False:
                    dict_trieuchungbenh_dangXet = self.get_TrieuChungBenh_đangXet()
                    id_trieuchung_user = self.get_idTrieuCHung_user(input_user)
                    dict_doTuongDong = self.get_doTuongDong(id_trieuchung_user)
                    self.get_diemCBR_moiTrieuChung( id_trieuchung_user, dict_doTuongDong, dict_trieuchungbenh_dangXet)
                    dict_allCBR = self.get_diemCBR_AllTrieuChung_daXet()
                    chuanDoan  = self.get_chuanDoan(dict_allCBR)
                    if chuanDoan == None:
                        id_benh_nghiNgo = self.tim_idbenh_nghiNgo(dict_allCBR)
                        list_id_trieuchung_daXet = self.get_all_idtrieuChunng_daXet()
                        id_trieuChung_tiepTheo = self.get_idtrieuChung_tiepTheo(id_benh_nghiNgo, list_id_trieuchung_daXet)
                        self.get_idcauHoi_by_idTrieuChung(id_trieuChung_tiepTheo)
                        self.get_cauHoi()
                        return self.cauHoi
                    return chuanDoan
            
    def correct_input(self,input_user):
       
        self.get_list_answer()
        list_answer = self.list_option
        for i in list_answer:
            if i == 'Tiếp tục':
                if input_user=='Tiếp tục':
                    self.id_question = self.list_id_question[-1]
                    return input_user
            elif i == 'Kết thúc':
                if input_user=='Kết thúc':
                    self.finish_turn()
                    return input_user
            if input_user == i:
                return input_user
        return 'Error'
    #lây danh sách các đap án triệu chứng của câu hỏi
    def get_list_answer(self):
        if(self.id_question!='Q_error'):
            list_answer = list(self.df_trieuChung[self.df_trieuChung['idCauHoi'].str.upper()==self.id_question]['ten'])
            self.list_option = list_answer
        else:
            self.list_option = ['Tiếp tục', 'Kết thúc']
        
    def get_cauHoi(self):
        if(self.id_question!='Q_error'):
            self.cauHoi = self.df_cauHoi[self.df_cauHoi['id']==self.id_question]['noiDung'].values[0]
        else:
            self.cauHoi = 'Chatbot không hiểu. Vui lòng lựa chọn lại . Bạn có muốn tiếp tục ?'
    #LÂY ID TRIỆU CHỨNG BỞI INPUT
    def get_idTrieuCHung_user(self,input_user):
        id_trieuchung = list(self.df_trieuChung[self.df_trieuChung['ten']==input_user]['id'].values)[0]
        return id_trieuchung
    
        #LẤY THÔNG TIN TRIỆU CHỨNG ĐANG XÉT
    def get_TrieuChungBenh_đangXet(self):
        dict_trieuchungbenh= dict()
        list_id_trieuchung = self.df_trieuChung[self.df_trieuChung['idCauHoi']==self.id_question]['id'].values
        for i in list_id_trieuchung:
        
            for j in range(self.df_trieuChungBenh.shape[0]):
                    if self.df_trieuChungBenh['idTrieuChung'].iloc[j] ==i:
                        if self.df_trieuChungBenh['idBenh'].iloc[j] not in list(dict_trieuchungbenh.keys()):
                            dict_trieuchungbenh[self.df_trieuChungBenh['idBenh'].iloc[j]] = {self.df_trieuChungBenh['idTrieuChung'].iloc[j]:self.df_trieuChungBenh['trongSo'].iloc[j]}
                        else :
                            dict_trieuchungbenh[self.df_trieuChungBenh['idBenh'].iloc[j]].update({self.df_trieuChungBenh['idTrieuChung'].iloc[j]:self.df_trieuChungBenh['trongSo'].iloc[j]})
            
        return dict_trieuchungbenh

        # LẤY ĐỘ TƯƠNG ĐỒNG CỦA TRIỆU CHỨNG ĐANG XÉT VỚI CÁC TRIỆU CHỨNG CÙNG LOẠI TRONG CSDL
    def get_doTuongDong(self,id_trieuchung_user):
        df = self.df_doTuongDong[(self.df_doTuongDong['idTrieuChung2']==id_trieuchung_user)| (self.df_doTuongDong['idTrieuChung1']==id_trieuchung_user)]
        dict_doTuongDong = {id_trieuchung_user: {}}
        for i in range(df.shape[0]):
            if df['idTrieuChung1'].iloc[i]==id_trieuchung_user:
                dict_doTuongDong[id_trieuchung_user].update({df['idTrieuChung2'].iloc[i]: df['heSo'].iloc[i]})
            if df['idTrieuChung2'].iloc[i]==id_trieuchung_user:
                dict_doTuongDong[id_trieuchung_user].update({df['idTrieuChung1'].iloc[i]: df['heSo'].iloc[i]})
        dict_doTuongDong[id_trieuchung_user].update({id_trieuchung_user:1})
        return  dict_doTuongDong

    #Tính sự quan trọng của trieu chứng đang xét với các case bênh trong csdl
    def get_diemCBR_moiTrieuChung(self ,id_trieuchung_user, dict_doTuongDong,dict_trieuchungbenh):

        df_tongHeSo = self.df_trieuChungBenh.groupby('idBenh').sum()
        for i in list(dict_doTuongDong[id_trieuchung_user].keys()):
            dict1_tmp = dict_doTuongDong[id_trieuchung_user]
            for j in list(dict_trieuchungbenh.keys()):
                dict2_tmp = dict_trieuchungbenh[j]
                for k in list(dict_trieuchungbenh[j].keys()):
                    if k==i:
                        result =round((dict1_tmp[i]*dict2_tmp[k])/int(df_tongHeSo[df_tongHeSo.index==j].values[0]),4)
                        if j not in list(self.dict_cbr.keys()):
                            self.dict_cbr[j]= {k: result}
                        else:
                            self.dict_cbr[j].update({k: result}) 
        # self.dict_cbr = dict_cbr

    #Tính điểm cbr của các triệu chứng đã xét với các case bệnh
    def get_diemCBR_AllTrieuChung_daXet(self):
        dict_allCBR = dict()
        for i in list(self.dict_cbr.keys()):
            list1 = list(self.dict_cbr[i].values())
            total_cbr = sum(list1)
            dict_allCBR[i]=total_cbr
        return dict_allCBR

    #Tìm ra id benh nghi ngờ
    def tim_idbenh_nghiNgo(self,dict_allCBR):
        id_benh = list(dict_allCBR.keys())[list(dict_allCBR.values()).index(max(dict_allCBR.values()))]
        return id_benh

    # lấy ra list các id_trieuchung từ các list id câu hỏi đã hỏi=> list triệu chứng đã xét
    def get_all_idtrieuChunng_daXet(self):
        list_id_trieuchung =[]
        for id_question in self.list_id_question:
            list_id_trieuchung= list_id_trieuchung + list(self.df_trieuChung[self.df_trieuChung['idCauHoi'].str.upper()==id_question]['id'])
        return list_id_trieuchung

    # tim ra  id triệu chứng quan trọng tiếp theo của bệnh nghi ngờ
    def get_idtrieuChung_tiepTheo(self,id_benh,list_id_trieuchung_daXet):
        id_trieuChung_quantrong = ''
        result_heso =0
        df_trieuChungBenh1 = self.df_trieuChungBenh.copy()
        df = df_trieuChungBenh1[df_trieuChungBenh1['idBenh']==id_benh].reset_index()
        df1 = df.copy()
        for i in range(df.shape[0]):
            if df['idTrieuChung'].iloc[i]  in list_id_trieuchung_daXet:
                df1.drop(df1[df1['idTrieuChung']==df['idTrieuChung'].iloc[i]].index.values[0], axis=0, inplace=True)
            else:
                result_heso = max(list(df1['trongSo']))
        id_trieuChung_quantrong = list(df1[df1['trongSo']==result_heso]['idTrieuChung'])[0]
        return id_trieuChung_quantrong
    
      # lấy id câu hỏi bởi id triệu chứng
    def get_idcauHoi_by_idTrieuChung(self,idTrieuChung):
        self.id_question= self.df_trieuChung[self.df_trieuChung['id']==idTrieuChung]['idCauHoi'].values[0]
        

    def get_chuanDoan(self,dict_allCBR):
        chuanDoan = None
    
        if len(self.list_id_question)==16:
            max_cbr = max(list(dict_allCBR.values()))
            self.finish_turn()

            if(max_cbr<0.9):
                chuanDoan = '[CHATBOT]: Chưa đủ các triệu chứng rõ ràng để chatbot chuẩn đoán bệnh cho bạn trong phạm vi của chúng tôi' 
            else:
                id_benhChuanDoan = self.tim_idbenh_nghiNgo(dict_allCBR)
                chuanDoan = '[CHATBOT:]' +'Bạn đang có dấu hiệu của bệnh'+ str(list(self.df_benh['ten'].values)[0])
              
        elif len(self.list_id_question)<=16:
            max_cbr = max(list(dict_allCBR.values()))
            if max_cbr<0.9:
                self.new_turn = False
                chuanDoan = None
                # if self.id_question != 'Q1':
                #     self.list_id_question.append(self.id_question)
                
            else:
                id_benhChuanDoan = self.tim_idbenh_nghiNgo(dict_allCBR)
                chuanDoan = '[CHATBOT:]' +'Bạn đang có dấu hiệu của bệnh'+ str(list(self.df_benh[self.df_benh['id']==id_benhChuanDoan]['ten'].values)[0])
                self.finish_turn()
        return  chuanDoan


