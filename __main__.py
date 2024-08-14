import tkinter
import _thread
from data import pynput


class cfg:
    gey = (500, 500)
    sxe = False
    tle = "Exams"
    font_size = 15
    test_label = {
                  "choose-single": "单项选择题",
                  "decide": "判断题",
                  "choose-more": "多项选择题"
                  }
    in_test = []
    in_answer = []
    

class sxe:
    def __init__(self):
        self.fulscreen = None


    def begin(self):
        self.fulscreen(True)
        with pynput.keyboard.Listener(win32_event_filter=self.op) as self.lis:
           self.lis.join()
        

    def op(self, msg, data):
        abc = [i for i in range(65, 91)] + [i for i in range(ord('0'), ord('9') + 1)] + [160, 8, 13, 32, 162, 192, 189, 187, 37, 38, 39, 40]
        if not data.vkCode in abc:
            self.lis.suppress_event()


class gui:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("{}x{}".format(*cfg.gey))
        self.root.title(cfg.tle)

        self.test_button = tkinter.Button(master=self.root, text="get_answer", command=self.get_answer)
        self.test_button.place(x=0, y=0, relw=1, relh=0.05)

        self.as_scrolling_frame = tkinter.Frame(master=self.root)
        self.as_scrolling_frame.place(x=0, rely=0.05, relw=1, relh=0.95)

        self.scro = tkinter.Scrollbar(master=self.as_scrolling_frame)
        self.scro.pack(side="right", fill='y')

        self.as_canvas_scrolling = tkinter.Canvas(master=self.as_scrolling_frame)
        self.as_canvas_scrolling.pack(side="right", fill="both", expand=True)
 
        self.test_display_frame = tkinter.Frame(master=self.as_canvas_scrolling, width=1e+5, height=1e+5)
        
        self.as_canvas_scrolling.create_window((0, 0), window=self.test_display_frame, anchor='nw')

        self.as_canvas_scrolling.configure(yscrollcommand=self.scro.set, scrollregion=self.as_canvas_scrolling.bbox("all"))
        self.scro.config(command=self.as_canvas_scrolling.yview)
        self.as_canvas_scrolling.bind_all('<MouseWheel>', lambda event, self=self : self.as_canvas_scrolling.yview_scroll(-1 * (int(event.delta / 120)), 'units'))
        self.as_canvas_scrolling.bind_all('<Control - MouseWheel>', self.change_font_size)
        
        _ = self.get_test()
        cfg.in_test = _
        self.load_test()

    
    def change_font_size(self, event):
        cfg.font_size += int(event.delta / 120)
        self.load_test()
    

    def abc(self, l):
        return chr(ord(str(l)) + ord('A') - ord('1'))


    def get_answer(self):
        anw = []
        for i in cfg.in_answer:
            if type(i) == list:
                anw.append([self.abc(l + 1) for l in range(len(i)) if i[l].get()])  
                        
            else:
                anw.append(self.abc(i.get()))

        print(anw)
        return anw
    

    def get_test(self, path="./test_paper.test"):
        with open(path, 'r', encoding="utf-8") as f:
            ot = f.read()
            f.close()
        ot = [i for i in ot.split("\n") if (i != '') and (not (i[:2] in ["##", "//"])) and (not (i[0] in ['#']))]
        rt = []
        noft = int(ot[0])
        tp = ot[1 : noft + 1]
        
        for i in range(noft + 1):
            ot.pop(0)
        
        for i in range(len(tp)):
            t, s, idx = tp[i].split(' ')
            s = int(s)
            idx = int(idx) + 1
            if s == 0: continue
            rt.append([t])
            for l in range(0, s * idx, idx):
                rt[i].append(ot[l: l + idx])
            del ot[: s * idx]

        return rt


    def load_test(self, test=None, sort=True):
        fme = self.test_display_frame

        if not test: test = cfg.in_test

        for i in fme.winfo_children():
            i.destroy()

        ft = ("微软雅黑", cfg.font_size, "bold")
        _label = lambda *arges, **keys : tkinter.Label(font=ft, *arges, **keys) 

        row, col = 0, 0
        
        for i in range(len(test)):
            t = test[i][0]
            _label(master=fme, text=cfg.test_label[t]).grid(row=row, column=col, sticky='w')
            row += 1
            if t in ["choose-single", "choose-more", "decide"]:
                for l in range(1, len(test[i])):
                    lb = str(l) + ". "
                    _label(master=fme, text=lb + test[i][l][0]).grid(row=row, column=col, sticky='w')
                    row += 1

                    if t == "choose-more":
                        cfg.in_answer.append([])
                    else:
                        cfg.in_answer.append(tkinter.IntVar())
                    
                    for j in range(1, len(test[i][l])):
                        lb = self.abc(j)
                        if t == "choose-more":
                            _ = tkinter.IntVar()
                            cfg.in_answer[-1].append(_)
                            tkinter.Checkbutton(master=fme, text=lb + ". " + test[i][l][j], font=ft, variable=_).grid(row=row, column=col, sticky='w')
                        else:
                            tkinter.Radiobutton(master=fme, text=lb + ". " + test[i][l][j], font=ft, variable=cfg.in_answer[-1], value=j).grid(row=row, column=col, sticky='w')

                        row += 1

                    _label(master=fme, text='').grid(row=row, column=col, sticky='w')
                    row += 1


def main():
    _ = gui()

    if cfg.sxe:
        __ = sxe()
        __.fulscreen = lambda tf : _.root.attributes("-fullscreen", tf)
        _thread.start_new_thread(__.begin, ())
    _.root.mainloop()


if __name__ == "__main__":
    main()
