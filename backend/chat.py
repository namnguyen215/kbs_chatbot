import db
from cbr_tieuhoa import TuVan

class Chat():
    # tv = TuVan()
    def __init__(self):
        #để t add code lên git
        self.list_question = {"type":"","benh":"","question":[]}
        self.list_option= ["Mô tả","Triệu chứng", "Nguyên nhân", "Cách phòng ngừa"]
        self.pick = 0
        self.tv = None
    
    def hello(self):
        ops =[]
        ops.append("Xem thông tin các bệnh")
        ops.append("Tư vấn bệnh")
        return ops
    
    def xu_li_xem_thong_tin(self, msg):
        if self.list_question["benh"] == "" :
            self.list_question["benh"] = msg
            print("benh: ", self.list_question["benh"])
        else:                     
            pass
        return self.list_option            
            
        
    def xu_li_tu_van(self, msg):
        list_answer = []
        if msg == "Tư vấn bệnh":
            self.list_question["benh"] = "Tư vấn bệnh"
        else:
            self.tv.get_list_answer()
            list_answer = self.tv.list_option                
        if self.tv.id_question!='Q_error' :
            self.tv.list_id_question.append(self.tv.id_question)        
        return list_answer  
    
    
    
    def get_list_disease(self):
        df = db.get_danh_sach_benh()
        return df
    
    def get_trieu_chung_by_benh(self, benhid):
        trieu_chung = db.get_trieu_chung_by_benh(benhid)
        result = self.handle_list_return(trieu_chung)
        return result
    
    def handle_list_return(self, list_return:list):
        result = ""
        for item in list_return:
            result += "\n"+"- "+item 
        return result
    
    def split_text(self, text):
        ls_split = text.split("|")
        # print(text)
        result = self.handle_list_return(ls_split)
        return result
    
    def get_option(self, msg):
        #truyen vao input la cau tra loi
        ops = []

        if msg == 'Xem thông tin các bệnh' and self.pick == 0:
            self.list_question['type'] = msg
            ops= list(self.get_list_disease()['ten'])
            self.pick = 1
            return ops
        elif msg == 'Tư vấn bệnh' and self.pick == 0:
            print("tuvan")
            self.tv = TuVan()
            self.list_question['type'] = msg
            self.pick = 1
            self.tv.start_turn()
            ops = self.xu_li_tu_van(msg)
            print(ops)
            return ops
        
        if self.list_question["type"] == "Xem thông tin các bệnh":
            ops = self.xu_li_xem_thong_tin(msg)
        elif self.list_question["type"] == "Tư vấn bệnh":
            ops = self.xu_li_tu_van(msg)
        
        print(ops)
        return ops
    
    def get_response(self, msg):
        #truyen vao input la cau tra loi
        if self.list_question["type"] == 'Xem thông tin các bệnh' and self.list_question["benh"] != "":
            df = self.get_list_disease()
            df = df[df['ten'] == self.list_question["benh"]]
            if msg == "Mô tả":
                return df['moTa'].values[0]
            elif msg == "Triệu chứng":
                return self.get_trieu_chung_by_benh(df['id'].values[0])
            elif msg == "Nguyên nhân":
                return self.split_text(df['nguyenNhan'].values[0])
            elif msg == "Cách phòng ngừa":
                return self.split_text(df['nganNgua'].values[0])            
        elif msg == "Tư vấn bệnh":
            return "Bạn đã chọn: " + msg;     
        elif self.list_question["type"] == 'Tư vấn bệnh' and self.list_question["benh"] != "":
            print(self.list_question)
            chuanDoan = self.tv.process(msg)
            print(self.tv.id_question)
            print(self.tv.dict_cbr)
            print("Message: ", msg)
            print(self.tv.list_id_question)
            self.tv.get_cauHoi()
            cauhoi = self.tv.cauHoi            
            print("cauhoi: ", cauhoi)
            if chuanDoan!= "Error" and chuanDoan!= None:
                return (chuanDoan)    
            else:        
                return cauhoi
        return "Bạn đã chọn: " + msg ;
    
