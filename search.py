#!/usr/bin/env python
import os,Tkinter,time,thread,tkMessageBox

def spider():
    crawler = os.walk("/Users/kmspriyatham/Movies/My Movies")
    appender(crawler)
    #crawler = os.walk("/Users/kmspriyatham/Codes/")
    #appender(crawler)
    crawler = os.walk("/Users/kmspriyatham/Documents/")
    appender(crawler)
    crawler = os.walk("/Users/kmspriyatham/Academics/")
    appender(crawler)
    crawler = os.walk("/Users/kmspriyatham/Music/iTunes/iTunes Media/Music/")
    appender(crawler)
    for items in os.listdir("/Applications/"):
        filesList.append(os.path.join("/Applications",items))
    rankFileHandler()

def appender(crawler):
    for dirPath,dirNames,fileNames in crawler:
        for items in fileNames:
            if(items != ".DS_Store"):
                filesList.append(os.path.join(dirPath,items))

def search():
    prevSearchTerm = ""
    count = 0
    while True:
        searchTerm = searchField.get()
        if(searchTerm == ""):
            searchResults.delete(0,Tkinter.END)
            searchResultsList[:] = []
            prevSearchTerm = ""
        elif(searchTerm == prevSearchTerm):
            pass
        else:
            count = 0
            searchResults.delete(0,Tkinter.END)
            searchResultsList[:] = []
            for files in filesList:
                if searchTerm.lower() in os.path.basename(files.lower()):
                    searchResults.insert(Tkinter.END,os.path.split(files)[1])
                    searchResultsList.append(files)
                    count += 1
                if count > 27:
                    break
            prevSearchTerm = searchTerm
        time.sleep(0.001)    
  
def fileOpener(PressEvent):
    try:
        fileName = searchResultsList[searchResults.index(Tkinter.ACTIVE)]
        fileToBeOpened = str(fileName)
        fileToBeOpened = nameModifier(fileToBeOpened)
        openCommand = "open " + fileToBeOpened
        os.system(openCommand)
        return "break"
    except Tkinter.TclError:
        print "No File Selected"

def fileDeleter(PressEvent):
    if(tkMessageBox.askokcancel("Delete","Are you sure you want to delete the file?")):
        try:
            fileName = searchResultsList[searchResults.index(Tkinter.ACTIVE)]
            searchResults.delete(Tkinter.ACTIVE)
            os.remove(fileName)
            filesList.pop(filesList.index(fileName))
            searchResultsList.pop(searchResultsList.index(fileName))
            tkMessageBox.showinfo("Alert!","File Deleted")
            return "break"
        except Tkinter.TclError:
            print "Couldn't be deleted"

def nameModifier(fileName):
    fileName = fileName.replace(" ","\ ")
    fileName = fileName.replace("(","\(")
    fileName = fileName.replace(")","\)")
    fileName = fileName.replace("'","\\'")
    fileName = fileName.replace(",","\,")
    fileName = fileName.replace("[","\[")
    fileName = fileName.replace("]","\]")
    fileName = fileName.replace("&","\&")
    return fileName

def focusShiftDown(PressEvent):
    searchResults.focus_set()
    searchResults.activate(0)
    return "break"

def focusShiftUp(PressEvent):
    if(searchResults.index(Tkinter.ACTIVE) == 0):
        searchField.focus_set()
        return "break"

def quitSearch():
    exit(0)

def rankFileHandler():
    rankFile = open("rankFile.txt","r+")
    for items in filesList:
        rankFile.write(os.path.split(items)[1]  )
    rankFile.close()    
    

filesList = []
searchResultsList = []
searchWindow = Tkinter.Tk()
searchWindow.title("Search")
searchWindow.geometry("700x525+350+100")
searchWindow.minsize(700,525)
searchWindow.maxsize(700,525)
searchWindow.configure(background = "white")

os.system("""osascript -e 'tell application "System Events" to set frontmost of application process "Python" of application "System Events" to true'""")

searchField = Tkinter.Entry(searchWindow)
searchField.focus_set()
searchField.bind("<Down>",focusShiftDown)
searchField.pack()

searchResults = Tkinter.Listbox(searchWindow)
searchResults.config(height = 27,width = 72)
searchResults.bind("<Return>",fileOpener)
searchResults.bind("<Double-Button-1>",fileOpener)
searchResults.bind("<BackSpace>",fileDeleter)
searchResults.bind("<Up>",focusShiftUp)
searchResults.pack()

quitButton = Tkinter.Button(searchWindow,text = "Quit",command = quitSearch)
quitButton.pack()

thread.start_new_thread(search,())
thread.start_new_thread(spider,())

searchWindow.mainloop()