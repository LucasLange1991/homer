import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import json
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import subprocess
from homer_helperfile import *





#tkinter fenster einstellungen

window = tk.Tk()
window.title("homer")
window.geometry("485x367")
window.configure(bg="black")
window.attributes('-topmost', True)



# GIF
gif_image = Image.open(r'homer_working.gif')
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(gif_image))
        gif_image.seek(len(frames))  # Nächstes Einzelbild im GIF
except EOFError:
    pass


# Funktion zum Aktualisieren des Bildes in regelmäßigen Abständen
def update_image(frame_idx):
    image_label.configure(image=frames[frame_idx])
    image_label.image = frames[frame_idx]

    # Das nächste Einzelbild nach einer bestimmten Zeit anzeigen (hier: 100 ms)
    window.after(100, update_image, (frame_idx + 1) % len(frames))



# Hintergrundbild-Label erstellen und platzieren
image_label = tk.Label(window)
image_label.place(x=0, y=0)


checkbox_var = tk.IntVar()





#RR + FSM button funktionen

#KE

def rueckruf():
    try:
        subprocess.Popen([r'C:\Program Files\Notepad++\Notepad++.exe', json_ke_RR])
        output.delete("1.0", "end")
        output.insert("end", "...reading... KE RR Datenpunkte\n")
    except FileNotFoundError:
        output.delete("1.0", "end")
        output.insert("end", "not found.\n")

def fsm():
    try:
        subprocess.Popen([r'C:\Program Files\Notepad++\Notepad++.exe', json_ke_FSM])
        output.delete("1.0", "end")
        output.insert("end", "...reading... KE FSM Datenpunkte\n")
    except FileNotFoundError:
        output.delete("1.0", "end")
        output.insert("end", "not found.\n")


#BE

def be_rueckruf():
    try:
        subprocess.Popen([r'C:\Program Files\Notepad++\Notepad++.exe', json_be_RR])
        output.delete("1.0", "end")
        output.insert("end", "...reading... BE RR Datenpunkte\n")
    except FileNotFoundError:
        output.delete("1.0", "end")
        output.insert("end", "not found.\n")

def be_fsm():
    try:
        subprocess.Popen([r'C:\Program Files\Notepad++\Notepad++.exe', json_be_FSM])
        output.delete("1.0", "end")
        output.insert("end", "...reading... BE FSM Datenpunkte\n")
    except FileNotFoundError:
        output.delete("1.0", "end")
        output.insert("end", "not found.\n")





#funktion Ergebnisse


def open_Ergebnisse():
    try:
        subprocess.Popen([r'C:\Program Files\Notepad++\Notepad++.exe', 'Ergebnisse.txt'])

    except FileNotFoundError:
        output.delete("1.0", "end")
        output.insert("end", "not found.\n")

    output.delete("1.0", "end")
    output.insert("end", "...reading... Ergebnisse.txt\n")




#radiobuttons funktion + variable datenpunkte ändern

def handle_radiobutton():
    global datenpunkte
    if checkbox_var.get() == 1:
        datenpunkte = json_ke_RR
        output.delete("1.0", "end")
        output.insert("end", "KE RR Datenpunkte ausgewählt.\n")

def handle_radiobutton2():
    global datenpunkte
    if checkbox_var.get() == 2:
        datenpunkte = json_ke_FSM
        output.delete("1.0", "end")
        output.insert("end", "KE FSM Datenpunkte ausgewählt.\n")

def handle_radiobutton3():
    global datenpunkte
    if checkbox_var.get() == 3:
        datenpunkte = json_be_FSM
        output.delete("1.0", "end")
        output.insert("end", "BE FSM Datenpunkte ausgewählt.\n")

def handle_radiobutton4():
    global datenpunkte
    if checkbox_var.get() == 4:
        datenpunkte = json_be_RR
        output.delete("1.0", "end")
        output.insert("end", "BE RR Datenpunkte ausgewählt.\n")





#pdf dokument hinzufügen und file_path für suche ändern

class PDFDropLabel(tk.Label):
    def __init__(self, parent):
        super().__init__(parent)
        self.bind("<Button-1>", self.browse_files)
        self.config(text="PDF +")
        self.configure(bg="#9f5e70", fg="white", font=("Arial", 12))
        
    

    def browse_files(self, event):
        global file_path 
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.config(text="PDF Dokument hinzugefügt")
        else:
            messagebox.showerror("Keine Datei", "Es wurde keine Datei ausgewählt.")


#suche

def search_pdf():
    global datenpunkte

    with open(datenpunkte, 'r', encoding='utf-8') as file:
        data = json.load(file)

    suchbegriffe = []

    for key, values in data.items():
        if key in [   
            'Status-Felder',
            'Mustertyp',
            'Fahrzeug',
            'Rueckruf',
            'SW-Update',
            'Prozessuales',
            'Klaeger',
            'Klageantraege',
            'Erwerb',
            'Darlehen',
            'Leasing',
            'Weiterveraeusserung',
            'Vortraege/Bezuege - immer',
            'Vortraege/Bezuege - WLTP',
            'Vortraege/Bezuege - zusammengelegt',
            'Sonderfaelle & Einzelkaempfer - immer',
            'Sonderfaelle & Einzelkaempfer - s. Nutzf.',
            'Sonderfaelle & Einzelkaempfer - zusammengelegt',
            'be_Mustertyp',
            'be_Status-Felder',
            'be_Parteien',
            'be_Fahrzeug',
            'be_Prozessuales',
            'be_Ansprueche',
            'be_Rueckruf/SW-Update',
            'be_Erwerb',
            'be_Darlehen',
            'be_Weiterveraeusserung',
            'be_Leasing',
            'be_Antraege',
            'be_RA-Kosten',
            'be_Vortrag/Bezugnahme/Ruegen Klaeger',
            'be_Sonderfaelle / Einzelkaempfer',
            'be_Individuelle Kanzleimusterpunkte',
            'be_Standart-Muster Individuell',
            'be_FSM-Muster',
        ]:
            if isinstance(values, list):
                suchbegriffe.extend(values)
                #suchbegriffe = values
            elif isinstance(values,dict):
                #suchbegriffe = [item for sublist in values.values() for item in sublist]
                suchbegriffe.extend([item for sublist in values.values() for item in sublist])

    print(suchbegriffe)



# suche nach stichworten + kontext

    context_lenght = 0 

    def search_pdf_context(filepath, search_queries, context_length=850, num_lines=3):
        resource_manager = PDFResourceManager()
        return_string = StringIO()
        laparams = LAParams()
        device = TextConverter(resource_manager, return_string, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)

        with open(filepath, 'rb') as file:
            for page in PDFPage.get_pages(file, check_extractable=True):
                interpreter.process_page(page)

            text = return_string.getvalue()

# Durchsuche den Text nach den Suchbegriffen und gib den Kontext aus
        matches = {}
        lines = text.split('\n')
        num_lines_total = len(lines)

        for search_query in search_queries:
            query_matches = []
            found_match = False
            #match_count = 0

            for line_number, line in enumerate(lines):
                if search_query.lower() in line.lower():
                    found_match = True
                    start_index = max(0, line_number - num_lines - 3)                   # Startzeile für den Kontext
                    end_index = min(num_lines_total, line_number + num_lines + 12)       # Endzeile für den Kontext
                    context_lines = lines[start_index:end_index]
                    context = '\n'.join(context_lines)


                    if len(context) > context_lenght:
                        context = context[:context_length] + "..."


                    query_matches.append(context)
                    #match_count += 1

                    #if match_count >= 5:
                        #break

            if not found_match:
                query_matches.append("xx------------xx-\n--xx----------xx--\n---xx--------xx---\n----xx------xx----\n-----xx----xx-----\n------xx--xx------\n--------xx--------\n------xx--xx------\n-----xx----xx-----\n----xx------xx----\n---xx-------xx----\n--xx---------xx---\n-xx-----------xx--")
            
            matches[search_query] = query_matches

        device.close()
        return_string.close()

        return matches
    
    output.delete("1.0", "end")
    output.insert("end", "Suche abgeschlossen.")


# aufruf
    matches = search_pdf_context(file_path, suchbegriffe, context_length=850)

# Ergebnisse in Textdatei schreiben
    output_file = 'ergebnisse.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        for search_query, context_list in matches.items():
            file.write(f"\n \n              *** Suchbegriff = {search_query} ***\n\n\n\n")
            for context in context_list:
                file.write(f"                      *Treffer*\n\n {context}\n\n\n\n")
            file.write("\n")


#output text + window

output = tk.Text(window, height=2, width=30, bg="#7c3b02", fg="#c7a671", font=("Dreaming Outloud Pro", 10))
output.pack()
output.place(x=130, y=318)

output_text = tk.Text(window, height=22, width=45, bg="black", fg="#c7a671")
output_text.pack()
output_text.place(x=1000, y=20)

# Buttons RR/FSM KE/BE

button_FSM = tk.Button(window, text="FSM", command=fsm, bg="#9b688d", fg="white", width=3, height=1, font=("Arial", 15, "bold"))
button_FSM.place(x=28, y=78)

button_RR = tk.Button(window, text="RR", command=rueckruf, bg="#9b688d", fg="white", width=2, height=1, font=("Arial", 15, "bold"))
button_RR.place(x=75, y=78)

button_be_FSM = tk.Button(window, text="FSM", command=be_fsm, bg="#94877d", fg="white", width=3, height=1, font=("Arial", 15, "bold"))
button_be_FSM.place(x=349, y=120)

button_be_RR = tk.Button(window, text="RR", command=be_rueckruf, bg="#94877d", fg="white", width=3, height=1, font=("Arial", 15, "bold"))
button_be_RR.place(x=422, y=120)


# Buttons search ergebnisse output

button_PDFsearch = tk.Button(window, text="suchen!", command=search_pdf, bg="#3c1045", fg="white", width=10, height=1, font=("Arial", 15, "bold"))
button_PDFsearch.place(x=330, y=10)

button_ergebnisse = tk.Button(window, text="Ergebnisse", command=open_Ergebnisse, bg="#9b688d", fg="white", width=9, height=1, font=("Arial", 10, "bold") )
button_ergebnisse.place(x=360,y=69)


#radiobuttons

radio_button1 = tk.Radiobutton(window,bg="#9b688d", text="", variable=checkbox_var, value=1, command=handle_radiobutton)
radio_button1.pack
radio_button1.place(x=78, y=140)

radio_button2 = tk.Radiobutton(window,bg="#9b688d", text="", variable=checkbox_var, value=2, command=handle_radiobutton2)
radio_button2.pack
radio_button2.place(x=44, y=140)

radio_button3 = tk.Radiobutton(window,bg="#94877d", text="", variable=checkbox_var, value=3, command=handle_radiobutton3)
radio_button3.pack
radio_button3.place(x=360, y=170)

radio_button4 = tk.Radiobutton(window,bg="#94877d", text="", variable=checkbox_var, value=4, command=handle_radiobutton4)
radio_button4.pack
radio_button4.place(x=433, y=170)


# PDF-Drop-Label erstellen und platzieren

pdf_label = PDFDropLabel(window)
pdf_label.place(x=6, y=6)



# Starte die Aktualisierung des Bildes
update_image(0)

# Tkinter-Hauptschleife starten
window.mainloop()