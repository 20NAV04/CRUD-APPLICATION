import MySQLdb
import tkinter as tk
from tkinter import ttk
import MySQLdb._exceptions

db = None

class InputError(Exception):
    def __init__(self, message):
        super().__init__(message)

class LoginGUI:
    host = ""
    user = ""
    password = ""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("300x250")
        self.root.title("CRUD Application Login")
        self.root.resizable(False, False)

        self.root.rowconfigure(0,weight=1)
        self.root.columnconfigure(0,weight=1)

        self.frame = tk.Frame(self.root)
        self.frame.grid(column = 1, row = 0)
        self.frame.columnconfigure(0, weight=1)
        for i in range (6):
            self.frame.rowconfigure(i, weight=1)

        self.hostLabel = tk.Label(self.frame, text="Enter Host Name")
        self.hostLabel.grid(column=0, row=0)
        self.hostForm = tk.Entry(self.frame)
        self.hostForm.grid(column=1, row=0, padx=5,pady=5)

        self.userLabel = tk.Label(self.frame, text="Enter User Name")
        self.userLabel.grid(column=0, row=1)
        self.userForm = tk.Entry(self.frame)
        self.userForm.grid(column=1, row=1, padx=5,pady=5)

        self.passLabel = tk.Label(self.frame, text="Enter Password")
        self.passLabel.grid(column=0, row=2)
        self.passForm = tk.Entry(self.frame)
        self.passForm.grid(column=1, row=2, padx = 5, pady = 5)

        self.submitCredentials = tk.Button(self.frame, text="Submit", command=self.attemptLogin)
        self.submitCredentials.grid(column = 0, row = 3, sticky="ew", columnspan = 2)
        
        self.status = tk.Label(self.frame, wraplength=250)
        self.status.grid(column=0,row=4, columnspan = 2, rowspan=2)

    def attemptLogin(self):
        self.host = self.hostForm.get()
        self.user = self.userForm.get()
        self.password = self.passForm.get()
        global db
        try:
            db = MySQLdb.connect(self.host, self.user, self.password)
            self.root.quit()
            self.root.destroy()
        except MySQLdb.Error as err:
            self.status.config(text=err.args[1])
       
    
LoginGUI().root.mainloop()


class mainGUI:
    databaseList = []
    tableList = ["Select Table"]
    fieldList = []
    fieldTypes = []
    recordList = []
    keyNames = []
    keyIndexes = []
    forms = []
    fieldAmount = None
    PPWForms = []
    CreateTablePKs = []
    CreateTableFKs = []
    selectedEntry = None
    typeMapping = {
        'bigint': int,
        'bit': bool,
        'char': str,
        'date': "date",
        'datetime': "date",
        'decimal': float,
        'float': float,
        'int': int,
        'longtex': str,
        'mediumint': int,
        'mediumtext': str,
        'smallint': int,
        'text': str,
        'time': "date",
        'tinyint': int,
        'tinytext': str,
        'varchar': str,
        'double': float,
        'timestamp': "date"
    }
    
    def __init__(self):
        '''MAIN WINDOW'''
        self.selectDatabases()
        self.root = tk.Tk()
        self.root.geometry("1200x600")
        self.root.title("CRUD Application")
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        '''LEFT FRAME'''
        self.lframe = tk.Frame(self.root)
        self.lframe.grid(column=0,row=0, sticky="news")
        self.lframe.grid_propagate(False)

        self.lframe.columnconfigure(0, weight=1)
        self.lframe.rowconfigure(0, weight=1)
        self.lframe.rowconfigure(1, weight=3)
        self.lframe.rowconfigure(2, weight=1)

        self.header = tk.Frame(self.lframe)
        self.header.grid(column=0,row=0, sticky = "news")
        self.header.grid_propagate(False)
        self.header.rowconfigure(0, weight = 3)
        self.header.rowconfigure(1, weight = 1)
        self.header.columnconfigure(0, weight = 0)

        self.title = tk.Label(self.header, text = "CRUD APPLICATION", font = ("TKDefaultFont", 25))
        self.title.grid(row = 0, column = 0)

        self.note = tk.Label(self.header, text = "For adding and updating values, blank fields are interpreted as NULL.  For searching values, blank fields are not included; type NULL for filtering NULL values. Select a record on the right to update and delete", wraplength=550)
        self.note.grid(column = 0, row = 1, sticky = "news", padx = 25)

        self.formframe = tk.Frame(self.lframe)
        self.formframe.grid(column=0, row=1, sticky="news")
        self.formframe.rowconfigure(0, weight=1)
        self.formframe.columnconfigure(0, weight=1)
        self.formframe.columnconfigure(1)
        self.formframe.grid_propagate(False)

        self.formCanvas = tk.Canvas(self.formframe)
        self.formCanvas.grid(column=0, row=0, sticky="news")
        self.formCanvasScrollbar = ttk.Scrollbar(self.formframe, orient="vertical", command=self.formCanvas.yview)
        self.formCanvasScrollbar.grid(column=1,row=0,sticky="ns")

        self.formframePH = tk.Label(self.formCanvas, text="Input forms will appear here after selecting a table.")
        self.formframePH.pack(expand=True)
        
        self.controlframe = tk.Frame(self.lframe)
        self.controlframe.grid(column=0, row=2, sticky="news")
        self.controlframe.grid_propagate(False)

        self.controlframe.columnconfigure(0, weight=1)
        self.controlframe.columnconfigure(1, weight=1)
        self.controlframe.columnconfigure(2, weight=1)
        self.controlframe.columnconfigure(3, weight=1)
        self.controlframe.rowconfigure(0, weight=1)

        self.addRecBtn = tk.Button(self.controlframe, text="Add Record", command =self.addRec)
        self.addRecBtn.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.delRecBtn = tk.Button(self.controlframe, text="Delete Record", command=self.delRec)
        self.delRecBtn.grid(row=0, column=1, padx=10, pady=10, sticky="news")
        self.updateRecBtn = tk.Button(self.controlframe, text="Update Record", command=self.updateRec)
        self.updateRecBtn.grid(row=0, column=2, padx=10, pady=10, sticky="news")
        self.searchRecBtn = tk.Button(self.controlframe, text="Search Record", command=self.selectRec)
        self.searchRecBtn.grid(row=0, column=3, padx=10, pady=10, sticky="news")
      

        '''RIGHT FRAME'''
        self.rframe = tk.Frame(self.root, bg="blue")
        self.rframe.grid(column=1,row=0, sticky="news")
        self.rframe.grid_propagate(False)

        self.rframe.columnconfigure(0, weight=1)
        self.rframe.rowconfigure(0, weight=1)
        self.rframe.rowconfigure(1, weight=5)

        self.navframe = tk.Frame(self.rframe)
        self.navframe.grid(column=0, row=0, sticky="news")
        self.navframe.grid_propagate(False)
        self.navframe.rowconfigure(0,weight=1)
        for x in range (3):
            self.navframe.columnconfigure(x,weight=1)

        self.navframeButtons = tk.Frame(self.navframe)
        self.navframeButtons.grid(row = 0, column = 0, sticky="news")
        self.navframeButtons.rowconfigure(0, weight = 1)
        self.navframeButtons.rowconfigure(1, weight = 1)
        self.navframeButtons.columnconfigure(0, weight = 1)
        self.navframeButtons.columnconfigure(1, weight = 1)

        self.addDBBtn = tk.Button(self.navframeButtons, text="Add Database", command = self.popupAddDB)
        self.addDBBtn.grid(column=0, row=0, sticky="ew", padx=5, pady=5)

        self.delDBBtn = tk.Button(self.navframeButtons, text="Delete Database", command = self.popupDelDB)
        self.delDBBtn.grid(column=1, row=0, sticky="ew", padx=5, pady=5)

        self.addTableBtn = tk.Button(self.navframeButtons, text="Add Table", command = self.createTable, state = tk.DISABLED)
        self.addTableBtn.grid(column=0, row=1, sticky="ew", padx = 5)

        self.delTableBtn = tk.Button(self.navframeButtons, text="Delete Table", command = self.popupDelTable, state = tk.DISABLED)
        self.delTableBtn.grid(column=1, row=1, sticky="ew", padx = 5)

        self.selectedDB = tk.StringVar()
        self.selectedDB.set("Select Database")
        self.dbDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedDB, values=self.databaseList, state="readonly")
        self.dbDrpDwn.grid(column=2, row=0, sticky="ew", padx=5)
        self.selectedDB.trace_add('write', self.onDatabaseChange)

        self.selectedTable = tk.StringVar()
        self.selectedTable.set("Select Table")
        self.tableDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedTable, values=self.tableList, state="readonly")
        self.tableDrpDwn.grid(column=3, row=0, sticky="ew", padx=5)
        self.selectedTable.trace_add('write', self.onTableChange)

        self.dataframe = tk.Frame(self.rframe, bg="white")
        self.dataframe.grid(column=0, row=1, sticky="news")
        self.dataframe.grid_propagate(False)
        self.dataframe.rowconfigure(0, weight=1)
        self.dataframe.rowconfigure(1)
        self.dataframe.columnconfigure(0, weight=1)
        self.dataframe.columnconfigure(1)

        self.dataframePH = tk.Label(self.dataframe, text="Select a Database and a Table to Start.", bg="white")
        self.dataframePH.place(anchor="center", relx=.5,rely=.5)

    def selectDatabases(self):
        c = db.cursor()
        c.execute("SHOW DATABASES;")
        options = c.fetchall()
        for option in options:
            self.databaseList.append(option[0])
        c.close()

    def onDatabaseChange(self,p1,p2,p3):
        try:
            self.innerFFrame.destroy()
        except:
            pass
        try:
            self.formframePH.destroy()
        except:
            pass
        self.formframePH = tk.Label(self.formCanvas, text="Input forms will appear here after selecting a table.")
        self.formframePH.pack(expand=True)
        
        self.destroyDisplay()
        self.dataframePH = tk.Label(self.dataframe, text="Select a Database and a Table to Start.", bg="white")
        self.dataframePH.place(anchor="center", relx=.5,rely=.5)

        if self.selectedDB.get() == "Select Database":
            self.addTableBtn['state'] = tk.DISABLED
            self.delTableBtn['state'] = tk.DISABLED
        elif self.selectedDB.get() != "Select Database":
            self.addTableBtn['state'] = tk.NORMAL
            self.delTableBtn['state'] = tk.NORMAL
            
            c = db.cursor()
            c.execute("USE {}".format(self.selectedDB.get()))
            c.close()
            self.selectTables()

    def selectTables(self):
        self.tableList = []
        c = db.cursor()
        c.execute("SHOW TABLES;")
        options = c.fetchall()
        for option in options:
            self.tableList.append(option[0])
        c.close()
        self.recreateTableDrp()
    
    def recreateTableDrp(self):
        self.tableDrpDwn.destroy()
        self.selectedTable.set("Select Table")
        self.tableDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedTable, values=self.tableList, state="readonly")
        self.tableDrpDwn.grid(column=3, row=0, sticky="ew")

    def popupAddDB(self):
        try:
            self.winDelDB.destroy()
        except:
            pass
        
        try:
            self.alertPopup.destroy()
        except:
            pass
    
        self.alertPopup = tk.Toplevel(self.root)
        self.alertPopup.title("Add Database")
        self.alertPopup.geometry = ("300x250")
        self.alertPopup.resizable(False, False)
        self.alertPopupL = tk.Label(self.alertPopup, text="Database Name:")
        self.alertPopupL.grid(column=0,row=0,sticky="news", padx=5, pady=5)
        self.alertPopupE = tk.Entry(self.alertPopup)
        self.alertPopupE.grid(column=1,row=0,sticky="news", padx=5, pady=5)
        self.alertPopupBtn = tk.Button(self.alertPopup, command = self.addDB, text="Add")
        self.alertPopupBtn.grid(column=0,row=1, columnspan=2, sticky="news", padx=5, pady=5)
        self.addDBError = tk.Label(self.alertPopup, wraplength=250)
        self.addDBError.grid(column=0, row=2, rowspan=2, columnspan=2, padx=5, pady=5)
        self.alertPopup.mainloop()
   
    def popupDelDB(self):
        try:
            self.alertPopup.destroy()
        except:
            pass
        
        try:
            self.winDelDB.destroy()
        except:
            pass

        self.winDelDB = tk.Toplevel(self.root)
        self.winDelDB.title("Delete Database")
        self.winDelDB.geometry = ("300x250")
        self.winDelDB.resizable(False, False)
        self.winDelDBL = tk.Label(self.winDelDB, text="Choose Database: ")
        self.winDelDBL.grid(column=0, row=0, sticky="news", padx=5,pady=5)
        self.toDel = tk.StringVar()
        self.dbDrpDwn = ttk.Combobox(self.winDelDB, textvariable=self.toDel, values=self.databaseList, state="readonly")
        self.dbDrpDwn.grid(column=1,row=0, padx=5,pady=5,sticky="news")
        self.winDelDBBtn = tk.Button(self.winDelDB, command = self.delDB, text="Delete")
        self.winDelDBBtn.grid(column=0,row=1, columnspan=2, sticky="news", padx=5, pady=5)
        self.delDBError = tk.Label(self.winDelDB, wraplength=250)
        self.delDBError.grid(column=0, row=2, rowspan=2, columnspan=2, padx=5, pady=5)
        self.winDelDB.mainloop()

    def addDB(self):
        c = db.cursor()
        try:
            if '`' in self.alertPopupE.get():
                raise InputError("` is not allowed in input.")
            if ' ' in self.alertPopupE.get():
                raise InputError("Spaces are not allowed in input.")
            if ';' in self.alertPopupE.get():
                raise InputError("; is not allowed in input")
            c.execute("CREATE DATABASE %s;" % (self.alertPopupE.get()))
            c.close()
            self.alertPopup.destroy()
            self.recreateDBDrp()
        except MySQLdb.Error as err:
            c.close()
            self.addDBError.config(text=err.args[1])
        except InputError as err:
            c.close()
            self.addDBError.config(text=err)

    def delDB(self):
        c = db.cursor()
        try:
            c.execute("DROP DATABASE %s;" % (self.toDel.get()))
            c.close()
            self.winDelDB.destroy()
            self.recreateDBDrp()
            self.selectedDB.set("Select Database")
            self.tableList = []
            self.recreateTableDrp()
        except MySQLdb.Error as err:
            c.close()
            self.delDBError.config(text=err.args[1])
      
    def recreateDBDrp(self):
        self.databaseList = []
        self.selectDatabases()
        self.dbDrpDwn.destroy()
        self.dbDrpDwn = ttk.Combobox(self.navframe, textvariable=self.selectedDB, values=self.databaseList, state="readonly")
        self.dbDrpDwn.grid(column=2, row=0, sticky="ew", padx=5)

    def getPrimaryKey(self, dbname, tablename):
        self.keyNames = []
        c = db.cursor()
        c.execute("""SELECT k.column_name
        FROM information_schema.table_constraints t
        JOIN information_schema.key_column_usage k
        USING(constraint_name, table_schema, table_name)
        WHERE t.constraint_type="PRIMARY KEY"
        AND t.table_schema= "%s"
        AND t.table_name= "%s";
        """ % (dbname, tablename))
        for key in c.fetchall():
            self.keyNames.append(key[0])
        c.close()

    def onTableChange(self,p1,p2,p3):
        if(self.selectedTable.get() != "Select Table"):
            self.getPrimaryKey(self.selectedDB.get(), self.selectedTable.get())
            self.fetchColumns()
            self.fetchRecords()
            self.fetchDataType()
            self.destroyDisplay()
            self.createDisplay()
            self.createForms()
    
    def fetchColumns(self):
        self.fieldList = []
        self.keyIndexes = []
        c = db.cursor()
        c.execute("""SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = "%s" 
        AND TABLE_NAME = "%s" ORDER BY ORDINAL_POSITION;""" % (self.selectedDB.get(), self.selectedTable.get())) 
        
        for index, column in enumerate(c.fetchall()):
            self.fieldList.append(column[0])
            if column[0] in self.keyNames:
                self.keyIndexes.append(index)
        c.close()

    def fetchRecords(self):
        self.recordList = []
        c = db.cursor()
        c.execute("SELECT * FROM %s;" % (self.selectedTable.get()))
        for data in c.fetchall():
            self.recordList.append(data)
        c.close()

    def fetchDataType(self):
        self.fieldTypes = []
        c = db.cursor()
        c.execute("""SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "%s" AND TABLE_NAME = "%s" ORDER BY ORDINAL_POSITION;""" % (self.selectedDB.get(), self.selectedTable.get()))

        for datatype in c.fetchall():
            self.fieldTypes.append(datatype[0])
        c.close()
    
    def destroyDisplay(self):
        for child in self.dataframe.winfo_children():
            child.destroy()

    def createDisplay(self):
        self.tree = ttk.Treeview(self.dataframe, columns=self.fieldList, show="headings")
        for column in self.fieldList:
            self.tree.heading(column, text=column)
        for record in self.recordList:
            self.tree.insert('', tk.END, values=record)
        self.tree.grid(row=0, column=0, sticky="news")

        self.treeScrollbarX = tk.Scrollbar(self.dataframe, orient = "horizontal", command=self.tree.xview)
        self.treeScrollbarY = tk.Scrollbar(self.dataframe, orient = "vertical", command=self.tree.yview)
        self.treeScrollbarX.grid(row=1, column = 0, sticky="ew")
        self.treeScrollbarY.grid(row=0, column = 1, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self.getEntryId)

    def getEntryId(self, target):
        self.selectedEntry = self.tree.focus() 
        self.onSelectChange()
    
    def createForms(self):
        try:
            self.innerFFrame.destroy()
        except:
            pass
        try:
            self.formframePH.destroy()
        except:
            pass

        self.forms = []

        self.innerFFrame = ttk.Frame(self.formCanvas)
        self.innerFFrame.bind("<Configure>", lambda e: self.formCanvas.configure(scrollregion=self.formCanvas.bbox("all")))
        self.formCanvas.create_window((0,0), window=self.innerFFrame, anchor="nw")
        self.formCanvas.configure(yscrollcommand=self.formCanvasScrollbar.set)
        self.innerFFrame.columnconfigure(0, weight=1)
        self.innerFFrame.columnconfigure(1, weight=1)
    
        for index, field in enumerate(self.fieldList):
            self.field = tk.Label(self.innerFFrame, text=field, wraplength=150)
            self.field.grid(column=0, row=index, sticky="ew", padx=50, pady=10)
            self.entry = tk.Entry(self.innerFFrame, width=30)
            self.entry.grid(column=1, row=index, sticky="ew", padx=50, pady=10)
            self.forms.append((self.field, self.entry))

    def delRec(self):
        if self.selectedTable.get() != "Select Table" and self.selectedEntry is not None:
            self.toDeleteVal = []
            self.query = ""
            for index in self.keyIndexes:
                if self.typeMapping[self.fieldTypes[index]] == "date":
                    self.toDeleteVal.append("'"+str(self.tree.item(self.selectedEntry)['values'][index])+"'")
                else:
                    self.toDeleteVal.append(self.tree.item(self.selectedEntry)['values'][index])
            for index, key in enumerate(self.toDeleteVal):
                if index == 0:
                    self.query += "DELETE FROM %s WHERE %s = %s" % (self.selectedTable.get(), self.keyNames[index], self.toDeleteVal[index])
                else:
                    self.query += " AND %s = %s" % (self.keyNames[index], self.toDeleteVal[index])
            self.query += ";"
            
            try:
                c = db.cursor()
                c.execute(self.query)
                c.close()
                self.tree.delete(self.selectedEntry)
            except MySQLdb.Error as e:
                self.alertMessage(e.args[1])
    
    def onSelectChange(self):
        if self.selectedEntry == '':
            return
        for i in range(len(self.fieldList)):
            self.forms[i][1].delete(0, tk.END)
            self.forms[i][1].insert(0, self.tree.item(self.selectedEntry)['values'][i])

    def updateRec(self):
        if self.selectedTable.get() != "Select Table" and self.selectedEntry is not None:
            self.newVal = []
            self.newValCpy = []
            self.query = ""
            
            try:
                for i in range(len(self.fieldList)):
                    if self.forms[i][1].get() == '':
                        self.newVal.append('NULL')
                        self.newValCpy.append(self.forms[i][1].get())
                    elif self.typeMapping[self.fieldTypes[i]] is str:
                        self.newVal.append("\""+str(self.forms[i][1].get())+"\"")
                        self.newValCpy.append(str(self.forms[i][1].get()))
                    elif self.typeMapping[self.fieldTypes[i]] == "date":
                        self.newVal.append("'"+str(self.forms[i][1].get())+"'")
                        self.newValCpy.append(str(self.forms[i][1].get()))
                    else:
                        self.newVal.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
                        self.newValCpy.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
            except ValueError as err:
                self.alertMessage("Value error detected! Check your forms if inputs are appropriate!")
                return
            
            self.query += "UPDATE %s SET " % (self.selectedTable.get())
            for i in range(len(self.fieldList)):
                self.query += "%s = %s" % (self.fieldList[i], self.newVal[i])
                if i != (len(self.fieldList)-1):
                    self.query += ", "
            for i, key in enumerate(self.keyNames):
                if i == 0:
                    if self.typeMapping[self.fieldTypes[self.keyIndexes[i]]] == "date":
                        self.query += " WHERE %s = %s" % (key, "'"+str(self.tree.item(self.selectedEntry)['values'][self.keyIndexes[i]])+"'")
                    else:
                        self.query += " WHERE %s = %s" % (key, self.tree.item(self.selectedEntry)['values'][self.keyIndexes[i]])
                else:
                    if self.typeMapping[self.fieldTypes[self.keyIndexes[i]]] == "date":
                        self.query += " AND %s = %s" % (key, "'"+str(self.tree.item(self.selectedEntry)['values'][self.keyIndexes[i]])+"'")
                    else:
                        self.query += " AND %s = %s" % (key, self.tree.item(self.selectedEntry)['values'][self.keyIndexes[i]])
            self.query += ";"

            try:
                c = db.cursor()
                c.execute(self.query)
                self.tree.item(self.selectedEntry, values=self.newValCpy)
                c.close()
                self.alertMessage()
            except MySQLdb.Error as e:
                self.alertMessage(e.args[1])
    
    def addRec(self):
        if self.selectedTable.get() != "Select Table":
            self.query=""
            self.toAddVal = []
            self.toAddValCopy = []
            try:
                for i in range(len(self.fieldList)):
                    if self.forms[i][1].get() == '':
                        self.toAddVal.append('NULL')
                        self.toAddValCopy.append(self.forms[i][1].get())
                    elif (self.typeMapping[self.fieldTypes[i]]) is str:
                        self.toAddVal.append("\""+self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get())+"\"")
                        self.toAddValCopy.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
                    elif (self.typeMapping[self.fieldTypes[i]]) == "date":
                        self.toAddVal.append("'"+str(self.forms[i][1].get())+"'")
                        self.toAddValCopy.append(str(self.forms[i][1].get()))
                    else:
                        self.toAddVal.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
                        self.toAddValCopy.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
            except ValueError as err:
                self.alertMessage("Value error detected! Check your forms if inputs are appropriate!")
                return
            self.query += "INSERT INTO %s (" % (self.selectedTable.get())
            for i in range(len(self.fieldList)):
                self.query += "%s" % (self.fieldList[i])
                if (i != (len(self.fieldList)-1)):
                    self.query += ", "
                else:
                    self.query += ") VALUES ("
            for i in range(len(self.fieldList)):
                self.query += "%s" % (self.toAddVal[i])
                if (i != (len(self.fieldList)-1)):
                    self.query += ", "
                else:
                    self.query += ");"
            
            try:
                c = db.cursor()
                c.execute(self.query)
                c.close()
                self.tree.insert('', tk.END, values=self.toAddValCopy)
                self.alertMessage()
            except MySQLdb.Error as e:
                self.alertMessage(e.args[1])

    def selectRec(self):
        if self.selectedTable.get() != "Select Table":
            self.toFilterVal = []
            self.recordList = []
            self.query = ""

            try:
                for i in range (len(self.fieldList)):
                    if self.forms[i][1].get() == 'NULL':
                        self.toFilterVal.append('NULL')
                    elif self.forms[i][1].get() == '':
                        self.toFilterVal.append(self.fieldList[i])
                    elif (self.typeMapping[self.fieldTypes[i]]) is str:
                        self.toFilterVal.append("\""+self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get())+"\"")
                    elif (self.typeMapping[self.fieldTypes[i]]) == "date":
                        self.toFilterVal.append("'"+str(self.forms[i][1].get())+"'")
                    else:
                        self.toFilterVal.append(self.typeMapping[self.fieldTypes[i]](self.forms[i][1].get()))
            except ValueError as err:
                self.alertMessage("Value error detected! Check your forms if inputs are appropriate!")
                return
            
            self.query = "SELECT * FROM %s WHERE " % (self.selectedTable.get())

            for i in range (len(self.fieldList)):
                if self.fieldList[i] == self.toFilterVal[i]:
                    if i == 0:
                        self.query += "1 = 1"
                    else:
                        self.query += " AND 1 = 1 "
                elif self.toFilterVal[i] == 'NULL':
                    if i == 0:
                        self.query += "%s IS NULL" % (self.fieldList[i])
                    else:
                        self.query += " AND %s IS NULL " % (self.fieldList[i])
                else:
                    if i == 0:
                        self.query += "%s = %s" % (self.fieldList[i], self.toFilterVal[i])
                    else:
                        self.query += " AND %s = %s" % (self.fieldList[i], self.toFilterVal[i])
            self.query += ";"
            c = db.cursor()
            c.execute(self.query)
            for data in c.fetchall():
                self.recordList.append(data)
            self.destroyDisplay()
            self.createDisplay()
        
    def alertMessage(self, message = "Action Successful!"):
        try:
            self.alertAction.destroy()
        except:
            pass

        self.alertAction = tk.Toplevel(self.root)
        self.alertAction.title("Alert")
        self.alertAction.geometry = ("300x250")
        self.alertAction.resizable(False, False)
        self.alertActionM = tk.Label(self.alertAction, text = message, wraplength = 800)
        self.alertActionM.grid(column=0,row=0,sticky="news", padx=5, pady=5)
        self.alertAction.mainloop()

    def createTable(self):
        if self.selectedDB.get() != 'Select Database':
            self.fieldAmount = None
            self.getFieldAmount()

    def getFieldAmount(self):
        try:
            self.popupFieldAmount.destroy()
        except:
            pass
        self.popupFieldAmount = tk.Toplevel(self.root)
        self.popupFieldAmount.rowconfigure(0, weight = 1)
        self.popupFieldAmount.rowconfigure(1, weight = 1)
        self.popupFieldAmount.columnconfigure(0, weight = 1)
        self.popupFieldAmount.columnconfigure(1, weight = 1)

        self.pfaLabel = tk.Label(self.popupFieldAmount, text = "Number of fields: ")
        self.pfaLabel.grid(column = 0, row = 0, sticky = "ew", padx = 5, pady = 5)
        self.pfaEntry = tk.Entry(self.popupFieldAmount)
        self.pfaEntry.grid(column = 1, row = 0, sticky = "ew", padx = 5, pady = 5)
        self.pfaSubmit = tk.Button(self.popupFieldAmount, text = "Submit", command = self.validateFieldAmount)
        self.pfaSubmit.grid(row = 1, column = 0, columnspan=2, sticky = "ew", padx = 5, pady = 5,)
        self.popupFieldAmount.mainloop()

    def validateFieldAmount(self):
        try:
            int(self.pfaEntry.get()) 
        except:
            self.alertMessage("Input is not valid! Please enter numbers (integers) only.")
            return

        if int(self.pfaEntry.get()) > 0:
                self.fieldAmount = int(self.pfaEntry.get())
                self.popupFieldAmount.destroy()
                self.popupPopulateFields()
        else:
            self.alertMessage("Field amount must be greater than 0!")  
    
    def popupPopulateFields(self):
        self.PPWForms = []
        try:
            self.popupPopulateWindow.destroy()
        except:
            pass
        self.popupPopulateWindow = tk.Toplevel(self.root)
        self.popupPopulateWindow.geometry("1200x500")
        self.popupPopulateWindow.title("Define Fields")
        self.popupPopulateWindow.resizable(False, False)
        self.popupPopulateWindow.rowconfigure(0, weight = 1)
        self.popupPopulateWindow.columnconfigure(0, weight = 1)
        self.popupPopulateWindow.columnconfigure(1)
        self.popupPopulateWindow.grid_propagate(False)

        self.PPWCanvas = tk.Canvas(self.popupPopulateWindow)
        self.PPWCanvas.grid(row=0,column=0, sticky="news")
        self.PPWCanvasScrollbar = ttk.Scrollbar(self.popupPopulateWindow, orient="vertical", command=self.PPWCanvas.yview)
        self.PPWCanvasScrollbar2 = ttk.Scrollbar(self.popupPopulateWindow, orient = "horizontal", command = self.PPWCanvas.xview)
        self.PPWCanvasScrollbar.grid(row=0,column=1,sticky="ns")
        self.PPWCanvasScrollbar2.grid(row=self.fieldAmount+3,column=0,sticky="ew")
        
        self.PPWFieldFrame = tk.Frame(self.PPWCanvas)
        self.PPWFieldFrame.bind("<Configure>", lambda e: self.PPWCanvas.configure(scrollregion=self.PPWCanvas.bbox("all")))
        self.PPWCanvas.create_window((0,0), window = self.PPWFieldFrame, anchor = "nw")
        self.PPWCanvas.configure(yscrollcommand=self.PPWCanvasScrollbar.set)
        self.PPWCanvas.configure(xscrollcommand=self.PPWCanvasScrollbar2.set)

        self.PPWTableNameL = tk.Label(self.PPWFieldFrame, text = "Enter Table Name: ")
        self.PPWTableNameE = tk.Entry(self.PPWFieldFrame)

        self.PPWTableNameL.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.PPWTableNameE.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.PPWForms.append(self.PPWTableNameE)

        self.PPWSubmitBtn  = tk.Button(self.PPWFieldFrame, text = "Create Table", command = self.buildCreateTableQuery)
        self.PPWSubmitBtn.grid(row = self.fieldAmount+2, column = 0)

        self.PPWL1 = tk.Label(self.PPWFieldFrame, text = "Field Name")
        self.PPWL2 = tk.Label(self.PPWFieldFrame, text = "Data Type")
        self.PPWL3 = tk.Label(self.PPWFieldFrame, text = "Constraints")
        self.PPWL4 = tk.Label(self.PPWFieldFrame, text = "References")

        self.PPWL1.grid(row = 1, column = 0, padx = 5)
        self.PPWL2.grid(row = 1, column = 1, padx = 5, columnspan=4)
        self.PPWL3.grid(row = 1, column = 5, padx = 5, columnspan=4)
        self.PPWL4.grid(row = 1, column = 9, padx = 5)

        for i in range(self.fieldAmount):
            self.PPWFieldName = tk.Entry(self.PPWFieldFrame)
            self.PPWDatatype = tk.StringVar()
            self.PPWIsUnique = tk.IntVar()
            self.PPWNotNull = tk.IntVar()
            self.PPWIsPK = tk.IntVar()
            self.PPWIsFK = tk.IntVar()
            self.PPWTable = tk.StringVar()
            self.PPWField = tk.StringVar()
            self.PPWR1 = tk.Radiobutton(self.PPWFieldFrame, text = "Integer", value = "INT", variable=self.PPWDatatype)
            self.PPWR2 = tk.Radiobutton(self.PPWFieldFrame, text = "Float", value = "FLOAT", variable=self.PPWDatatype)
            self.PPWR3 = tk.Radiobutton(self.PPWFieldFrame, text = "Text", value = "TEXT", variable=self.PPWDatatype)
            self.PPWR4 = tk.Radiobutton(self.PPWFieldFrame, text = "Date (YYYY-MM-DD)", value ="DATE", variable=self.PPWDatatype)

            self.PPWFieldName.grid(row = i+2, column = 0, pady = 5, padx = (5, 0))
            self.PPWR1.grid(row = i+2, column = 1)
            self.PPWR2.grid(row = i+2, column = 2)
            self.PPWR3.grid(row = i+2, column = 3)
            self.PPWR4.grid(row = i+2, column = 4)
            
            self.PPWCB1 = tk.Checkbutton(self.PPWFieldFrame, text= "Unique", variable=self.PPWIsUnique)
            self.PPWCB2 = tk.Checkbutton(self.PPWFieldFrame, text= "Not Null", variable=self.PPWNotNull)
            self.PPWCB3 = tk.Checkbutton(self.PPWFieldFrame, text= "Primary Key", variable=self.PPWIsPK)
            self.PPWCB4 = tk.Checkbutton(self.PPWFieldFrame, text= "Foreign Key", variable=self.PPWIsFK)

            self.PPWCB1.grid(row = i+2, column = 5)
            self.PPWCB2.grid(row = i+2, column = 6)
            self.PPWCB3.grid(row = i+2, column = 7)
            self.PPWCB4.grid(row = i+2, column = 8)

            self.PPWCMBB1 = ttk.Combobox(self.PPWFieldFrame, textvariable=self.PPWTable, values = self.tableList)
            self.PPWCMBB2 = ttk.Combobox(self.PPWFieldFrame, textvariable=self.PPWField, values = "")
            self.PPWTable.trace_add("write", lambda a,b,c, combobox1 = self.PPWCMBB1, combobox2 = self.PPWCMBB2: self.PPWFetchFields(combobox1, combobox2))

            self.PPWCMBB1.grid(row=i+2, column = 9, padx = 5)
            self.PPWCMBB2.grid(row=i+2, column = 10)

            self.PPWForms.append((self.PPWFieldName, self.PPWDatatype, self.PPWIsUnique, self.PPWNotNull, self.PPWIsPK, self.PPWIsFK, self.PPWTable, self.PPWField))
            
    def buildCreateTableQuery(self):
        self.CreateTablePKs = []
        self.CreateTableFKs = []
        
        if self.PPWForms[0].get() == '':
            self.alertMessage("Table name is blank")
            return
        if '`' in self.PPWForms[0].get():
            self.alertMessage("` not allowed in table name")
            return
        if ' ' in self.PPWForms[0].get():
            self.alertMessage("Spaces not allowed in table name")
            return
        if ';' in self.PPWForms[0].get():
            self.alertMessage("; not allowed in table name")
            return

        self.query = ""
        self.query += "CREATE TABLE %s (" % (self.PPWForms[0].get())
        for index, form in enumerate(self.PPWForms):
            if index == 0:
                pass
            else:
                
                if self.PPWForms[index][0].get() == '':
                    self.alertMessage("A field name is blank")
                    return
                if '`' in self.PPWForms[index][0].get():
                    self.alertMessage("` not allowed in field names")
                    return
                if ' ' in self.PPWForms[index][0].get():
                    self.alertMessage("Spaces not allowed in field names")
                    return
                if ';' in self.PPWForms[index][0].get():
                    self.alertMessage("; not allowed in field names")
                    return
                if self.PPWForms[index][1].get() == '':
                    self.alertMessage("Detected a field which has no datatype selected!")
                    return

                self.query += "%s %s" % (self.PPWForms[index][0].get(), self.PPWForms[index][1].get())
                if self.PPWForms[index][2].get() == 1:
                    self.query += " UNIQUE"
                if self.PPWForms[index][3].get() == 1:
                    self.query += " NOT NULL"
                if self.PPWForms[index][4].get() == 1:
                    self.CreateTablePKs.append(self.PPWForms[index][0].get())
                if self.PPWForms[index][5].get() == 1:
                    if self.PPWForms[index][6].get() == '' or self.PPWForms[index][7].get() == '':
                        self.alertMessage("A field was designated as a foreign key, but references were not properly defined in the dropdowns")
                        return
                    self.CreateTableFKs.append((self.PPWForms[index][0].get(), self.PPWForms[index][6].get(), self.PPWForms[index][7].get()))
                if index != len(self.PPWForms)-1:
                    self.query += ", "
        if len(self.CreateTablePKs) > 0:
            self.query += ", CONSTRAINT PRIMARY KEY ("
            for index, key in enumerate(self.CreateTablePKs):
                self.query += key
                if index == len(self.CreateTablePKs)-1:
                    self.query += ")"
                else:
                    self.query += ", "
        else:
            self.alertMessage("The table MUST have a primary key")
            return
        
        if len(self.CreateTableFKs) > 0:
            for index, key2 in enumerate(self.CreateTableFKs):
                self.query += ", CONSTRAINT FOREIGN KEY (%s) REFERENCES %s(%s)" % (self.CreateTableFKs[index][0], self.CreateTableFKs[index][1], self.CreateTableFKs[index][2])
        self.query += ");"

        c = db.cursor() 
        try:
            c.execute(self.query)
            c.close()
            self.popupPopulateWindow.destroy()
            self.destroyDisplay()
            
            try:
                self.innerFFrame.destroy()
            except:
                pass
            try:
                self.formframePH.destroy()
            except:
                pass

            self.formframePH = tk.Label(self.formCanvas, text="Input forms will appear here after selecting a table.")
            self.formframePH.pack(expand=True)
            self.dataframePH = tk.Label(self.dataframe, text="Select a Database and a Table to Start.", bg="white")
            self.dataframePH.place(anchor="center", relx=.5,rely=.5)

            self.selectTables()
            self.alertMessage()
        except MySQLdb.Error as err:
            c.close()
            self.alertMessage(err.args[1])
                  
    def PPWFetchFields(self, combobox1, combobox2):
        self.PPWFieldList = []
        combobox2.set("")
        c = db.cursor()
        c.execute("""SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = "%s" 
        AND TABLE_NAME = "%s" ORDER BY ORDINAL_POSITION;""" % (self.selectedDB.get(),combobox1.get())) 
        for column in c.fetchall():
            self.PPWFieldList.append(column[0])
        c.close()
        combobox2['values'] = self.PPWFieldList

    def popupDelTable(self):
        try:
            self.winDelTable.destroy()
        except:
            pass
       
        self.winDelTable = tk.Toplevel(self.root)
        self.winDelTable.title("Delete Table")
        self.winDelTable.geometry = ("300x250")
        self.winDelTable.resizable(False, False)
        self.winDelTableL = tk.Label(self.winDelTable, text="Choose Table: ")
        self.winDelTableL.grid(column=0, row=0, sticky="news", padx=5,pady=5)
        self.toDelTable = tk.StringVar()
        self.toDelTableDrpDwn = ttk.Combobox(self.winDelTable, textvariable=self.toDelTable, values=self.tableList, state="readonly")
        self.toDelTableDrpDwn.grid(column=1,row=0, padx=5,pady=5,sticky="news")
        self.winDelTableBtn = tk.Button(self.winDelTable, command = self.delTable, text="Delete")
        self.winDelTableBtn.grid(column=0,row=1, columnspan=2, sticky="news", padx=5, pady=5)
        self.delTableError = tk.Label(self.winDelTable, wraplength=250)
        self.delTableError.grid(column=0, row=2, rowspan=2, columnspan=2, padx=5, pady=5)
        self.winDelTable.mainloop()

    def delTable(self):
        c = db.cursor()
        try:
            c.execute("DROP TABLE %s" % (self.toDelTable.get()))
            c.close()
            self.destroyDisplay()

            try:
                self.innerFFrame.destroy()
            except:
                pass
            try:
                self.formframePH.destroy()
            except:
                pass

            self.formframePH = tk.Label(self.formCanvas, text="Input forms will appear here after selecting a table.")
            self.formframePH.pack(expand=True)
            self.dataframePH = tk.Label(self.dataframe, text="Select a Database and a Table to Start.", bg="white")
            self.dataframePH.place(anchor="center", relx=.5,rely=.5)

            self.selectTables()
            self.winDelTable.destroy()
            self.alertMessage()
        except MySQLdb.Error as err:
            c.close()
            self.delTableError.config(text=err.args[1])


if db != None:       
    win = mainGUI()
    win.root.mainloop()

db.commit()
print("Program Terminated.")
