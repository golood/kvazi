import tkinter as tk


class MainWidow(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Квази')
        self.root.geometry('600x300')

        self.btn_open_file = tk.Button(self.root, text='Загрузить файл')
        self.btn_open_file.place(x=10, y=20)

        self.var_name_var_load = tk.StringVar()
        self.lb_name_file_load = tk.Label(self.root, textvariable=self.var_name_var_load)
        self.lb_name_file_load.place(x=200, y=26)

        self.btn_save_file = tk.Button(self.root, text='Сохранить результаты решения', state=tk.DISABLED)
        self.btn_save_file.place(x=10, y=60)

        self.btn_start = tk.Button(self.root, text='Вычислить', state=tk.DISABLED)
        self.btn_start.place(x=10, y=120)

        self.root.mainloop()


if __name__ == '__main__':
    window = MainWidow()
