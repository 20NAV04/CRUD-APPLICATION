import tkinter as tk
from tkinter import ttk
import MySQLdb
from MySQLdb import _exceptions

db = MySQLdb.connect("localhost", "root", "ace")


class GUI():
    fieldAmount = None
    PPWForms = []
    CreateTablePKs = []
    CreateTableFKs = []
    tableList = ['component', 'db']
    

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Testing Add Tables")
        
        self.createTableBtn = tk.Button(self.root, text = "Create Table", command = self.createTable)
        self.createTableBtn.pack(fill="both")
        self.root.mainloop()

    def createTable(self):
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

            self.PPWCMBB1 = ttk.Combobox(self.PPWFieldFrame, state="readonly", textvariable=self.PPWTable, values = self.tableList)
            self.PPWCMBB2 = ttk.Combobox(self.PPWFieldFrame, state="readonly", textvariable=self.PPWField, values = "")
            self.PPWTable.trace_add("write", lambda a,b,c, combobox1 = self.PPWCMBB1, combobox2 = self.PPWCMBB2: self.PPWFetchFields(combobox1, combobox2))

            self.PPWCMBB1.grid(row=i+2, column = 9, padx = 5)
            self.PPWCMBB2.grid(row=i+2, column = 10)

            self.PPWForms.append((self.PPWFieldName, self.PPWDatatype, self.PPWIsUnique, self.PPWNotNull, self.PPWIsPK, self.PPWIsFK, self.PPWTable, self.PPWField))
            
            

    def buildCreateTableQuery(self):
        self.CreateTablePKs = []
        self.CreateTableFKs = []
        self.query = ""
        self.query += "CREATE TABLE %s (" % (self.PPWForms[0].get())
        for index, form in enumerate(self.PPWForms):
            if index == 0:
                pass
            else:
                self.query += "%s %s" % (self.PPWForms[index][0].get(), self.PPWForms[index][1].get())
                if self.PPWForms[index][2].get() == 1:
                    self.query += " UNIQUE"
                if self.PPWForms[index][3].get() == 1:
                    self.query += " NOT NULL"
                if self.PPWForms[index][4].get() == 1:
                    self.CreateTablePKs.append(self.PPWForms[index][0].get())
                if self.PPWForms[index][5].get() == 1:
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
        if len(self.CreateTableFKs) > 0:
            for index, key2 in enumerate(self.CreateTableFKs):
                self.query += ", CONSTRAINT FOREIGN KEY (%s) REFERENCES %s(%s)" % (self.CreateTableFKs[index][0], self.CreateTableFKs[index][1], self.CreateTableFKs[index][2])
        self.query += ");"
        print(self.query)

        c = db.cursor() 
        try:
            c.execute(self.query)
            c.close()
            self.popupPopulateWindow.destroy()
        except MySQLdb.Error as err:
            c.close()
            self.alertMessage(err.args[1])
                  
    def PPWFetchFields(self, combobox1, combobox2):
        self.PPWFieldList = []
        combobox2.set("")
        c = db.cursor()
        c.execute("""SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = "mysql" 
        AND TABLE_NAME = "%s";""" % (combobox1.get())) 
        for column in c.fetchall():
            self.PPWFieldList.append(column[0])
        c.close()
        combobox2['values'] = self.PPWFieldList

GUI()
