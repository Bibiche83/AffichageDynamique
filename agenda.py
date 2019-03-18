
# -*- coding: utf-8 -*-

from tkinter import* # Importation du module tkinter
from tkinter.messagebox import *
from calendar import monthcalendar # Instancie un calendrier mensuel
from calendar import Calendar # Instancie un calendrier annuel
from time import localtime # Importation de la date et de l'heure locales
from datetime import time, datetime # Module permettant de manipuler les dates et les durées.
from os import chdir        # Importation du module OS pour effectuer le changement de répertoire
import os
import os.path
from PIL import Image, ImageTk  # Module PIL (traitement des images importées)
from contextlib import suppress
               
#==== CLASSE ==============================================================================================
 
class Agenda(object) :
    "Instanciation de l'agenda"
   
    dico_iteration = {}
   
    def __init__(self, d, m, y) :
        "Constructeur"     
        self.d = d
        self.m = m
        self.y = y 
 
#----------------------------------------------------------------------------------------------------------
 
    def pages(self, destroy_date = int()) :
        "Création des pages"
        if destroy_date != int() : # Destruction éventuelle de la page précédemment consultée
            destroy_date.destroy()
        self.page = Tk()
        self.page.title('Mon agenda')
       
#----------------------------------------------------------------------------------------------------------
 
        self.frame = Frame(self.page, bg='white')
        self.frame.grid()
   
#----------------------------------------------------------------------------------------------------------
 
        self.buttons = Frame(self.frame, bg='white')
        self.buttons.grid(row=0, column=0, sticky = 'w')
 
#----------------------------------------------------------------------------------------------------------
   
        # Widget Frame qui contient la date du jour et deux petits triangles de changement de date :
        self.subframe = Frame(self.frame, bg='white', relief='groove', bd=1, padx= 170)
        self.subframe.grid(row=1, column=0, columnspan=2, sticky = 'nsew')
   
#----------------------------------------------------------------------------------------------------------
   
        #Création de trois boutons d'en-tête. Les commandes sont configurées plus tard :
        self.button_list = list()
        self.textes = ['Enregistrer', 'Valider', 'Effacer']
        for i in range(0, len(self.textes)):
            self.button = Button(self.buttons, text = self.textes[i], bg='#357AB7', fg='white', activebackground='white', activeforeground='#357AB7')
            self.button.grid(row=0, column=i)
            self.button_list.append(self.button)
 
        # Création de l'onglet "rechercher" :
        self.search_labelframe = LabelFrame(self.buttons, bd=1, highlightthickness=0, bg='white')
        self.search_labelframe.grid(row=0, column = 4)
 
        # Importation de l'image de la loupe :
        self.mon_image = "/home/benoit/Documents/agendrier/loupe.png" # Importation de l'image
        self.image = Image.open(self.mon_image)
        self.size = 32, 32 # Réduction de la taille de l'image
        self.image.thumbnail(self.size)
        self.photo = ImageTk.PhotoImage(self.image, master = self.page)
 
        # Fonction qui efface le mot "Rechercher" lorsque l'utilisateur clique dans le widget "Entry"
        def delete(event):
            if self.search_entry.get() == "Rechercher":
                self.search_entry.delete(0, 'end')
 
        # Création du widget "chercher":
        self.search_entry = Entry(self.search_labelframe, fg='#357AB7', font='Times 12 bold', border=0, highlightthickness=0)
        self.search_entry.grid(row=0, column=0)
        self.search_entry.insert(0, "Rechercher")
        self.search_entry.bind('<Button-1>', delete)
 
        # Création du bouton "loupe" :
        self.find = Actions(self.d, self.m, self.y)
        self.search = Button(self.search_labelframe, image=self.photo, bd=0, highlightthickness=0, command = lambda : self.find.search(self.search_entry))
        self.search.grid(row=0, column=1)
 
 #----------------------------------------------------------------------------------------------------------
       
        # Création du triangle de changement de date (vers le futur):
        self.next_day = Actions(int(self.d)+1, self.m, self.y) # Création de l'objet "Jour d'après" :
        self.right_triangle=Button(self.subframe,bg='white',fg='#357AB7',text=u"\u25B6",bd=0,highlightthickness=0,padx=0,pady=0,activebackground='#357AB7',activeforeground='white')
        self.right_triangle.grid(row = 0, column = 2, padx = 10, sticky = 'e')
        self.right_triangle['command'] = lambda : self.next_day.next_day(self.page)
#----------------------------------------------------------------------------------------------------------
 
        # Date sous la forme dd/mm/yyyy.
        # Quatre possibilités différentes concernant l'adjonction d'un "0" supplémentaire :
        if int(self.d) < 10 and self.m < 10 :
            self.date = Label(self.subframe, bg = 'white', fg='#357AB7', bd=0, font = 'Times 18 bold',
            text = '0' + str(self.d) + '/' + '0' + str(self.m) + '/' + str(self.y))
        elif int(self.d) < 10 :
            self.date = Label(self.subframe, bg = 'white', fg='#357AB7', bd=0, font = 'Times 18 bold',
            text = '0' + str(self.d) + '/' + str(self.m) + '/' + str(self.y))
        elif self.m < 10 :
            self.date = Label(self.subframe, bg = 'white', fg='#357AB7', bd=0, font = 'Times 18 bold',
            text = str(self.d) + '/' + '0' + str(self.m) + '/' + str(self.y))
        else :
            self.date = Label(self.subframe, bg = 'white', fg='#357AB7', bd=0, font = 'Times 18 bold', text = str(self.d) + '/' + str(self.m) + '/' + str(self.y))
        self.date.grid(row = 0, column = 1, sticky = 'nsew')
 
#----------------------------------------------------------------------------------------------------------
 
        # Création du triangle de changement de date (vers le passé):
        self.previous_day = Actions(int(self.d)-1, self.m, self.y) # Création de l'objet "Jour d'avant" :
        self.left_triangle=Button(self.subframe, bg='white', fg='#357AB7', text=u"\u25C0", bd=0, highlightthickness=0, padx = 0, pady = 0, activebackground = '#357AB7', activeforeground = 'white')
        self.left_triangle.grid(row = 0, column = 0, padx = 10, sticky = 'w')
        self.left_triangle['command'] = lambda : self.previous_day.previous_day(self.page)
   
#----------------------------------------------------------------------------------------------------------
 
        # Jour en cours. Remplacement des slashes par des tirets bas :
        self.current_date = self.date['text'].replace('/', '_')
 
#----------------------------------------------------------------------------------------------------------
 
        # Création des pages de l'agenda
        self.subframe2_list = list() # Création de deux listes vides.
        self.hour_list = []
        for i in range(7,22): # pour chaque heure de la journée :
            self.subframe2 = Frame(self.frame, bg='white') # Création d'un cadre
            self.subframe2.grid(row=i-5, column=0, sticky='nsew')
            self.subframe2_list.append(self.subframe2)
            if i < 10 : # Création des étiquettes affichant les heures de la journée.
                self.label = Label(self.subframe2, fg = 'white', bg = '#357AB7', padx=5, pady=2,font = 'bold', text = '  ' + str(i) + u"\u2070\u2070")
            else :
                self.label = Label(self.subframe2, fg = 'white', bg = '#357AB7', padx=5, pady=2,font = 'bold', text = str(i) + u"\u2070\u2070")
            self.label.grid(row=0, column = 0, sticky='nsew')  
            # Création des entrées pour chaque heure de la journée :
            self.hour = Text(self.subframe2, bg ='white', fg = 'black', font ='Times 14', highlightthickness=0, bd=1, selectbackground='blue', selectforeground='white', wrap='word', width=50, height=1, padx=10, pady=2)
            self.hour.grid(row=0, column=1, sticky='nsew')
            self.hour_list.append(self.hour)
 
        self.action_affichage = Actions(self.d, self.m, self.y, self.current_date, self.hour_list)
        self.action_affichage.entries(self.page) # Affichage les différentes entrées de la page appelée.
       
        self.save = Actions(self.d, self.m, self.y, self.current_date)
        self.validation = Actions(self.d, self.m, self.y, self.current_date)
        self.invalider = Actions(self.d, self.m, self.y, self.current_date)
        self.erase = Actions(self.d, self.m, self.y, self.current_date)
        self.button_list[0]['command'] = lambda : self.save.save(self.subframe2_list)
        self.button_list[1]['command'] = lambda : self.validation.validation(self.subframe2_list, self.page)
        self.button_list[2]['command'] = lambda : self.erase.erase(self.subframe2_list, self.page)
   
        # Message qui apparait sous la forme d'une fenêtre pop-up dans le cas où une entrée n'a pas été traitée ni validée. Le message contient la date et le texte de l'entrée :
        self.validated = open('validated','r')
        self.read_validated = self.validated.readlines()
        self.validated.close()
        for i in range (0, len(self.read_validated)):
            self.read_validated[i] = self.read_validated[i][:-1]
        self.filelist = open('entrylist', 'r')
        self.readfilelist = self.filelist.readline()
        self.filelist.close()
        self.readfilelist = self.readfilelist.split(',')
        self.readfilelist = self.readfilelist[:-1]
        for i in range(0, len(self.readfilelist)) :
            if self.readfilelist[i] not in Agenda.dico_iteration :
                Agenda.dico_iteration[self.readfilelist[i]] = 0
                index = Agenda.dico_iteration[self.readfilelist[i]]
            else:
                Agenda.dico_iteration[self.readfilelist[i]] = 1
                index = Agenda.dico_iteration[self.readfilelist[i]]
            self.readfilelist[i] = self.readfilelist[i].split('-')
            for i2 in range(0, len(self.readfilelist[i])):
                self.readfilelist[i][i2] = self.readfilelist[i][i2].split('_')
            if self.readfilelist[i][0] == '':
                self.readfilelist[i][0] = []
            self.duration = datetime.now() - datetime(int(self.readfilelist[i][0][2]), int(self.readfilelist[i][0][1]), int(self.readfilelist[i][0][0]))
            self.readfilelist[i][0] = '_'.join(self.readfilelist[i][0])
            self.readfilelist[i][1] = ''.join(self.readfilelist[i][1])
            self.readfilelist[i] = '-'.join(self.readfilelist[i])
            if self.duration.days > 1 and self.readfilelist[i] not in self.read_validated :
                while index < 1 :
                    self.file = open(self.readfilelist[i], 'r')
                    self.readfile = self.file.readline()
                    self.readfilelist[i] = self.readfilelist[i].replace("_", "/")
                    self.readfilelist[i] = self.readfilelist[i][:-3]
                    self.warning = showwarning(self.readfilelist[i], self.readfilelist[i] + '\n' + self.readfile)
                    index += 1
                    Agenda.dico_iteration[self.readfilelist[i]] = 1
 
        # Démarrage du réceptionnaire d'événements :
        self.page.mainloop()
                               
#==== CLASSE ==============================================================================================    
 
class Actions(Agenda) :
    "Actions enregister, effacer, valider..."
   
    def __init__(self, d, m, y, current_date = [], hour_list = []) :
        "Constructeur"
        Agenda.__init__(self, d, m, y)
        self.current_date = current_date
        self.hour_list = hour_list
       
#----------------------------------------------------------------------------------------------------------
                       
    def previous_day(self, page) :
        "Conditions à remplir pour reculer d'un jour"
        if self.d < 1 :
            self.m -=1
            if self.m == 0 :
                self.m = 12
                self.y -= 1
            self.c = monthcalendar(self.y, self.m)
            self.d = max(max(self.c))# "max(max" s'explique par le fait que self.c est une liste de listes.
        self.pages(page)
 
#----------------------------------------------------------------------------------------------------------
       
    def next_day(self, page) :
        "Conditions à remplir pour avancer d'un jour"
        self.c = monthcalendar(self.y, self.m) # Mois en cours.
        if self.d > max(max(self.c)): # Si le n° du jour est supérieur au n° du dernier jour du mois
            self.d = '1' # N° du jour = 1
            self.m += 1
            if self.m > 12 :
                self.m = 1  # m = mois
                self.y += 1 # y = year(année)
        self.pages(page)               
 
#----------------------------------------------------------------------------------------------------------
 
    def save(self, subframe2_list):
        "Enregistrement des entrées"
        self.subframe2_list = subframe2_list
        self.file = None
        for i in range(0, len(self.subframe2_list)) :
            for child in self.subframe2_list[i].winfo_children():
                if child.winfo_class() == "Text":
                    self.get_text = child.get(1.0, 'end')
                    self.filename = str(self.current_date) + '-' + str(i)
                    if len(self.get_text) > 1 :
                        self.file = open(self.filename, 'w')
                        self.file.write(self.get_text)
                        self.file.close()
                        self.filelist = open('entrylist', 'r')
                        self.readfilelist = self.filelist.readline()
                        self.filelist.close()
                        self.readfilelist = self.readfilelist.strip() + self.filename + ','
                        self.readfilelist.replace('\n','')
                        self.filelist = open('entrylist', 'w')
                        self.filelist.write(self.readfilelist)                     
                        self.filelist.close()
                        self.readfilelist = self.readfilelist.split(',')
                        self.readfilelist2 = []
                        for entry in self.readfilelist :
                            if entry not in self.readfilelist2 :
                                self.readfilelist2.append(entry)
                            if entry == '' :
                                del entry
                        self.readfilelist2 = ",".join(self.readfilelist2)
                        self.filelist = open('entrylist', 'w')
                        self.filelist.write(self.readfilelist2)
                        self.filelist.close()
                if child['bg'] == 'green' and child['fg'] == 'white' :
                    self.green(i, self.filename)
 
#----------------------------------------------------------------------------------------------------------
 
    def entries(self, page) :
        "Affichage des entrées de la page consultée"
        self.page = page
        self.filelist = open('entrylist', 'r')
        self.readfilelist = self.filelist.readline()
        self.readfilelist = self.readfilelist.split(',')
        for i in range(0, len(self.readfilelist)):
            self.readfilelist[i] = self.readfilelist[i].split('-')
        self.readfilelist = self.readfilelist[:-1]
        self.filelist.close()
        for i in range (0, len(self.readfilelist)) :
            self.filename = str(self.current_date) + '-' + self.readfilelist[i][1]
            if '-'.join(self.readfilelist[i]) == self.filename :
                self.file = open(self.filename, 'r')
                self.readfile = self.file.readline()
                self.hour_list[int(self.readfilelist[i][1])].delete(1.0, 'end')
                self.readfile = self.readfile.strip()
                self.hour_list[int(self.readfilelist[i][1])].insert('end', self.readfile)
                self.file.close()
        self.validated = open('validated', 'r')
        self.read_validated = self.validated.readlines()
        self.validated.close()
        self.read_validated_2 = []
        for entry in self.read_validated :
            if entry not in self.read_validated_2 :
                self.read_validated_2.append(entry)
        self.validated = open('validated', 'w')
        for i in range (0, len(self.read_validated_2)):
            self.validated.write(self.read_validated_2[i])
        self.validated.close()
        for i in range(0, len(self.read_validated_2)):
            self.read_validated_2[i] = self.read_validated_2[i].split('-')
            if self.read_validated_2[i][0] == self.current_date :
                self.hour_list[int(self.read_validated_2[i][1])].config(bg = 'green', fg = 'white')
               
#----------------------------------------------------------------------------------------------------------    
 
    def validation(self, subframe2_list, page):
        "Validation des entrées traitées (Rendez-vous honorés etc...)"
        self.page = page
        self.subframe2_list = subframe2_list
        self.validated_entry = self.page.focus_get()
        self.validated_entry.config(bg = 'green', fg = 'white')
        self.save(self.subframe2_list)
                       
#----------------------------------------------------------------------------------------------------------    
 
    def green(self, i, filename) :
        "Stockage des pages validées dans un fichier"
        self.validated = open('validated', 'a')
        self.validated.write(filename + '\n')
        self.validated.close()
           
#----------------------------------------------------------------------------------------------------------
                   
    def erase(self, subframe2_list, page):
        "Effacement des entrées"
        self.page = page
        self.subframe2_list = subframe2_list
        self.get_entry = self.page.focus_get()
        self.get_entry.delete(1.0, 'end')
        self.get_entry.config(bg='white', fg='black')
        self.filename = ''
        for i  in range(0, len(self.subframe2_list)) :
            for child in self.subframe2_list[i].winfo_children():
                if child == self.get_entry:
                    self.filename = str(self.current_date) + '-' + str(i)  
        self.validated = open('validated', 'r')
        self.read_validated = self.validated.readlines()
        self.validated.close()
        if self.filename + '\n' in self.read_validated :
            self.read_validated.remove(self.filename + '\n')
        self.validated = open('validated', 'w')
        for i in range(0, len(self.read_validated)):
            self.validated.write(self.read_validated[i])
        self.validated.close()
        self.filelist = open('entrylist', 'r')
        self.readfilelist = self.filelist.readline()
        self.readfilelist = self.readfilelist.split(',')
        if self.filename in self.readfilelist :
            self.readfilelist.remove(self.filename)
        self.readfilelist = ','.join(self.readfilelist)
        self.filelist.close()
        self.filelist = open('entrylist', 'w')
        self.filelist.write(self.readfilelist)
        self.filelist.close()
        os.remove('/home/benoit/' + self.filename)
                   
#----------------------------------------------------------------------------------------------------------
   
    def search(self, search_entry):
        "Méthode qui cherche une chaîne de caractères dans les fichiers"
        with suppress(Exception):
            self.search_string = search_entry.get()
            self.search_string = self.search_string.lower()
            self.listdir = os.listdir('/home/benoit/Documents/agendrier')
            self.list_all_files = list()
            for i in range (0, len(self.listdir)) :
                if self.listdir[i]!='validated' and self.listdir[i]!='entrylist' and self.listdir[i]!='__pycache__' and os.path.splitext(self.listdir[i])[1]!='.py' and os.path.splitext(self.listdir[i])[1] != '.py~':
                    self.list_all_files.append(self.listdir[i])
            self.in_page = Toplevel(bg = 'white', padx=10, pady=10)
            self.in_page.title('Votre recherche')
            self.label = Label(self.in_page, bg = 'white', text = 'Les pages suivantes'+'\n'+'contiennent votre recherche', fg = 'black', font='Times 18 bold')
            self.label.grid(row=0, column = 0, columnspan = 4, pady = 10)
            i2 = 1 # variable d'incrémentation de la ligne dans le Toplevel
            i3 = 0 # variable d'incrémentation de la colonne dans le Toplevel
            for i in range(0, len(self.list_all_files)):
                self.file = open(self.list_all_files[i], 'r')
                self.readfile = self.file.readline()
                self.readfile = self.readfile.lower()
                self.file.close()
                if self.readfile.find(self.search_string) != -1 :
                    self.filename = os.path.splitext(self.list_all_files[i])
                    self.d = int(self.filename[0][:2])
                    self.m = int(self.filename[0][3:5])
                    self.y = int(self.filename[0][6:10])
                    self.button_page = Button(self.in_page, bg='#357AB7', fg='white', text=self.filename[0][:10].replace('_','/'))
                    self.button_page.grid(row=i2, column = i3, sticky = 'w')
                    self.show_page = Agenda(self.d, self.m, self.y)
                    self.show_page.pages
                    self.button_page.config(command=self.show_page.pages)
                    i3 += 1
                    if i3 % 4 == 0:
                        i2 += 1
                        i3 = 0 
        if len(self.in_page.winfo_children()) == 1 :
            self.label.config(bg='red', fg='white', text='Aucun résultat', padx = 50)
           
# ##### MAIN PROGRAMM #####################################################################################
 
if __name__ == "__main__":
 
    rep = os.getcwd() # = /home/benoit
    if rep != '' :
        rep = ''
    chdir(rep + "D:\PROJET_AFFICHAGE_DYNAMIQUE\PROGRAMME") # Change directory, c'est-à dire changement du répertoire de travail courant.
 
    d = localtime()[2] # Current day
    m = localtime()[1] # Current month 
    y = localtime()[0] # Current year
 
    agenda = Agenda(d, m, y)
    agenda.pages()