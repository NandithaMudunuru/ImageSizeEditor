"""
Author: Nanditha Mudunuru
email: nanditha.mudunuru@gmail.com
date: 31 January 2022
"""


import os
import tkinter as tk
from tkinter import filedialog, Text, Entry, ttk

def reSize(path, fileFormat, width, height):

    import os
    from PIL import Image
    from pdf2image import convert_from_path

    # Setting file format
    if fileFormat=='.jpg':
        outType='JPEG'
    elif fileFormat=='.png':
        outType='PNG'

    # Creating output directory
    outPath = os.path.join(path, 'Resized Images') 
    os.mkdir(outPath)

    # Reading and coverting pdfs to images
    List = os.listdir(path)
    fileNames = [x.split('.')[0] for x in List if x.split('.')[-1]=='pdf']
    print('Converting pdfs to images.')
    statusBox.insert('end', 'Running: Converting pdfs to images.\n')
    for f in fileNames:
        pdfImg = convert_from_path(os.path.join(path,f+'.pdf'))
        if len(pdfImg)==1:
            pdfImg[0].save(os.path.join(outPath, f+fileFormat), outType)
        else:
            for i in range(len(pdfImg)):
                pdfImg[i].save(os.path.join(outPath, f+'{0:02d}'.format(i)+fileFormat), outType)

    # Reading and resizing images
    List = os.listdir(outPath)
    fileNames = [x for x in List if x.split('.')[-1]==fileFormat[1:]]
    print('Resizing and saving images.')
    statusBox.insert('end', 'Running: Resizing and saving images.\n')
    for f in fileNames:
        img = Image.open(os.path.join(outPath, f))
        img = img.resize((int(3.7795275591*width),int(3.7795275591*height)))
        img = img.save(os.path.join(outPath, f)) 

    print('Run complete.')
    statusBox.insert('end', 'Running: Complete.\n')

root = tk.Tk()
root.title('Image Resize')

# Main Canvas
canvas = tk.Canvas(root, height=350, width=700, bg='#A0816C')
canvas.pack()

frame = tk.Frame(root, bg='#A0816C')
frame.place(relwidth=0.98, relheight=0.96, relx=0.01, rely=0.02)

# Input Variables
Folder = tk.StringVar(root, os.sep)
FinalWidth = tk.IntVar(root, 100)
FinalHeight = tk.IntVar(root, 100)
Format = tk.StringVar(root, '.jpg')

# Input frames
inputFrame = tk.Frame(frame, bg='#E8DED1')
inputFrame.place(relwidth=1, relheight=0.7)

## Folder selector frame
selFolFrame = tk.Frame(inputFrame, bg='#E8DED1')
selFolFrame.place(relwidth=0.6, height=30, relx=0.2, rely=0.1)

def selFolder():
    folder = filedialog.askdirectory()
    txtFolder.insert('end',folder)
    displayFolder(folder)

def findFolder():
    folder = txtFolder.get()
    displayFolder(folder)

def displayFolder(text):
    #statusBox.delete('1.0', tk.END)
    statusBox.insert('end', 'Selected folder: '+text+'\n')
    Folder.set(text)

### Text format entry
txtFolder = Entry(selFolFrame)  
txtFolder.place(relwidth=0.6, relheight=1)
openFolder = tk.Button(selFolFrame, text='Go', fg='white', bg='#A0816C', command=findFolder)
openFolder.place(relwidth=0.1, relx=0.6, relheight=1)

### Select from dialog box
selectFolder = tk.Button(selFolFrame, text='Select Folder', padx=10, pady=5, fg='white', bg='#263D42',
    command=selFolder)
selectFolder.pack(side=tk.RIGHT)

## Dimension selector frame
setDimFrame = tk.Frame(inputFrame, bg='#E8DED1')
setDimFrame.place(relwidth=0.6, height=60, relx=0.2, rely=0.3)

### Width
ttk.Label(setDimFrame, text='Width (mm):', background='#E8DED1').grid(column=0, row=0, columnspan=1, rowspan=1, sticky=tk.W)
widthEntry = ttk.Entry(setDimFrame)
widthEntry.grid(column=0, row=1, columnspan=1, rowspan=1, ipady=5)

### Height
ttk.Label(setDimFrame, text='Height (mm):', background='#E8DED1').grid(column=1, row=0, columnspan=1, rowspan=1, sticky=tk.W)
heightEntry = ttk.Entry(setDimFrame)
heightEntry.grid(column=1, row=1, columnspan=1, rowspan=1, ipady=5)

### Output file format
ttk.Label(setDimFrame, text='Output Format:', background='#E8DED1').grid(column=2, row=0, columnspan=1, rowspan=1, sticky=tk.W)

Format.set(".jpg") # default value

formatDD = tk.OptionMenu(setDimFrame, Format, ".jpg", ".png")
formatDD.grid(column=2, row=1, columnspan=1, rowspan=1, sticky=tk.W, ipadx=20)

### Get variables
def getDims():
    try:
        FinalWidth.set(widthEntry.get())
        statusBox.insert('end', 'Width: '+widthEntry.get()+'\n')
    except:
        statusBox.insert('end', 'Invalid Width: Enter a positive integer in mm \n')
    try:
        FinalHeight.set(heightEntry.get())
        statusBox.insert('end', 'Height: '+heightEntry.get()+'\n')
    except:
        statusBox.insert('end', 'Invalid Height: Enter a positive integer in mm \n')

    statusBox.insert('end', 'Format: '+Format.get()+'\n')
    

getDimensions = tk.Button(setDimFrame, text='Submit', fg='white', bg='#263D42', command=getDims)
getDimensions.grid(column=3, row=1, columnspan=1, rowspan=2, padx=10)


## Submit button frame
submitFrame = tk.Frame(inputFrame, bg='#E8DED1')
submitFrame.place(relwidth=0.6, height=60, relx=0.2, rely=0.7)

### Run
def run():
    reSize(Folder.get(), Format.get(), FinalWidth.get(), FinalHeight.get())

runCommand = tk.Button(submitFrame, text='Run', fg='white', bg='#263D42', command=run)
runCommand.pack()




## Status Frame
statusFrame = tk.Frame(frame, bg='#A0816C')
statusFrame.place(relwidth=1, relheight=0.28, rely=0.72)
### Output
statusBox = Text(statusFrame, bg='#A0816C', fg='white')
statusBox.place(relwidth=1, relheight=1)
#### Create a scrollbar widget and set its command to the text widget
scrollbar = ttk.Scrollbar(statusBox, orient='vertical', command=statusBox.yview)
scrollbar.place(relheight=1, relwidth=0.02, relx=0.98)
#### Communicate back to the scrollbar
statusBox['yscrollcommand'] = scrollbar.set

root.mainloop()