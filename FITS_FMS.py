#To note the filenames of .fits files in a folder
#To extract metadata from a from the .fits files, 

from astropy.io import fits
import sqlite3
import os
import random
import sys
import time
import logging
import pickle
import os.path

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QFileDialog,
    QLabel,
    QMainWindow,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QProgressBar,
    QTextEdit,
    QTextBrowser,
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlDatabase

from FITSMetaDB26_ui import Ui_MainWindow

global logfolder
logfolder = os.getenv('LOCALAPPDATA') + '\FITS_DB\\'
# checking if the directory demo_folder  
# exist or not. 
print (logfolder)
if not os.path.exists(logfolder): 
      
    # if the demo_folder directory is not present  
    # then create it. 
    os.makedirs(logfolder) 
logfile = logfolder + 'FITS_DB.log'    
logging.basicConfig(filename=logfile, encoding='utf-8',filemode='w', level=logging.DEBUG)




global DB_folder 
global root_folder 
#DB_folder = 'c:'
#root_folder = 'c:'
#if not os.path.exists('sample'):
#    os.mkdir('sample')
settingsfile = logfolder + 'folder.pkl'
if(os.path.exists(settingsfile)) :
        with open(settingsfile, 'rb') as file:
             DB_folder, root_folder = pickle.load(file)
else:
     DB_folder = "c:"
     root_folder = "c:"

    
    
#######################
class help_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help information")
        self.setGeometry(50, 50, 800, 700)

        self.text_edit = QTextBrowser(self)
        self.text_edit.setGeometry(50, 50, 700, 600)

        help_file = 'fits_helpfile.txt'
        
        if os.path.isfile(help_file):
            with open(help_file, "r") as f:
                file_contents = f.read()
                self.text_edit.setPlainText(file_contents)
        else:
            print("File does not exist.")

########################
class AnotherWindow(QMainWindow):    #QWidget):
    """
    This "window" is a QMainWindow (QWidget). If it has no parent, it
    will appear as a free-floating window.
    """

    def __init__(self):
        super().__init__()
        #imported from tableview_querymodel_search.py
        #layout = QVBoxLayout()
        #self.label = QLabel("Another Window")  # <2>
        #layout.addWidget(self.label)
        #self.setLayout(layout)

        global DB_folder
        basedir = os.path.dirname(__file__)
        basedir2 = DB_folder
        #def changeWord(word):
        for letter in basedir2:     # Use "\\" for windows.
            if letter == "/":
                 basedir2 = basedir2.replace(letter,"\\")
        
        db = QSqlDatabase.addDatabase("QSQLITE")
        #db = QSqlDatabase("QSQLITE")
        #db.setDatabaseName("mydatabase.db")
        db.setDatabaseName(os.path.join(basedir2 + "\\metadata.db"))
            #db.open()    
            #db = QSqlDatabase("QSQLITE")
        
        if db.isOpen() != True:
             db.open()
        
       
        container = QWidget()
        layout_search = QHBoxLayout()

        self.h_file_name = QLineEdit()
        self.h_file_name.setPlaceholderText("Dir and file name...")
        self.h_file_name.textChanged.connect(self.update_query)
        
        self.h_keyword = QLineEdit()
        self.h_keyword.setPlaceholderText("Keyword..")
        self.h_keyword.textChanged.connect(self.update_query)
        
        self.h_value = QLineEdit()
        self.h_value.setPlaceholderText("Value of keyword...")
        self.h_value.textChanged.connect(self.update_query)
        
        layout_search.addWidget(self.h_file_name)
        layout_search.addWidget(self.h_keyword)
        layout_search.addWidget(self.h_value)

        layout_view = QVBoxLayout()
        layout_view.addLayout(layout_search)

        self.table = QTableView()

        layout_view.addWidget(self.table)

        container.setLayout(layout_view)

        self.model = QSqlQueryModel()
        self.table.setModel(self.model)

        self.query = QSqlQuery(db=db)

        self.query.prepare(
            "SELECT fileName.LNaam,  keyword, value FROM metadata "
            "INNER JOIN fileName on metadata.fileName_id=fileName.id WHERE "
            "fileName.LNaam LIKE '%' || :file_name || '%' AND "
            "metadata.keyword LIKE '%' || :fits_keyword || '%' AND "
            "metadata.value LIKE '%' || :key_value || '%'"
        )
            

        self.update_query()
        self.setMinimumSize(QSize(1024, 600))
        self.setCentralWidget(container)

    def update_query(self, s=None):

        # Get the text values from the widgets.
        file_name = self.h_file_name.text()
        fits_keyword = self.h_keyword.text()
        key_value = self.h_value.text()

        self.query.bindValue(":file_name", file_name)
        self.query.bindValue(":fits_keyword", fits_keyword)
        self.query.bindValue(":key_value", key_value)
        print(file_name)

        self.query.exec()
        self.model.setQuery(self.query)



#######################

        ##############################
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.w = None  # No external window yet. 
        self.show()
        self.help_window = None

        self.pushButton_help.clicked.connect(self.open_help_window)

        self.pushButton_view_DB.clicked.connect(self.show_new_window)

        self.label_root_folder.setText(str(root_folder))
        self.label_folder_db.setText(str(DB_folder))
        self.pushButton_create_db.pressed.connect(self.create_db)
        self.pushButton_root_folder.pressed.connect(self.set_root_folder)
        db_folder2 = self.pushButton_Folder_db.clicked.connect(self.set_db_folder)
    ######################
    def open_help_window(self):
        if self.help_window == None:
            self.help_window =  help_window()                        #AnotherWindow()
            self.help_window.show()
            return self.w
        else:
            self.help_window.close()
            self.help_window=None
        
        # Add a label to the window
        self.label = QLabel("This is the help_window", self)
        self.label.move(50, 50)
#################################


    def show_new_window(self, checked):
         
        #  self.w = None
        #  self.w = AnotherWindow()
        if self.w is None:
            self.w = AnotherWindow()
            self.w.show()
            return self.w
           
        else:
            self.w.close()
            self.w=None
       
        
        ###############################################################      
    def set_db_folder(self):
            global DB_folder
            DB_folder = self.get_folder()
            self.label_folder_db.setText(str(DB_folder))
            self.save_folders()
            return 
        ###############################################################
    def set_root_folder(self):
            global root_folder
            root_folder = self.get_folder()
            self.label_root_folder.setText(str(root_folder))
            self.save_folders()
            return
        #############################

        # tag::get_folder[]
    def get_folder(self):
        caption = ""  # Empty uses default caption.
        initial_dir = ""  # Empty uses current folder.
        folder_path = QFileDialog.getExistingDirectory(
            self,
            caption=caption,
            directory=initial_dir,
        )
        print("Result:", folder_path)
        return folder_path
        
    
    def save_folders(self) :
         global logfolder
         global DB_folder
         global root_folder
         settingsfile = logfolder + 'folder.pkl'
         print(str(logfolder))
         #if(os.path.exists(settingsfile)) :
              # Pickling the variable
         with open(settingsfile, 'wb') as file:
                      pickle.dump([DB_folder, root_folder], file)
                      
         return   

    def reset(self):
        self.current_value = 0
        self.progressBar.reset()        

    def progress(self):
        if self.current_value  <= self.progressBar.maximum():
            self.current_value += 1
            self.progressBar.setValue(self.current_value) 
        else :
             self.reset()

    def toggle_window(self, checked):
        if self.w.isVisible():
            self.w.hide()
        else:
            self.w.show()

    def create_db(self):
        global DB_folder
        global root_folder
        # Connect to the database
        #print('in create_db, DSBfolder = ' + DB_folder)

        db_file = DB_folder +'/metadata.db'
        print(db_file)
        conn = sqlite3.connect(db_file)    #'d:/_d/fits_meta/metadata.db')
        cur = conn.cursor() 
        
        cur.execute(''' CREATE TABLE IF NOT EXISTS fileName
                (id INTEGER PRIMARY KEY ,
                LNaam    TEXT) ''')
        cur.execute(''' select * from filename ''')
        cur.execute(''' DELETE FROM filename ''')
                
        cur.execute('''CREATE TABLE IF NOT EXISTS metadata
                (id             integer primary key, 
                keyword        TEXT,
                value         TEXT,  
                fileName_id   INTEGER NOT NULL,
                FOREIGN KEY(fileName_id) REFERENCES fileName(id));''')
        cur.execute(''' select * from metadata ''')
        cur.execute(''' DELETE FROM metadata ''')
                            
        conn.commit()
        #conn.close()
        
        ###############################

        # Loop over all the FITS files in the directory

        #root = root_folder   #"d:/_foto_a/"
        
        cur = conn.cursor() 
        self.reset()
        for path, subdirs, files in os.walk(root_folder):
            for name in files:
                if (name.endswith('.fits') or name.endswith('.fts') or name.endswith('.fit')) : # or name.endswith('.xisf')):
                        #print(path, "   ", subdirs, "   ", name)
                        #os.chdir(root)
                        os.path.normcase(path)
                        name = os.path.join(path, name)
                        logging.info(name)   #write filename to logfile
                        #print(name)
                        self.progress()
                            #self.label_create_db_activity.setText(str(name))
                        #self.label_create_db_activity.setText(str(name))
                        #time.sleep(0.1)
                        #print(DB_folder)
                        hdul = fits.open(name)  #- slegs vir .fits leers
                        hdul.verify('fix+ignore')              #
                        header = hdul[0].header
                        
                        #print(header)
                        
                    # Insert the metadata into the tables
                    # Insert filename
                    # cur.execute("INSERT INTO fileName LNaam VALUES(name, )")
                        cur.execute("INSERT INTO fileName (LNaam) VALUES (?)", [name])
                        
                        self.progress
                    #kry Filename_id
                        indeks=(cur.lastrowid)
                        #print(" rowid = ",indeks)
                    #Insert key and value and fileName_id
                        for keyword, value in header.items():
                            cur.execute("INSERT INTO metadata (keyword, value, filename_id) VALUES (?,?,?)", (keyword, str(value), indeks))
                                                


                    # Close the FITS file
                        hdul.close()

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        self.progressBar.setValue(self.progressBar.maximum())

        return

        
     #    self.w = None # Discard reference, close window.
   
    #####################################################    
 

app = QApplication(sys.argv)
w = MainWindow()

app.exec()

#  self.textBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
#         self.textBrowser.setGeometry(QtCore.QRect(100, 170, 701, 192))
#         self.textBrowser.setSource(QtCore.QUrl("file:///D:/_d/FITS_Meta/QHelpFile.htm"))
#         self.textBrowser.setOpenLinks(False)
#         self.textBrowser.setObjectName("textBrowser")
