#!/usr/bin/python
from PySide.QtCore import  *
from PySide.QtGui import  *
from unicodedata import normalize
import sys
import ctypes
import Tkinter
import Engine
import picdl
import Object
import time

class Label(QLabel):
    def __init__(self,parent):
        super(label, self).__init__()
        self.setParent(parent)
    def dragEnterEvent(self,e):
        e.accept()
    def dropEvent(self,e):
        e.setDropAction(Qt.MoveAction)
        e.accept()
        source = self.sender()
        position = e.pos()
        source.Move(e.pos().x(),e.pos().y())

class Window(QMainWindow):
    def __init__(self):
        super(Window ,self).__init__()

       	root = Tkinter.Tk()

	screen_width = root.winfo_screenwidth() - 30
	screen_height = root.winfo_screenheight()
        screensize = (screen_width,screen_height)

        self.WinX = screensize[0]-15
        self.WinY = screensize[1]-80

        self.setWindowTitle("X Narrator")
        self.setGeometry(9 , 30 , screensize[0]-15, screensize[1]-80 )
        self.setFixedSize(self.size())
        self.setWindowIcon(QPixmap("./data/pics/logo1.png"))

        MyMenueBar = self.menuBar()
        File = MyMenueBar.addMenu("&File")
        Object_ = MyMenueBar.addMenu("&Object") 
        help = MyMenueBar.addMenu("&Help")

        self.exit = QAction("Exit" , self)
        self.reset = QAction("Reset" , self )
        self.inst = QAction("Instruction" , self)
        self.about = QAction("About" , self)
        self.add = QAction("Add Object" , self) 
        self.objList = QAction("Object Lists" , self) 

        File.addAction(self.reset)
        File.addAction(self.exit)

        help.addAction(self.inst)
        help.addAction(self.about)
        
        Object_.addAction(self.objList)
        Object_.addAction(self.add) 
        

        self.interpreter = QLineEdit(">>> ",self)
        self.interpreter.resize(200 , 25)
        self.interpreter.setText(">>> ")
        self.interpreter.setFont(QFont("Consolas" ,8))
        self.interpreter.move(2000 , 50)
        self.interpreter.setToolTip("Enter Your Command and Press Enter")

        self.info = QTextEdit(self)
        self.info.setReadOnly(1)
        self.info.move( -2000 , 100) 
        self.info.setText("\n >> Your Info Will be Printed Here")
        self.info.setFont(QFont("Consolas" ,7))

        self.mainview = QLabel(self)
        self.mainview.setFrameStyle((QFrame.StyledPanel | QFrame.Plain))
        self.mainview.resize(1 , 1)
        self.mainview.move(600 , 300)
        self.mainview.setPixmap(QPixmap("./data/pics/def_bg.jpg"))
        self.mainview.setScaledContents(1)

        self.txtlbl1 = QLabel(self)
        self.txtlbl1.setText("Enter your commands here :")
        self.txtlbl1.setFont(QFont("Trebuchet MS" ,8))
        self.txtlbl1.resize(200 , 12)
        self.txtlbl1.move(70 , 5000)

        self.txtlbl2 = QLabel(self)
        self.txtlbl2.setText("Engine Response : ")
        self.txtlbl2.setFont(QFont("Trebuchet MS" ,8))
        self.txtlbl2.resize(200 , 12)
        self.txtlbl2.move(20 , 5000)

        self.txtlbl3 = QLabel(self)
        self.txtlbl3.setText("Previous Commands : ")
        self.txtlbl3.setFont(QFont("Trebuchet MS" ,8))
        self.txtlbl3.resize(200 , 12)
        self.txtlbl3.move(20 , 5000)

        self.prev = QTextEdit(self)
        self.prev.setReadOnly(1)
        self.prev.resize(1 , 1)
        self.prev.setFont(QFont("Consolas" ,7))

        self.reset.triggered.connect(app.quit)
        self.exit.triggered.connect(app.quit)
        self.inst.triggered.connect(self.Inst)
        self.about.triggered.connect(self.About)
        self.add.triggered.connect(self.AddObj)
        self.objList.triggered.connect(self.objListfunc)
        self.interpreter.returnPressed.connect(self.UpdateNarrator)

        self.LogoIn()
        
        self.Engine = Engine.Engine(self)

    def LogoIn(self ):
        self.logo = QLabel(self)
        self.logo.setScaledContents(1)
        self.logo.resize(1,1)
        self.logo.move(300 , 100)
        logo = QPixmap("./data/pics/logo1.png")
        self.logo.setPixmap(logo)
        self.logo.setFocus()

        self.logoAnim = QPropertyAnimation(self.logo , "geometry")
        self.logoAnim.setStartValue(QRect(250 , 100 , 1, 1))
        self.logoAnim.setDuration(2000)
        self.logoAnim.setEndValue(QRect(250 , 50 ,775 , 585 ))
        self.logoAnim.setEasingCurve(QEasingCurve.InOutBounce)
        QTimer.singleShot(500 , self.logoAnim , SLOT("start()"))
        self.initilized = 0
	root = Tkinter.Tk()
        self.cloud = QLabel(self)
        cloud = QPixmap("./data/pics/cloud.png")
        self.cloud.setPixmap(cloud)
        self.cloud.resize(cloud.size())
        self.cloud.move(root.winfo_screenwidth() -50, 50)

        self.cloudAnim = QPropertyAnimation(self.cloud , "pos")
        self.cloudAnim.setStartValue(self.cloud.pos())
        self.cloudAnim.setEndValue(QPoint(-300 , 50))
        self.cloudAnim.setDuration(100000)
        self.cloudAnim.setLoopCount(10)
        self.cloudAnim.start()

        self.sun = QLabel(self)
        sun = QPixmap("./data/pics/sun.png")
        self.sun.setPixmap(sun)
        self.sun.resize(sun.size())
        self.sun.move(100 , 2000)

        self.sunAnim = QPropertyAnimation(self.sun , "pos")
        self.sunAnim.setStartValue(self.sun.pos())
        self.sunAnim.setEndValue(QPoint(100 , 50))
        self.sunAnim.setDuration(2000)
        self.sunAnim.start()

        self.t = 0
        self.timer = QBasicTimer()
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(350 , 600 , 600 , 20)
        QTimer.singleShot(2010 , self , SLOT("TimerStart()"))

        self.progAnim = QPropertyAnimation(self.pbar , "pos")
        self.progAnim.setStartValue(QPoint(350 , 1000))
        self.progAnim.setEndValue(QPoint(350 , 600))
        self.progAnim.setDuration(2000)
        self.progAnim.start()

        self.clicklbl = QLabel(self)
        self.clicklbl.setText("Click on XNarrator Logo To Start The App :) ")
        self.clicklbl.setFont(QFont("Trebuchet MS" ,12))
        self.clicklbl.resize(400 , 60)
        self.clicklbl.move(350 , 1000)

        self.cickAnim = QPropertyAnimation(self.clicklbl , "pos")
        self.cickAnim.setStartValue(QPoint(350 , 1000))
        self.cickAnim.setEndValue(QPoint(350 , 560))
        self.cickAnim.setDuration(500)


    def timerEvent(self, e):
        if self.t >= 100 :
            self.cickAnim.start()
            self.timer.stop()
        else :
            self.t += 2
            self.pbar.setValue(self.t)

    def TimerStart(self):
        self.timer.start(100 , self)

    def LogoOut(self):
        self.cloudAnim.stop()

        self.OutAnim = QPropertyAnimation(self.cloud , "pos")
        self.OutAnim.setStartValue(self.cloud.pos())
        self.OutAnim.setEndValue(QPoint(self.cloud.x() , -1000))
        self.OutAnim.setDuration(1000)
        self.OutAnim.start()

        self.OutAnim1 = QPropertyAnimation(self.sun , "pos")
        self.OutAnim1.setStartValue(self.sun.pos())
        self.OutAnim1.setEndValue(QPoint(self.sun.x() , -1000))
        self.OutAnim1.setDuration(1000)
        self.OutAnim1.start()

        self.OutAnim2 = QPropertyAnimation(self.logo , "pos")
        self.OutAnim2.setStartValue(self.logo.pos())
        self.OutAnim2.setEndValue(QPoint(self.logo.x() , -1000))
        self.OutAnim2.setDuration(1000)
        self.OutAnim2.start()

        self.progAnim1 = QPropertyAnimation(self.pbar , "pos")
        self.progAnim1.setStartValue(QPoint(350 , 600))
        self.progAnim1.setEndValue(QPoint(350 , 1000))
        self.progAnim1.setDuration(2000)
        self.progAnim1.start()

        self.cickAnim1 = QPropertyAnimation(self.clicklbl , "pos")
        self.cickAnim1.setStartValue(QPoint(350 , 560))
        self.cickAnim1.setEndValue(QPoint(350 , 1000))
        self.cickAnim1.setDuration(1000)
        self.cickAnim1.start()


    def Reset(self):
        self.interpreter.clear()
        self.info.clear()

    def InitUI(self):
        RemX = self.WinX - 200 - 100
        RemY = self.WinY - 100
        remy = (RemY - 425) / 2

        self.Myanim = QPropertyAnimation(self.interpreter ,"pos")
        self.Myanim.setStartValue(self.interpreter.pos())
        self.Myanim.setEndValue(QPoint(20 , 50))
        self.Myanim.setDuration(2500)
        self.Myanim.setEasingCurve(QEasingCurve.InOutExpo)
        self.Myanim.start()

        self.Myanim0 = QPropertyAnimation(self.txtlbl1 ,"pos")
        self.Myanim0.setStartValue(self.txtlbl1.pos())
        self.Myanim0.setEndValue(QPoint(20 , 32))
        self.Myanim0.setDuration(2500)
        self.Myanim0.setEasingCurve(QEasingCurve.InOutExpo)
        self.Myanim0.start()

        self.Myanim1 = QPropertyAnimation(self.mainview , "geometry")
        self.Myanim1.setDuration(2500)
        self.Myanim1.setStartValue( QRect( self.mainview.pos() , self.mainview.size() ))
        self.Myanim1.setEndValue( QRect(250 ,50, RemX , RemY ) )
        self.Myanim1.setEasingCurve(QEasingCurve.InOutQuart)
        self.Myanim1.start()

        self.BGx , self.BGy = RemX , RemY

        self.Myanim2 = QPropertyAnimation(self.prev , "geometry")
        self.Myanim2.setDuration(2500)
        self.Myanim2.setStartValue( QRect( self.prev.pos() , self.prev.size() ))
        self.Myanim2.setEndValue( QRect(20 , 50 + 25 + remy , 200 , 200 ) )
        self.Myanim2.setEasingCurve(QEasingCurve.InOutQuart)
        self.Myanim2.start()

        self.Myanim3 = QPropertyAnimation(self.info , "geometry")
        self.Myanim3.setDuration(2500)
        self.Myanim3.setStartValue( QRect( self.info.pos() , self.info.size() ))
        self.Myanim3.setEndValue( QRect(20 , 50 + 25 + 200 + 2*remy , 200 , 200 ) )
        self.Myanim3.setEasingCurve(QEasingCurve.InOutQuart)
        self.Myanim3.start()

        self.Myanim4 = QPropertyAnimation(self.txtlbl2 ,"pos")
        self.Myanim4.setStartValue(self.txtlbl2.pos())
        self.Myanim4.setEndValue(QPoint(20 , 50 + 25 + 200 + 2*remy - 15))
        self.Myanim4.setDuration(2500)
        self.Myanim4.setEasingCurve(QEasingCurve.InOutExpo)
        self.Myanim4.start()

        self.Myanim5 = QPropertyAnimation(self.txtlbl3 ,"pos")
        self.Myanim5.setStartValue(self.txtlbl2.pos())
        self.Myanim5.setEndValue(QPoint(20 , 50 + 25 + remy - 15))
        self.Myanim5.setDuration(2500)
        self.Myanim5.setEasingCurve(QEasingCurve.InOutExpo)
        self.Myanim5.start()

    def Inst(self):
        self.newWin = QMainWindow()
        self.newWin.setGeometry(200 , 200 , 300 ,300)
        self.newWin.setWindowTitle("Instructions")
        self.newWin.setWindowIcon(QPixmap("ogo1.png"))
        Instruction = QTextEdit("" ,self.newWin)
        Instruction.insertPlainText(""" Welcome to XNarrator :)\n
        How to use : \n Start typing your command in the interpreter box and hit enter . if your object is not available in our database you can manually add it by using Add Object window in " Object " Menu . \n Your Previous commands and some response from engine will be printed on your screen . \n To use XNarrator properly please kepp in mind that :
                 """)
        Instruction.setFont(QFont("Trebuchet MS" , 8))
        Instruction.resize(300 , 300)
        self.newWin.show()

    def About(self):
        self.newWin1 = QMainWindow()
        self.newWin1.setGeometry(200 , 200 , 300 , 300)
        self.newWin1.setWindowIcon(QPixmap("./data/pics/logo1.png"))
        self.newWin1.setWindowTitle("About")
        About_ = QTextEdit("" , self.newWin1)
        About_.insertPlainText("""What is XNarrator ?\n
it's an app to have fun with ! you ca simply create images from your thinkings . cool huh ? :D
How does this thing called "XNarrtor" Works ? \n
well , it's briefly consisted of three main parts :
1- Narrator , using python modules such as NLTK it processes the natural language into a unique format that our app engine can understand \n
            2- XEngine , it's a hub connecting all parts of XNarraor together and working . figuring out where (and how) to put an object in our window is part of XEngine's capabilities\n
            3- XWindow , Using PySide and QT it's a graphical UI with ability to create objects with different Animated functions .
        \nWho Developed this App ?
            XNarrator was developed by three Software engineers studying in Iran University of Science and Technology , Bardia.H , Arian.H , Kian.P \n

        Why they did it ?
            well , simply it was chance for them to have something of their own ;)

        """)
        About_.setFont(QFont("Trebuchet MS" , 8))
        About_.resize( 300 , 300 )
        self.newWin1.show()
        
    def AddObj(self) : 
        self.newWin2 = QMainWindow()
        self.newWin2.setGeometry(200 , 200 , 320 , 110)
        self.newWin2.setFixedSize(self.newWin2.size())
        self.newWin2.setWindowIcon(QPixmap("./data/pics/logo1.png"))
        self.newWin2.setWindowTitle("Download New Object")
        self.AddLabel = QLabel('Enter an image to download from Google: ',self.newWin2)
        self.AddLabel.move(10,10)
        self.AddLabel.resize(280,25)
        self.AddInput = QLineEdit(self.newWin2)
        self.AddInput.setFont(QFont("Trebuchet MS" , 8))
        self.AddInput.move (10,35)
        self.AddInput.resize( 300 , 30 )
        self.AddState = QLabel('',self.newWin2)
        self.AddState.resize(300,30)
        self.AddState.move(10,70)
        
        self.newWin2.show()  	
        self.AddInput.returnPressed.connect(self.download)
        
    def objListfunc(self) : 
        self.newWin3 = QMainWindow()
        self.newWin3.setGeometry(200 , 200 , 320 , 620)
        self.newWin3.setWindowIcon(QPixmap("./data/pics/logo1.png"))
        self.newWin3.setWindowTitle("Objects list")
	self.objtxt = QTextEdit(self.newWin3) 
	self.objtxt.move(10,10)
	self.objtxt.resize(300,600)
	self.objtxt.setReadOnly(1)
	for i,ob in enumerate(Object.Obj.KeyObjects()):
		self.objtxt.insertPlainText(str(i+1)+'- '+ob.capitalize() +"\n")
	self.newWin3.show()
        
    def download(self):
    	self.AddState.setText("Downloading...")
    	if not self.AddInput.text().lower() in Object.Obj.KeyObjects():
	    	picdl.download(self.AddInput.text().lower())
	    	self.AddState.setText("Downloaded!")
	    	time.sleep(1)
	    	self.newWin2.close()
	else:
	 	self.AddState.setText("This object already exists")

    def InsertInfo(self , text = " Engine Not Responding ! " ):
        """ Inserting New Info to Info Box in Main Window """
        text = "\n " + text
        self.info.insertPlainText(text )

    def UpdateNarrator(self) :
        	self.Engine.run()

    def mousePressEvent(self , event ) :
        if not self.initilized and self.t >= 100  :
            self.LogoOut()
            QTimer.singleShot(1000 , self , SLOT("InitUI()"))
            self.initilized += 1

    def dragEnterEvent(self,e):
        e.accept()
    def dropEvent(self,e):
        source = self.sender()
        position = e.pos()
        source.Move(e.pos().x(),e.pos().y())

    def keyPressEvent(self,e): 
        if e.key() == Qt.Key_Escape:
            self.close()
if __name__ == "__main__":
	app = QApplication(sys.argv)
	win = Window()
	win.show()
	app.exec_()
