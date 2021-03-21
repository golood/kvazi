import json
from tkinter import Tk, Button, Label, StringVar, DISABLED, NORMAL
from tkinter import filedialog
from tkinter.messagebox import showerror
from core.dto import Data
from core.models import ModelData
from core.exceptions import BusinessLogicException

INITIALDIR = '/home/ashum/projects/OTHER/kvazi'


class MainWidow(object):
    def __init__(self, model_data: ModelData):
        self.modelData = model_data

        self.root = Tk()
        self.root.title('Квази')
        self.root.geometry('600x300')

        self.btn_open_file = Button(self.root, text='Загрузить файл', command=self.load_file)
        self.btn_open_file.place(x=10, y=20)

        self.var_name_var_load = StringVar()
        self.lb_name_file_load = Label(self.root, textvariable=self.var_name_var_load)
        self.lb_name_file_load.place(x=200, y=26)

        self.btn_save_file = Button(self.root, text='Сохранить результаты решения', command=self.save_file,
                                    state=DISABLED)
        self.btn_save_file.place(x=10, y=60)

        self.btn_start = Button(self.root, text='Вычислить', command=self.calculation, state=DISABLED)
        self.btn_start.place(x=10, y=120)

        self.root.mainloop()

    def load_file(self):
        f_types = [('JSON files', '*.json')]
        filename = filedialog.askopenfilename(initialdir=INITIALDIR, title="Выберете файл", filetypes=f_types)

        if filename:
            self.__read_file(filename)

    def calculation(self):
        pass

    def save_file(self):
        pass

    def __read_file(self, filename):
        with open(filename) as f:
            _data = json.load(f)
        try:
            self.modelData.dataDTO = Data(_data)
            self.var_name_var_load.set(filename)
            self.btn_start.config(state=NORMAL)
        except BusinessLogicException as err:
            showerror(title='Ошибка', message=err)
            print('Error:', err)


if __name__ == '__main__':
    window = MainWidow(ModelData())
