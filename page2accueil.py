# -*- coding: utf-8 -*-

# ##########################importation des librairies nécessaires ##########################################
import shutil
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image, ImageTk
import socket
import PyQt5
import os
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys
from calendar import monthcalendar # Module servant à instancier les mois du calendrier
from time import localtime # Importation de la date et de l'heure locales
from datetime import datetime # Module permettant de manipuler les dates et les durées.
from os import chdir
from lxml import etree
import xml.etree.ElementTree as etree
import os
from xml.dom import minidom
from pdfminer import *
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from agenda import Agenda # Module permettant d'ouvrir l'agenda



# ####################### On créez la fenetre et on lui donne une taille en pixel ############################
fenetre = Tk()
fenetre.geometry("1600x900")
fenetre.configure(bg='#A9EAFE')

Titre = Label(fenetre, text='PROJET AFFICHAGE NUMERIQUE EN PYTHON IHM ADRIEN',bg='#74D0F1' ,relief = GROOVE)
Titre.pack(side = TOP)



# #############################Création des frames dans la page #################################################


# frame 1 image
Frame1 = Frame(fenetre,bg='#1E7FCB', borderwidth=2, relief=GROOVE)
Frame1.pack(side=LEFT, padx=10, pady=10)

# frame 2 texte
Frame2 = Frame(fenetre,bg='#1E7FCB', borderwidth=2, relief=GROOVE)
Frame2.pack(side=LEFT, padx=10, pady=10)

# frame 3 video
Frame3 = Frame(fenetre, bg='#1E7FCB', borderwidth=2, relief=GROOVE)
Frame3.pack(side=LEFT, padx=10, pady=10)

# frame 4 dans frame 1
Frame4 = Frame(Frame1, borderwidth=2, relief=GROOVE)
Frame4.pack(side=LEFT, padx=10, pady=10)

# frame 5 dans frame 2
Frame5 = Frame(Frame2, borderwidth=2, relief=GROOVE)
Frame5.pack(side=LEFT, padx=10, pady=10)

# frame 6 dans frame 3
Frame6 = Frame(Frame3, borderwidth=2, relief=GROOVE)
Frame6.pack(side=LEFT, padx=10, pady=10)


# Ajout de labels
Label(Frame1, text="IMAGE", bg='#1E7FCB').pack(padx=10, pady=10)
Label(Frame4, bg='#1E7FCB').pack(padx=10, pady=10)
Label(Frame2, text="TEXTE", bg='#1E7FCB').pack(padx=10, pady=10)
Label(Frame3, text="VIDEO", bg='#1E7FCB').pack(padx=10, pady=10)
Label(Frame5, bg='#1E7FCB',width=10, height=10).pack(padx=10, pady=10)
Label(Frame6, bg='#1E7FCB').pack(padx=10, pady=10)


# #################################################"CREATION D'UN ENTRY #####################

# Création d'un widget Entry (Champ de saisie)
duree1 = IntVar()
duree1.set(0)
Champ1 = Entry(Frame1, textvariable="durée", bg ="bisque", fg="maroon", width="5")
Champ1.focus_set()
Champ1.pack(padx = 5, pady = 5)
 
# Création d'un widget Entry (Champ de saisie)
duree2 = IntVar()
duree2.set(0)
Champ2 = Entry(Frame2, textvariable="durée", bg ="bisque", fg="maroon", width="5")
Champ2.pack(padx = 5, pady = 5)


# ################################# Création d'une fonction principale pour lecteur Vidéos PyQt5 ########################
    
    
class VideoWindow(QMainWindow):
    
 def __init__(self, parent=None):
            super(VideoWindow, self).__init__(parent)
            self.setWindowTitle("LECTEUR VIDEOS PYTHON") 
    
            self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    
            videoWidget = QVideoWidget()
    
            self.playButton = QPushButton()
            self.playButton.setEnabled(False)
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.playButton.clicked.connect(self.play)
    
            self.positionSlider = QSlider(Qt.Horizontal)
            self.positionSlider.setRange(0, 0)
            self.positionSlider.sliderMoved.connect(self.setPosition)
    
            self.errorLabel = QLabel()
            self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                                          QSizePolicy.Maximum)
    
            # Creation d'une nouvelle action
            openAction = QAction(QIcon('open.png'), '&Open', self)        
            openAction.setShortcut('Ctrl+O')
            openAction.setStatusTip('Open movie')
            openAction.triggered.connect(self.openFile)
    
            # Creation d'une action existente
            exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
            exitAction.setShortcut('Ctrl+Q')
            exitAction.setStatusTip('Exit application')
            exitAction.triggered.connect(self.exitCall)
    
            # Creation d'un menu déroulant et de "ajout "
            menuBar = self.menuBar()
            fileMenu = menuBar.addMenu('&File')
            #fileMenu.addAction(newAction)
            fileMenu.addAction(openAction)
            fileMenu.addAction(exitAction)
    
            # Creation d'un widget pour la fenetre lecteur
            wid = QWidget(self)
            self.setCentralWidget(wid)
    
            # Création des mises en page à placer dans un widget

            controlLayout = QHBoxLayout()
            controlLayout.setContentsMargins(0, 0, 0, 0)
            controlLayout.addWidget(self.playButton)
            controlLayout.addWidget(self.positionSlider)
    
            layout = QVBoxLayout()
            layout.addWidget(videoWidget)
            layout.addLayout(controlLayout)
            layout.addWidget(self.errorLabel)
    
            # Définir le widget pour qu'il contienne le contenu de la fenêtre
            wid.setLayout(layout)
    
            self.mediaPlayer.setVideoOutput(videoWidget)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
            self.mediaPlayer.positionChanged.connect(self.positionChanged)
            self.mediaPlayer.durationChanged.connect(self.durationChanged)
            self.mediaPlayer.error.connect(self.handleError)
   
   
 def openFile(self):
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",QDir.homePath())
            print(fileName)
            if fileName != '':
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
                self.playButton.setEnabled(True)
                shutil.copy(fileName,"Q:\Espace d'echange\TEST_PYTHON")
 
 def exitCall(self):
  sys.exit(app.exec_()) 
    
 def play(self):
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.mediaPlayer.pause()
            else:
                self.mediaPlayer.play()
    
 def mediaStateChanged(self, state):
            if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
                self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
            else:
                self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
    
 def positionChanged(self, position):
            self.positionSlider.setValue(position)
    
 def durationChanged(self, duration):
            self.positionSlider.setRange(0, duration)
    
 def setPosition(self, position):
            self.mediaPlayer.setPosition(position)
    
 def handleError(self):
            self.playButton.setEnabled(False)
            self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
    
def video():
 
  if __name__ == '__main__':
     app = QApplication(sys.argv)
     player = VideoWindow()
     player.resize(640, 480)
     player.show()
     app.exec_()

  
# ###########################Création de la fonction inserer image #############################################

def insererimage():
    photo = askopenfilename(title="Ouvrir une image",filetypes=[('jpg files','.jpg'),('png file', '.png')])
    image = ImageTk.PhotoImage(Image.open(photo))
    canvas= Canvas(Frame4)
    canvas.create_image(100, 100,anchor =NW, image=image) 
    shutil.copy(photo,"Q:\Espace d'echange\TEST_PYTHON")
    print(photo)
    canvas.pack() 


# #########################Création de la fonction créer ######################################################


def ChoisirDate(): 
 #==== CLASSE ==============================================================================================
  
 class Calendrier(object) :
     "Classe instanciant le calendrier"
  
 #----------------------------------------------------------------------------------------------------------
  
     def __init__(self, mainframe):
         "Constructeur"
         self.mainframe = mainframe
         self.y = localtime()[0] # Current year
         self.m = localtime()[1] # Current month
         self.d = localtime()[2] # Current day
         self.c = monthcalendar(self.y, self.m) # Création de l'objet "calendrier mensuel en cours"
         self.w = datetime(self.y, self.m, self.d)
         self.w = self.w.isocalendar()[1] # Retourne un tuple avec l'année et le n° de semaine en cours
  
         self.months = ((1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'), (5, 'Mai'), (6, 'Juin'),(7, 'Juillet'), (8, 'Août'), (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre'))
  
         self.days = ('S', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di')
  
 #----------------------------------------------------------------------------------------------------------
  
     def calendrier(self) :
         # Création d'un widget Frame pour placer les widgets de la ligne 0 :
         self.subframe = Frame(self.mainframe, bg='white')
         self.subframe.grid()
  
         # Création d'un widget Frame pour placer tous les widgets Button et les noms de chaque jour :
         self.subframe2 = Frame(self.mainframe, bg='white')
         self.subframe2.grid(row=1)
  
         # Création du bouton en forme de triangle permettant d'afficher le mois précédent :
         self.left_triangle1=Button(self.subframe, bg='white', fg='#357AB7', text=u"\u25C0",bd=0,highlightthickness=0, padx=0, pady=0, activebackground='#E4E4E4', command = self.prev_month)
         self.left_triangle1.grid(row = 0, column = 0, padx = 10, sticky='w')
  
         # Création du widget Label qui affiche le mois :
         for i in range(0, len(self.months)) :
             for i2 in range(0, len(self.months[i])):
                 if self.months[i][i2] == self.m :
                     self.month=Label(self.subframe,  bg='white', text=self.months[i][i2+1], font='Times 14', padx=10,pady=10)
                     self.month.grid(row = 0, column = 1, columnspan = 2, sticky = 'w')
  
         # Création du bouton en forme de triangle permettant d'afficher le mois suivant :
         self.right_triangle1=Button(self.subframe,  bg='white', fg='#357AB7', text=u"\u25B6", bd=0,highlightthickness=0, padx = 0, pady = 0, activebackground = '#E4E4E4', command = self.next_month)
         self.right_triangle1.grid(row = 0, column = 3, padx = 10, sticky = 'w')
    
         # Création du bouton en forme de triangle permettant d'afficher l'année précédente :
         self.left_triangle2=Button(self.subframe,  bg='white', fg='#357AB7', text=u"\u25C0", bd=0, highlightthickness=0,padx=0, pady=0, activebackground = '#E4E4E4', command = self.prev_year)
         self.left_triangle2.grid(row = 0, column = 4, padx = 10, sticky = 'e')
  
         # Création du widget Label qui affiche l'année :
         self.year = Label(self.subframe,  bg='white', text = str(self.y), font = 'Times 14', padx=10, pady=10)
         self.year.grid(row = 0, column = 5, columnspan = 2, sticky = 'e')
  
         # Création du bouton en forme de triangle permettant d'afficher l'année suivante :
         self.right_triangle2=Button(self.subframe,  bg='white', fg='#357AB7', text=u"\u25B6", bd=0, highlightthickness=0,padx=0, pady=0, activebackground='#E4E4E4', command = self.next_year)
         self.right_triangle2.grid(row = 0, column = 7, padx = 10, sticky = 'e')
  
         # Création des widgets Label affichant les deux premières lettres de chaque jour de la semaine :
         for i in range(0, len(self.days)):
             self.day=Label(self.subframe2, bg='#357AB7', fg='white', text=self.days[i], padx=10, pady=10)
             self.day.grid(row = 0, column = i, sticky = 'nsew')
  
 #----------------------------------------------------------------------------------------------------------
  
     def buttons(self) :
         "Création des boutons affichant les numéros de chaque jour du mois"
         self.buttonlist = []
         self.row_numb = 1 # numéro de ligne
         self.col_numb = 1 # La colonne 0 est réservée pour les boutons affichants les numéros de semaine.
         for child in self.subframe2.winfo_children() :
             if child.winfo_class() == 'Button' :
                 child.destroy() # Destruction des éventuels boutons déjà placés.
         for i in range(0, len(self.c)) :
             self.sub_buttonlist = []
             for i2 in range(0, len(self.c[i])):
                 if self.c[i][i2] == 0 : # Si le jour est absent , itération de la colonne.
                     self.col_numb +=1
                     if self.col_numb % 8 == 0 : # A la huitième colonne, itération de la ligne.
                         self.row_numb += 1
                         self.col_numb = 1 # Nouvelle ligne : Le numéro de colonne repasse à 1.
                 else : # Création des jours proprement dits :
                     self.button = Button(self.subframe2, text = str(self.c[i][i2]), relief='flat', bd=1, bg='white', padx = 10, pady = 10)
                     self.button.grid(row = self.row_numb, column = self.col_numb, sticky ='nsew')
                     self.sub_buttonlist.append(self.button)
                     self.sub_buttonlist.append(str(self.c[i][i2]))
                     self.buttonlist.append(self.sub_buttonlist)
                     self.sub_buttonlist = []
                     # Le bouton du jour courant est bleu :
                     if self.c[i][i2] == self.d and self.m == localtime()[1] and self.y == localtime()[0] :
                         self.button.configure(bg='#357AB7', fg='white')
                         self.row_curweek = self.row_numb # Récupération de la rangée de la semaine en cours
                     self.col_numb += 1
                     if self.col_numb % 8 == 0 :
                         self.row_numb += 1
                         self.col_numb = 1
                     self.last_row = self.row_numb # Valeur de la dernière ligne
         # Appel de la méthode pages du module Agenda. 
         for i in range(0, len(self.buttonlist)):
             # Création de l'objet "agenda" et configuration de la commande de chaque bouton :
             self.d = int(self.buttonlist[i][0]['text'])
             self.agenda = Agenda(self.d, self.m, self.y)
             self.buttonlist[i][0]['command'] = self.agenda.pages
  
 #----------------------------------------------------------------------------------------------------------
  
     def current_week(self) :
         "Affichage des n° de semaines du mois en cours"
         i = self.row_curweek # Variables D'itération
         self.curweek = datetime(self.y, self.m, self.d)
         self.curweek = self.curweek.isocalendar()[1] # Retourne l'année et le n° de semaine en cours.
         while i >= 1 : # Création des boutons avec les n° de semaine --> direction passé
             self.week = Button(self.subframe2, bg='#357AB7',fg='white',text=str(self.curweek), padx=10, pady=10)
             self.week.grid(row = i, column = 0, sticky = 'nsew')
             self.curweek -= 1          
             i -= 1
  
         i = self.row_curweek + 1
         self.curweek = datetime(self.y, self.m, self.d)
         self.curweek = self.curweek.isocalendar()[1] + 1 # Réinitialisation de la variable.
         while i <= self.last_row : # Création des boutons avec les n° de semaine --> direction futur
             self.week = Button(self.subframe2, bg='#357AB7',fg='white',text=str(self.curweek), padx=10, pady=10)
             self.week.grid(row = i, column = 0, sticky = 'nsew')
             self.curweek += 1          
             i += 1
  
 #----------------------------------------------------------------------------------------------------------
  
     def weeks(self) :
         "Affichage des n° de semaine du mois précédent ou du mois suivant"
         self.row = 1
         for i in range(0, len(self.c)): # Boucle de 0 jusqu'au nombre de semaines dans le mois courant.
             i2 = 0
             while i2 < len(self.c[i]): # Boucle de 0 jusqu'au nombre de jours dans chaque semaine du mois.
                 if self.c[i][i2] != 0  :
                     self.curweek = datetime(self.y, self.m, self.c[i][i2])
                     break # Interruption de la boucle si la valeur est != 0
                 i2 += 1
             self.curweek = self.curweek.isocalendar()[1] # Réinitialisation de la variable.
             # Création des nouveaux boutons de semaines :
             self.week = Button(self.subframe2, bg='#357AB7',fg='white',text=str(self.curweek), padx=10, pady=10)
             self.week.grid(row = self.row, column = 0, sticky = 'nsew')
             self.row +=1
  
 #----------------------------------------------------------------------------------------------------------
  
     def prev_month(self) :
         "Affiche le mois précédent"
        
         if self.m == 1 :
             self.m = 12
             self.y -= 1
             self.month['text'] = self.months[11][1]
             self.c = monthcalendar(self.y, 12)
             self.year.configure(text = str(self.y))
             self.buttons()
             self.weeks()
  
         else :
             self.m-=1
             self.month['text'] = self.months[self.m-1][1]
             self.c = monthcalendar(self.y, self.m)
             self.buttons()
             self.weeks()
  
 #----------------------------------------------------------------------------------------------------------
  
     def next_month(self) :
         "Affiche le mois suivant"
        
         if self.m == 12 :
             self.m = 1
             self.y += 1
             self.month['text'] = self.months[0][1]
             self.c = monthcalendar(self.y, self.m)
             self.year.configure(text = str(self.y))
             self.buttons()
             self.weeks()
  
         else :
             self.m += 1
             self.month['text'] = self.months[self.m-1][1]
             self.c = monthcalendar(self.y, self.m)
             self.buttons()
             self.weeks()
  
 #----------------------------------------------------------------------------------------------------------
  
     def prev_year(self) :
         "Recul d'une année dans le passé"
         # Compréhension de liste. La méthode prev_month et activée 12 fois :
         [self.prev_month() for i in range(12)]
  
 #----------------------------------------------------------------------------------------------------------
  
     def next_year(self) :
         "Projection d'une année dans le futur"
         # Compréhension de liste. La méthode next_month et activée 12 fois :    
         [self.next_month() for i in range(12)]
    
 #=========== MAIN PROGRAMM ================================================================================
  
 if __name__ == "__main__":
     fenetre = Tk()
     fenetre.title('Date et Jour')
     mainframe = Frame(fenetre, bg='white')
     mainframe.grid()
     calendrier = Calendrier(mainframe)
     calendrier.calendrier()
     calendrier.buttons()
     calendrier.current_week()
  
     fenetre.mainloop() # Démarrage du réceptionnaire d'événements   
    
    
# ##########################Création de la fonction A propos ##################################################


def apropos():
    showinfo("A propos", "Cette application a été créée par M. Adrien MARIE dans le cadre du projet BTS SN IR : AFFICHAGE NUMERIQUE. Elle est actuellement en développement.")
    

# ##########################Création de la fonction televerser ################################################


def televerser():
    
    HOST = "192.168.0.74"
    PORT = "80"
    
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        socket.connect((HOST,PORT))
        print("Client connecté !...")
        data="Client Python IHM Projet Affichage Numérique connecté !..."
        data = data.encode("utf8")
        socket.sendall(data)
    
    except:
        print("Connexion au serveur échoué!")


        
# ##################################################Création fonction ajouter texte #####################################################


def convert_pdf_to_txt():
 path = askopenfilename(title="Ouvrir un document",filetypes=[('Fichier PDF','.pdf')])
 rsrcmgr = PDFResourceManager()
 retstr = StringIO()
 codec = 'utf-8'
 laparams = LAParams()
 device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
 
 fp = open(path, 'rb')
 interpreter = PDFPageInterpreter(rsrcmgr, device)
 password = ""
 maxpages = 0
 caching = True
 pagenos=set()

 for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
  interpreter.process_page(page)

 text = retstr.getvalue()
 Label(Frame5, text=fp).pack(padx=10, pady=10)
 print(path)
 shutil.copy(path,"Q:\Espace d'echange\TEST_PYTHON")
 fp.close()
 device.close()
 retstr.close()
 return text 
    






# ################################"CREATION FICHIER XML ##################################################

def generer() :
 
 scenario = minidom.Document()

 xml = scenario.createElement('scenario')
 scenario.appendChild(xml)

 info = scenario.createElement('info')
 xml.appendChild(info)

 element = scenario.createElement('dateactivite')
 element.appendChild(scenario.createTextNode('04-03-2019'))
 info.appendChild(element)

 element = scenario.createElement('hdebut')
 element.appendChild(scenario.createTextNode('16:00'))
 info.appendChild(element)

 element = scenario.createElement('hfin')
 element.appendChild(scenario.createTextNode('13:00'))
 info.appendChild(element)

 element = scenario.createElement('cheminfichier')
 element.appendChild(scenario.createTextNode('chemin/du/fichier/choisit'))
 info.appendChild(element)

 element = scenario.createElement('ecranconcerne')
 element.appendChild(scenario.createTextNode('ecranprincipale'))
 info.appendChild(element)


 elements = scenario.createElement('image')
 xml.appendChild(elements)

 element1 = scenario.createElement('nom')
 element1.appendChild(scenario.createTextNode('Adrien_image'))
 elements.appendChild(element1)

 element1 = scenario.createElement('chemin')
 element1.appendChild(scenario.createTextNode('chemin'))
 elements.appendChild(element1)
 
 element1 = scenario.createElement('type')
 element1.appendChild(scenario.createTextNode('JPEG'))
 elements.appendChild(element1) 

 element1 = scenario.createElement('duree')
 element1.appendChild(scenario.createTextNode('3sec'))
 elements.appendChild(element1)


 elements2 = scenario.createElement('TEXTE')
 xml.appendChild(elements2)

 element2 = scenario.createElement('nom')
 element2.appendChild(scenario.createTextNode('Adrien_texte'))
 elements2.appendChild(element2)

 element2 = scenario.createElement('chemin')
 element2.appendChild(scenario.createTextNode('fichiertexte'))
 elements2.appendChild(element2)
 
 element2 = scenario.createElement('type')
 element2.appendChild(scenario.createTextNode('PDF'))
 elements2.appendChild(element2) 

 element2 = scenario.createElement('duree')
 element2.appendChild(scenario.createTextNode('5sec'))
 elements2.appendChild(element2)


 elements3 = scenario.createElement('VIDEOS')
 xml.appendChild(elements3)

 element3 = scenario.createElement('nom')
 element3.appendChild(scenario.createTextNode('eee'))
 elements3.appendChild(element3)

 element3 = scenario.createElement('chemin')
 element3.appendChild(scenario.createTextNode('fichiervideo'))
 elements3.appendChild(element3)
 
 element3 = scenario.createElement('type')
 element3.appendChild(scenario.createTextNode('MP4'))
 elements3.appendChild(element3) 

 element3 = scenario.createElement('duree')
 element3.appendChild(scenario.createTextNode('10.5sec'))
 elements3.appendChild(element3)



 elements4 = scenario.createElement('DESCRIPTION')
 xml.appendChild(elements4)

 element4 = scenario.createElement('duree')
 element4.appendChild(scenario.createTextNode('18.5sec'))
 elements4.appendChild(element4)
 
 element4 = scenario.createElement('type')
 element4.appendChild(scenario.createTextNode('entré brute'))
 elements4.appendChild(element4) 


 xml_str = scenario.toprettyxml(indent ="\t")

 fichier_xml = "scenariotype1.xml"
 with open(fichier_xml, "w") as f:
  f.write(xml_str)

# ###############################Création du bouton TELEVERSER ###############################################
          
          
boutonGenerer = Button(fenetre, text="Envoyer",bg='#FBF2B7',cursor="circle", command = televerser) 
boutonGenerer.pack(side=BOTTOM, padx=10, pady=10)
boutonGenerer2 = Button(fenetre, text="generer",bg='#FBF2B7',cursor="circle", command = generer) 
boutonGenerer2.pack(side=BOTTOM, padx=10, pady=10)
  
  
  
  # ##################################Création d'un menu déroulant #############################################
      
menubar= Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Ouvrir une image", command=insererimage)
menu1.add_command(label="Date", command=ChoisirDate)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)
  
  
menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Créer")
menu2.add_command(label="Parcourir")
menu2.add_command(label="Enregistrer")
menubar.add_cascade(label="Editer", menu=menu2)
  
menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=apropos)
menubar.add_cascade(label="Aide", menu=menu3)
              


# ##################### Création des boutons Ajouter pour chaque tâches ################################################

BoutonSup1= Button(Frame3, text ='Ajouter Vidéo',bg='#79F8F8',command = video).pack(side=LEFT, padx=5, pady=5)
BoutonVal1 = Button(Frame2, text ='Ajouter du Texte',bg='#79F8F8', command=convert_pdf_to_txt).pack(side=RIGHT, padx=5, pady=5)

AjouterImage= Button(Frame1, text ='Ajouter une Image',bg='#79F8F8', command=insererimage).pack(side=LEFT, padx=5, pady=5)
SupprimerImage= Button(Frame1, text ='Supprimer une Image',bg='#79F8F8').pack(side=RIGHT, padx=5, pady=5)

fenetre.config(menu=menubar)


                
fenetre.mainloop() # Boucle de la page pour qu'elle reste ouverte
