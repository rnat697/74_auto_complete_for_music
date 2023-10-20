# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'progress_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from music_python.generation import Generation
from music_python.prepocessing import Preprocessing

#TODO: SOMEHOW REDIRECT CONSOLE LOGS TO TEXT BROWSER
class MusicGeneratorThread(QtCore.QThread):
    progress_update = QtCore.pyqtSignal(str)  # Signal to update progress

    def __init__(self, promptName, outputFileName, promptLength, genLength):
        super().__init__()
        self.promptName = promptName 
        self.genLength = genLength
        self.promptLength = promptLength
        self.outFileName = outputFileName

        self.promptFile = ''
        if self.promptName == 'Alla Turca':
            self.promptFile = 'alla-turca'
        elif self.promptName == 'Fur Elise':
            self.promptFile = 'fur-elise'
        elif self.promptName == 'Clair de Lune':
            self.promptFile = 'debussy-clair-de-lune'
        elif self.promptName == 'La Campanella':
            self.promptFile = 'la_campanella'
        elif self.promptName == 'Piano Sonata No. 16':
            self.promptFile = 'Piano-Sonata-K545'

    def run(self):
        # Simulated music generation (replace with your code)
        sys.stdout = self
        try:
            preprocess = Preprocessing(self.promptFile)
            if(not preprocess.checkAlreadyPreprocessed()):
                preprocess.preprocessMidi()
            tokenise = preprocess.loadTokenizerFromJSON()
            data = preprocess.loadData()

            generation = Generation(data, maxGenLength=self.genLength, promptLength=self.promptLength, outFileName=self.outFileName, tokenizer=tokenise, promptName=self.promptName)
            generation.generateMusic()

        except Exception as e:
            errorMsg = f"Error during processing: {str(e)}"
            self.progress_update.emit(errorMsg)
        finally:
            sys.stdout = sys.__stdout__
    
    def write(self,text):
        self.progress_update.emit(text)

            


class Progress_Dialog(object):
    def __init__(self, outputFileName,selectedPrompt,promptLength,genLength):
        self.outputFileName = outputFileName
        self.selectedPrompt = selectedPrompt
        self.promptLength = promptLength
        self.genLenght = genLength
        self.generationCompleted = True
        self.runGenerationCode()
    

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)

         #  --- PROGRESS TITLE LABEL ---
        self.progressTitle = QtWidgets.QLabel(Dialog)
        self.progressTitle.setGeometry(QtCore.QRect(100, 20, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.progressTitle.setFont(font)
        self.progressTitle.setObjectName("progressTitle")

         #  --- PROGRESS BROWSER ---
        self.progressBrowser = QtWidgets.QTextBrowser(Dialog)
        self.progressBrowser.setGeometry(QtCore.QRect(35, 50, 341, 192))
        self.progressBrowser.setObjectName("progressBrowser")

         #  --- CLOSE BUTTON ---
        self.closeBtn = QtWidgets.QPushButton(Dialog)
        self.closeBtn.setGeometry(QtCore.QRect(160, 260, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.closeBtn.setFont(font)
        self.closeBtn.setObjectName("closeBtn")
        self.closeBtn.setEnabled(False)  # Initially disable the close button
        self.closeBtn.clicked.connect(self.handleCloseButtonClick)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.progressTitle.setText(_translate("Dialog", "Generating Music..."))
        self.closeBtn.setText(_translate("Dialog", "Close"))

    # closes window if the generation has completed
    def handleCloseButtonClick(self):
        # Handle the close button click event here
        if self.generationCompleted:
            self.dialog.accept() #AttributeError: 'Progress_Dialog' object has no attribute 'dialog'
        else:
            # Display a message to inform the user that generation is still in progress
            QtWidgets.QMessageBox.warning(None,"Warning", "Please wait until the generation is completed before closing the window.")


    # runing generation code
    def runGenerationCode(self):
        print("running generation code")
        # Create an instance of MusicGeneratorThread
        self.generator_thread = MusicGeneratorThread(self.selectedPrompt, self.outputFileName, self.promptLength, self.genLenght)

        # Connect the thread's signal to the progress dialog's slot
        self.generator_thread.progress_update.connect(self.updateProgress)

         # Connect the thread's finished signal to a slot
        self.generator_thread.finished.connect(self.onGenerationFinished)

        # Start the thread
        self.generator_thread.start()
   
    def updateProgress(self, progress_msg):
    # Update the progressBrowser with the received progress message
        self.progressBrowser.append(progress_msg)
    
    def onGenerationFinished(self):
        # This slot is called when the music generation thread has finished
        print("Music generation thread has finished")

        # Enable the close button since the thread has finished
        self.closeBtn.setEnabled(True)

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = Progress_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())
