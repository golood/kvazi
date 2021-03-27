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

        self.lb_title_result = Label(self.root, text='Результаты вычислений:', state=DISABLED)
        self.lb_title_result.place(x=10, y=160)
        self.var_body_result = StringVar()
        self.lb_body_result = Label(self.root, textvariable=self.var_body_result, state=DISABLED)
        self.lb_body_result.place(x=10, y=200)

        self.root.mainloop()

    def load_file(self):
        f_types = [('JSON files', '*.json')]
        filename = filedialog.askopenfilename(initialdir=INITIALDIR, title="Выберете файл", filetypes=f_types)

        if filename:
            self.__read_file(filename)

            self.var_body_result.set('')
            self.lb_title_result.config(state=DISABLED)
            self.btn_save_file.config(state=DISABLED)
            self.modelData.solve = None

    def calculation(self):
        try:
            self.modelData.solve_task()
            result = self.modelData.get_result()

            self.btn_save_file.config(state=NORMAL)
            self.show_result(result)
        except BaseException as err:
            print(err)
            showerror(title='Ошибка', message=err)

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

    def show_result(self, result):
        self.lb_title_result.config(state=NORMAL)
        self.lb_body_result.config(state=NORMAL)

        s = 'Значение целевой функции: {}\n'.format(result['c'])
        count = 0
        for item in result['var']:
            s += '{} = {}, '.format(item, result['var'][item])
            if count == 5:  # Выводим в строке по 5 переменных
                s += '\n'
                count = 0
                continue
            count += 1
        self.var_body_result.set(s)


if __name__ == '__main__':
    window = MainWidow(ModelData())
