"""
    Tkinter gui program
    Robert Bergers
"""

#import libraries
from tkinter import filedialog
from tkinter import *
import logging
from PIL import Image, ImageTk

root = Tk()
root.geometry("1280x720")

#The window object
class Window(Frame):
    #Declare new window
    def __init__(self, master=None):
        Frame.__init__(self, master)
        #variables
        self.master = master
        self.title = 'title'
        self.size = "1280x720"
        self.textWidgets = []
        self.focustext = 0
        root.lift()
        self.init_window()
        logging.info('Window title: %(self.title)s | Window size: %(self.size)s | Created\n', {'self.title':self.title, 'self.size':self.size})
    #Initialize window
    def init_window(self):
        #Create Frame
        self.master.title("%s" % self.title)
        self.textnumber = 0
        #Create Menu
        self.text = self.TextBox()
        self.textWidgets.insert(self.textnumber, self.text)
        if self.textWidgets[self.textnumber] != self.text:
            logging.critical('Textbox %s not created' % str(self.textnumber))
        else:
            logging.info('TextBox: %s | created.\n' % str(self.textnumber))
        self.textnumber += 1
        self.focustext += 1
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.file = Menu(self.menu)
        self.file.add_command(label="Exit", command=self.client_exit)
        self.file.add_command(label="Open", command=self.text.client_openfile)
        self.file.add_command(label="Save", command=self.text.client_savefile)
        self.file.add_command(label="Get Text", command=self.text.retrieve_text)
        self.file.add_command(label="New Text", command=self.add_text)
        self.menu.add_cascade(label="File", menu=self.file)
        self.edit = Menu(self.menu)
        self.edit.add_command(label="Undo")
        self.edit.add_command(label="Clear", command=self.TextBox.client_cleartext)
        self.menu.add_cascade(label="Edit", menu=self.edit)
        self.view = Menu(self.menu)
        self.view.add_command(label="Change Focus", command=self.focus_change())
        self.menu.add_cascade(label="View", menu=self.view)
        self.test = Menu(self.menu)
        self.test.add_command(label="Remove focus", command=self.linktoremove)
        self.test.add_command(label="Get Info", command=self.getinfo)
        self.menu.add_cascade(label="Test", menu=self.test)
    #METHODS
    #Close window
    def client_exit(self):
        exit()
    #Add widgets
    def add_text(self):
        self.text = self.TextBox()
        self.textWidgets.insert(self.textnumber, self.text)
        if self.textWidgets[self.textnumber] != self.text:
            logging.critical('Textbox %s not created\n' % str(self.textnumber))
        else:
            logging.info('Textbox: %s | created.\n' % self.textnumber)
        self.focustext = self.textnumber
        for i in range(self.textnumber):
            if self.textnumber != self.focustext:
                self.textWidgets[i].remove_text()
        self.textnumber += 1
        self.focustext += 1
    #Shift focus of text tabs
    def focus_change(self):
        if self.focustext == self.textnumber:
            self.focustext=0
            self.text = self.textWidgets[self.focustext]
            self.text.grid_remove()
        else:
            self.focustext += 1
            self.text = self.textWidgets[self.focustext]
            self.text.grid_remove()

        for i in range(self.textnumber):
            if self.textnumber != self.focustext:
                self.textWidgets[i].remove_text()
            else:
                self.textWidgets[i].raise_up()
    def getinfo(self):
        print(self.text.grid_info())
    def linktoremove(self):
        self.text.remove_text()
    #Subclasses
    class TextBox(Frame):
        #Initialize textbox
        def __init__(self):
            Frame.__init__(self)
            self.init_text()
        def init_text(self):
            self.text = Text(self.master)
            self.text.place(x=5, y=25, relwidth=1, relheight=1, width=-10, height=-30)
        # Open file and read to self.text
        def client_openfile(self):
                self.filename = filedialog.askopenfilename()
                file = open(self.filename, "r")
                mydata = file.read()
                print(mydata)
                file.close()
                self.text.insert(1.0, mydata)
        # Save self.text to file
        def client_savefile(self):
            self.filename = filedialog.asksaveasfile(title="Select file",
                                                     filetypes=(("text files", "*.txt"), ("all files", "*.*"), ("Markdown", "*.markdowd")))
            content = self.retrieve_text()
            print(content)
            file = open(self.filename, "w+")
            file.write(content)
            file.close()
            print(str(self.filename))
        #Clears content of text box
        def client_cleartext(self):
            self.text.delete(1.0, END)
        # Prints contents of self.text to console
        def retrieve_text(self):
            textContent = self.text.get(1.0, END)
            print(str(textContent))
            return textContent
        #Remove text task from list
        def remove_text(self):
            self.grid_forget()

        def raise_up(self):
            self.text.place(x=5, y=25, relwidth=1, relheight=1, width=-10, height=-30)




#Method to construct window
def gui():
    app = Window(root)
    root.mainloop()

#Main
if __name__ == '__main__':
    #Configure logger
    logging.basicConfig(filename='pytext.log', level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logging.info('Launching application\n')
    gui()