from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from sys import getsizeof, path
from os import system
from os.path import dirname as dir

path.append(dir(path[0]))

from Controller.ETLController import ETLController

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

files = []


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def openFolder():    
    system('start %windir%\explorer.exe "'+dir(path[0])+'\\Proyecto1\\WrongData"')

def openFolderD():    
    system('start %windir%\explorer.exe "'+dir(path[0])+'\\Proyecto1\\Documentation"')

window = Tk()

window.geometry("908x585")
window.configure(bg="#000000")


canvas = Canvas(
    window,
    bg="#000000",
    height=585,
    width=908,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)

canvas.place(x=0, y=0)
canvas.create_rectangle(271.0, 0.0, 908.0, 585.0, fill="#FCFCFC", outline="")

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))


button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
)
button_3.place(x=30.0, y=283.0, width=180.0, height=55.0)

button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=openFolder,
    relief="flat",
)
button_4.place(x=30.0, y=432.0, width=180.0, height=55.0)

canvas.create_text(
    26.0,
    96.0,
    anchor="nw",
    text="SmartETL",
    fill="#FCFCFC",
    font=("Roboto Bold", 36 * -1),
)

canvas.create_text(
    287.0,
    316.0,
    anchor="nw",
    text="Console",
    fill="#000000",
    font=("Roboto Bold", 24 * -1),
)

canvas.create_text(
    287.0, 10.0, anchor="nw", text="Data", fill="#000000", font=("Roboto Bold", 24 * -1)
)

canvas.create_rectangle(29.0, 138.0, 89.0, 143.0, fill="#FCFCFC", outline="")


button_image_6 = PhotoImage(file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=openFolderD,
    relief="flat",
)
button_6.place(x=210.0, y=539.0, width=55.0, height=35.3055419921875)



entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(590.0, 459.0, image=entry_image_1)
entry_1 = Text(bd=0, bg="#E1E1E1", highlightthickness=0)
entry_1.config(state=DISABLED)
entry_1.place(x=287.0, y=344.0, width=606.0, height=228.0)


tableFrame = Frame(window, height=100)

tableFrame.pack(side=TOP, anchor=NE, padx=10, pady=45)

fileTable = ttk.Treeview(tableFrame)
fileTable["columns"] = ("file_name", "file_path")

fileTable.column("#0", width=0, stretch=NO)
fileTable.column("file_name", anchor=CENTER, width=200)
fileTable.column("file_path", anchor=CENTER, width=400)

fileTable.heading("#0", text="", anchor=CENTER)
fileTable.heading("file_name", text="File Name", anchor=CENTER)
fileTable.heading("file_path", text="Path", anchor=CENTER)

fileTable.pack()


def deleteItems():
    global files
    # Get selected item to Delete
    if len(fileTable.selection()) !=0:
        selected_item = fileTable.selection()[0]
        item = fileTable.item(selected_item).get("values")
        files.remove(item[1])
        fileTable.delete(selected_item)


def open_csv_file():
    global files
    filetypes = (("csv files", "*.csv"), ("All files", "*.*"))
    f = fd.askopenfilename(filetypes=filetypes)
    if f != "":
        files.append(f)
        name = f.split("/").pop()
        fileTable.insert(parent="", index="end", text="", values=(name, f))


def startProcess():
    global files
    entry_1.config(state=NORMAL)
    etlController = ETLController(entry_1, files)
    etlController.etlProcess() 
    #time.sleep(5)  
    entry_1.insert(END, "-------------Terminado------------- \n")
    entry_1.insert(END, "Limpiando archivos \n")
    entry_1.config(state=DISABLED)
    files = []
    for i in fileTable.get_children():
        fileTable.delete(i)


button_image_5 = PhotoImage(file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=startProcess,
    relief="flat",
)
button_5.place(x=30.0, y=357.0, width=180.0, height=55.0)

button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=open_csv_file,
    relief="flat",
)
button_1.place(x=30.0, y=208.0, width=180.0, height=55.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=deleteItems,
    relief="flat",
)
button_2.place(x=30.0, y=283.0, width=180.0, height=55.0)

window.resizable(False, False)
window.mainloop()
