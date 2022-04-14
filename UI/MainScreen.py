from sys import path
from os.path import dirname as dir
path.append(dir(path[0]))



from tkinter import Menu, Tk
from tkinter import filedialog as fd


class MainScreen:
    def __init__(self):
        self.inicializerScreen()
    
    def inicializerScreen(self):
        # Inicializacion de la pantalla
        self.window = Tk()
        self.window.geometry("600x600")
        self.window.resizable(0,0)
        self.window.title("Smart ETL")
        # Menu
        navMenu = Menu(self.window)
        navMenu.add_command(label="Load Files", command=self.open_csv_file)
        self.window.config(menu=navMenu)
        self.window.mainloop()
    
    def open_csv_file(self):
        filetypes =(('csv files', '*.csv'), ('All files', '*.*'))
        f = fd.askopenfile(filetypes=filetypes)


def main():  # Funcion main
    queryTool = MainScreen()
    return 0


if __name__ == "__main__":
    main()