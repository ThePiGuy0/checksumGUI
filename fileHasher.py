#!/bin/python3

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
from math import floor,ceil

import hashlib
import os

labelFont = ['calibri',13]
entryFont = ['calibri',13]
buttonFont = ['calibri',13]
defaultHashMode = 'MD4'
radioButtons = ['MD4','MD5','SHA1','SHA256','SHA384','SHA512']
labelWidth=15
buttonWidth=15
entryWidth=70

windowTitle = "File Hasher"
fileLocationLabelText = "File Location"
openFileButtonText = "Open File"
hashingModeText = "Hashing Mode"
hashInputText = "Hash to Compare"
openHashButtonText = "Open Hash File"
generatedHashLabelText = "Generated Hash"
goButtonText = "Hash File"
errorMessage = ['Error','Hash file data type identification unsuccessful']
successMessage = ["Success","Your hash matches the generated hash"]

class main:
    def __init__(self):
        self.root = Tk()
        self.root.title(windowTitle)
        self.pathLabel = self.createLabel(fileLocationLabelText)
        self.pathLabel.grid(column=0,row=0)
        self.pathEntry = self.createEntry()
        self.pathEntry.grid(column=1,row=0,sticky=N+S)
        self.openFileButton = self.createButton(openFileButtonText,self.getFileLocation)
        self.openFileButton.grid(column=2,row=0,rowspan=2,sticky=N+S)
        self.hashingModeLabel = self.createLabel(hashingModeText)
        self.hashingModeLabel.grid(column=0,row=1)
        self.hashingModeFrame = Frame(self.root)
        self.hashingModeFrame.grid(column=1,row=1)
        self.hashMode = StringVar()
        self.hashMode.set(defaultHashMode.lower())
        for x in range(len(radioButtons)):
            radio = Radiobutton(self.hashingModeFrame,text=radioButtons[x].upper(),value=radioButtons[x].lower(),variable=self.hashMode)
            radio.grid(column=x,row=0)
        self.inputHashLabel = self.createLabel(hashInputText)
        self.inputHashLabel.grid(column=0,row=2)
        self.inputHashEntry = self.createEntry()
        self.inputHashEntry.grid(column=1,row=2,sticky=N+S)
        self.openHashButton = self.createButton(openHashButtonText,self.openHashFile)
        self.openHashButton.grid(column=2,row=2,rowspan=2,sticky=N+S)
        self.generatedHashLabel = self.createLabel(generatedHashLabelText)
        self.generatedHashLabel.grid(column=0,row=3)
        self.generatedHashOutput = self.createEntry('readonly')
        self.generatedHashOutput.grid(column=1,row=3,sticky=N+S)
        self.goButton = Button(self.root,text=goButtonText,font=buttonFont,command=self.generateHash)
        self.goButton.grid(column=0,row=4,columnspan=3,sticky=N+S+E+W)
        self.progress = Progressbar(self.root, orient=HORIZONTAL,length=100,mode='determinate')
        self.progress.grid(column=0,row=5,columnspan=3,sticky=N+S+E+W)
        self.root.mainloop()
    def createLabel(self,labelText):
        tempLabel = Label(self.root,text=labelText,font=labelFont,width=labelWidth)
        return tempLabel
    def createButton(self,buttonText,command):
        tempButton = Button(self.root,text=buttonText,font=buttonFont,width=buttonWidth,command=command)
        return tempButton
    def createEntry(self,state='normal'):
        tempEntry = Entry(self.root,font=entryFont,state=state,width=entryWidth)
        return tempEntry
    def getFileLocation(self):
        location = filedialog.askopenfilename()
        if location != '':
            self.pathEntry.delete(0,END)
            self.pathEntry.insert(0,location)
    def openHashFile(self):
        location = filedialog.askopenfilename()
        if location != '':
            datatype = []
            for x in list(location)[::-1]:
                if x == '.':
                    break
                else:
                    datatype.insert(0,x)
            datatype = ''.join(datatype)
            if datatype.upper() not in radioButtons:
                messagebox.showerror(*errorMessage)
            else:
                self.hashMode.set(datatype)
                with open(location,'r') as hashData:
                    checksumData = hashData.read()
                checksum = []
                for x in list(checksumData):
                    if x == ' ':
                        break
                    else:
                        checksum.append(x)
                self.inputHashEntry.delete(0,END)
                self.inputHashEntry.insert(0,''.join(checksum))
    def generateHash(self):
        fileToHash = self.pathEntry.get()
        if fileToHash != '':
            hashData = hashlib.new(self.hashMode.get())
            file = open(fileToHash,'rb')
            cont = True
            percentage = 0
            read_size = 0
            fullSize = os.path.getsize(fileToHash)
            chunkSize = ceil(fullSize / 100)
            while cont:
                data = file.read(chunkSize)
                hashData.update(data)
                read_size += len(data)
                percentage = floor((read_size / fullSize) * 100)
                self.progress['value'] = percentage
                self.root.update()
                if percentage == 100:
                    cont = False
            file.close()
            hexData = hashData.hexdigest()
            self.progress['value'] = 0
            self.generatedHashOutput.configure(state="normal")
            self.generatedHashOutput.delete(0,END)
            self.generatedHashOutput.insert(0,hexData)
            self.generatedHashOutput.configure(state="readonly")
            if hexData == self.inputHashEntry.get():
                messagebox.showinfo(*successMessage)
            else:
                messagebox.showerror("Hash Mismatch","Your hash does not match the generated hash")
if __name__ == '__main__':
    main()
