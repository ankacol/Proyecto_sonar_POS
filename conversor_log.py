from tkinter import filedialog, messagebox, ttk
from tkinter import *
from getLocationPos import get_pos
import os.path as path
import os

# Se crean las variables para llevar conteo de los puntos
counter_p = 0
counter_fp = 0
counter_sp = 0
counter_tp = 0




raiz = Tk()
raiz.title('Procesamiento archivos Sonar .log ANKA')
raiz.resizable(1, 1)
raiz.iconbitmap("anka.ico")
ruta_archivo_log = None
ruta_archivo_pos = None
raiz.geometry("400x400")
s = ttk.Style(raiz)
s.layout("LabeledProgressbar",
    [('LabeledProgressbar.trough',
    {'children': [('LabeledProgressbar.pbar',
                    {'side': 'left', 'sticky': 'ns'}),
                    ("LabeledProgressbar.label",
                    {"sticky": ""})],
    'sticky': 'nswe'})])
progressbar=ttk.Progressbar(raiz, orient="horizontal", length=300, mode="determinate", style="LabeledProgressbar")
progressbar.pack(side=BOTTOM)

def weeksecondstoutc(gpsweek,gpsseconds):
    import datetime
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
    elapsed = datetime.timedelta(days=(gpsweek*7),seconds=(gpsseconds))
    return datetime.datetime.timestamp(epoch + elapsed)

def state_check ():
        check= var1.get()
        print (check)



def abrir_archivo_pos():
    global ruta_archivo_pos
    ruta_archivo_pos = ""
    lid_file_label = Label(text="Selecciono el archivo: ")
    ruta_archivo_pos = filedialog.askopenfilename(initialdir = os.getcwd(),
        title = "Seleccione archivo .pos", filetypes = (("Archivos binarios", ".pos"),
        ("all files", "*.*")))
    lid_file_label.place(x = 10, y = 160)
    Label(text=ruta_archivo_pos).place(x = 10, y = 180)
    print("Ruta del archivo .log: " + ruta_archivo_pos)

# Funcion que se activa al pulsar el boton de "Abrir archivo" para cargar el archivo de trayectorias
def convertir_archivo_button():
    get_pos(ruta_archivo_pos=ruta_archivo_pos)
    info_message = "Los archivos han sido procesados correctamente"
    messagebox.showinfo(title="Exito!!!", message=info_message)
    



Label(text="Seleccione el archivo .pos de la ruta").place(x = 10, y = 110)

Button(text="Abrir archivo", bg="#eb7434", command = abrir_archivo_pos).place(x = 10, y = 130)

Button(text="Convertir archivo", bg="#eb7434", command = convertir_archivo_button).place(x = 10, y = 205)



raiz.mainloop()