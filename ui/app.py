from tkinter import *
from turtle import width
import sys
sys.path.insert(0, './backend')
# from backend.chat import Chat
import chat

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:
    # chat = Chat()
    bot_name = ""
    chat = chat.Chat()
    def __init__(self):
        self.window = Tk()
        self.bot_name = "Sam"
        self._setup_main_window()
        
    def run(self):
        self.window.mainloop()
        
    def _insert_welcome(self, msg, sender):
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        #bot relpy after 500 ms
        # self.text_widget.insert(END, "\n")
        self.text_widget.see(END)

    
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=490, height=600, bg=BG_COLOR, pady=5)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=15, pady=5, wrap=WORD)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=1)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
     
        #show welcome message
        self._insert_welcome("Chào bạn, mình là Sam - chuyên gia tiêu hóa của bạn", self.bot_name)
        self._insert_welcome("Bạn hãy lựa chọn thông tin muốn tư vấn nhé!", self.bot_name)
        self._show_route("welcome")
        # self._insert_message("welcome", self.bot_name)
     
    def _show_route(self, route):
        ops = self.chat.hello()
        for op in ops:
            option_button = Button(text = op, width = 30, 
                            activebackground = '#d88a6c',
                            highlightcolor = '#f2ba9c',
                            justify= LEFT,
                            command= lambda op=op :self._select_option(op))
            self.text_widget.window_create("end", window=option_button)
            self.text_widget.insert(END,"\n")     
     
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        #bot relpy after 500 ms
        self.text_widget.after(500, lambda: self._bot_reply(msg))
        #self.text_widget.insert(END, "\n")
        self.text_widget.see(END)
                     
    def _bot_reply(self, msg):
        ops  = self.chat.get_option(msg)  
        msg2 = f"\n{self.bot_name}: {self.chat.get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self._show_option(ops)
        self.text_widget.configure(state=DISABLED)     
        self.text_widget.see(END)   
        



    
    # def _select_option(self, op):
    #     self.chat.list_question['type'] = op
    #     if(op == 'Xem thông tin các bệnh'):
    #         self._insert_message(op, "\nYou")
    #         self._show_option(self.chat.get_list_disease())
    #     else:
    #         #tu van theo trieu chung tai day
    #         pass
        
    def _show_option(self, ops):
        #danh sach cac lua chon
        # ops = ['A','B','C']  
        
        for op in ops:
            option_button = Button(text = op, width = 30, 
                            activebackground = '#d88a6c',
                            highlightcolor = '#f2ba9c',
                            justify= LEFT,
                            command= lambda op=op :self._select_option(op))
            self.text_widget.window_create("end", window=option_button)
            self.text_widget.insert(END,"\n")
    
    def _select_option(self, op):
        self._insert_message(op, "\nYou")
        pass
        

if __name__ == "__main__":
    app = ChatApplication()
    app.run()