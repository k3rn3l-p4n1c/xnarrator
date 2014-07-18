from PySide.QtCore import *
from PySide.QtGui import *
import time as Time
import math
import random
import os
import PySide.QtHelp
import sys

class Window(QMainWindow) :
    """ Just for testing , will be deleted later ;) """
    def __init__( self ):
        super(Window ,self).__init__()
        self.setWindowTitle("Sheeep ! ")
        self.setGeometry(100 , 100 ,  800, 700)
        self.mainWindow = QLabel(self)
        self.bg = QPixmap("landscape_0.png")
        self.mainWindow.resize(self.bg.size())
        self.mainWindow.setPixmap(self.bg)

class Obj(QLabel) :
    @staticmethod
    def KeyObjects():
    	objs = []
        for imgname in os.listdir("./data/pics") :
            objs.append(imgname.split("_")[0])
        return objs
        
    def __init__(self , type , parent , X = 0 , Y = 0 , vis = -1 ) :
        super(Obj ,self).__init__()

        availableImages = []
        for imgname in os.listdir("./data/pics") :
            if imgname.split("_")[0] == type :
                availableImages.append(imgname)
        if len(availableImages) :
            fname = random.choice(availableImages)
        else :
        	fname = "<<nothing>>_0_2.png"
        directory = "./data/pics/".rstrip() + fname

        self.setParent(parent)
        self.parent = parent
        self.file_name = fname

        self.x = X
        self.y = Y
        self.visibilty = vis 

        self.pic = QPixmap(directory)
        self.setPixmap(self.pic)
        
        self.setsize()
        self.setScaledContents(True)
        self.move(X ,Y)
        self.w = self.width()
        self.h = self.height()
        self.name = type
        self.type = type
        
    def setsize(self):
    	size_i = int(self.file_name.split('_')[2][0])
    	current_size = (float(self.pic.width()),float(self.pic.height()))
    	if size_i == 0: n_size = (25,25)
    	if size_i == 1: n_size = (50,50)
    	if size_i == 2: n_size = (100,100)
    	if size_i == 3: n_size = (150,150)
    	if size_i == 4: n_size = (300,300)
    	if size_i == 5: n_size = (400,400)
    	if size_i == 6: n_size = (800,800)
    	k1,k2 = n_size[0]/current_size[0],n_size[1]/current_size[1]
    	k = min(k1,k2)
    	self.resize(self.pic.width()*k,self.pic.height()*k)
    	self.first_ind = -size_i
    	

    def ChangeVisibility(self , vis = 0):
        """ Make an object invisible - should be used """
        if vis == -1 :
            self.hide()
            self.visibilty = -1
        else :
            self.show()
    def Move(self, x=0 , y=0 ,time = 2 ,mag = 1) :
        """  moves the self Object to x , y """
        self.anim = QPropertyAnimation(self , "geometry")
        self.anim.setDuration(1000 * time)
        self.anim.setStartValue( QRect( self.pos() , self.size() ))
        self.anim.setEndValue( QRect(x , y, self.w*mag , self.h * mag) )
        self.anim.setEasingCurve(QEasingCurve.OutExpo)
        self.anim.start()
        if mag > .01 :
            self.x = x
            self.y = y
            self.h *= mag
            self.w *= mag


    def FadeOut(self ,time = .8 ):
        """ A fancier ChangeVisibility , note that self.(x,y,h,w) don't change after calling this method so that fade in can be called later """
        self.Move(self.x , self.y , time , .001 )
        self.visibilty = 0
    def FadeIn(self , time = .8 ):
        """
        a fancier way of creating an object
        how to use : Create an Object and make make in invisible using the ChangeVisibilty Method and than call FadeIn
        """
        if self.visibilty == 1 :
            pass
        else :
            if self.visibilty == 2 :
                self.Move(self.x , self.y , time , 1)
            else :
                self.FadeOut()
                self.ChangeVisibility(1)
                self.Move(self.x , self.y , time , 1 )
            self.visibilty = 1
    def FadeSide(self):
        null = [1 ,-1 ]
        self.anim = QPropertyAnimation(self , "geometry")
        self.anim.setDuration(1200)
        self.anim.setStartValue( QRect( self.pos() , self.size() ))
        self.anim.setEndValue( QRect(3000 * random.choice(null) , self.y, self.w*.5 , self.h*.5) )
        self.anim.setEasingCurve(QEasingCurve.InCurve)
        self.anim.start()
        self.x = 2000

    def Info(self):
        print "x = {} , y = {} , w = {} , h = {} , name = {} , indent = {} ".format(self.x , self.y , self.w , self.h , self.name , self.indent())

    def Shake(self):
        self.anim = QPropertyAnimation(self , "geometry")
        self.anim.setStartValue(QRect( self.pos() , self.size() ))
        for i in range(1,31):
        	self.anim.setKeyValueAt(i/30.0, QRect(self.x+(6*(-1)**i) , self.y, self.w , self.h ) )
        self.anim.setDuration(500 )
        self.anim.setEndValue(QRect(self.x , self.y, self.w , self.h ) )
        self.anim.setEasingCurve(QEasingCurve.InCirc)
        self.anim.start()


    def mousePressEvent(self,event):
        global Clicktime

        Clicktime = [QCursor.pos().x(),QCursor.pos().y()]
        QLabel.mousePressEvent(self,event)


    def mouseReleaseEvent(self,e):
        if QCursor.pos().x() - Clicktime[0] ==0 and QCursor.pos().y() - Clicktime[1]==0:
            self.Shake()
            QSound.play(str(self.type)+".wav")
            QSound.play(str(self.type)+".mp3")

    def mouseMoveEvent(self,event):
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QCursor.pos()-self.rect().topLeft())
        dropAction = drag.start(Qt.MoveAction)
        self.Move(QCursor.pos().x()-self.parent.x()-self.w/2,QCursor.pos().y()-self.parent.y()-self.h)

class Object() :
    def __init__(self , type , parent , count = 2 , vis = 1, X=0 , Y=0 ):

        self.parent = parent
        self.visibilty = vis
        self.name = type
        self.otype = type

        a = Obj(type , parent , X , Y)
        a.hide()
        Width = a.w
        self.x = a.x
        self.y = a.y
        self.w = a.w * count
        self.h = a.h
        self.indent = a.first_ind

        self.objects = []
        for i in range(count) :
            self.objects.append( Obj(type , parent , X + (i*Width) , Y) )

        self.cloud = Obj("<<talk>>" , self.parent ,0 ,0)
        xx = a.w / self.cloud.w
        yy = a.h / self.cloud.h
        magn = ( xx + yy ) / 2
        self.cloud.Move(0,0 , .0000001 , magn)
        self.cloud.Move(self.x - self.cloud.w*.8 , self.y - self.cloud.h*.8 , .0000001 , 1) 
        self.cloud.FadeOut(.00001)
        self.ChangeVisibility(vis)
        self.MakeRandom(1) 
        
    def SetIndent(self ):
        for obj in self.objects :
            obj.raise_()

    def SetName(self , name):
        """ Change the Object name """
        self.name = name
    def Move(self ,x = 200 ,y= 200  ,time = 2 ,mag =1):
        for i ,obj in enumerate(self.objects) :
             obj.Move(x + (i * obj.w *mag) ,y ,time ,mag)
        self.cloud.Move( x - self.cloud.w , y - self.cloud.h   , .00001 , 1)
        self.cloud.FadeOut(.00001)
        self.x = x
        self.y = y
        self.w *= mag
        self.h *= mag

    def FadeOut(self , time = .8) :
        for obj in self.objects :
            obj.FadeOut(time)
        self.visibilty = 0
    def FadeIn(self ,time = .8):
        for obj in self.objects :
            obj.FadeIn()
        self.visibilty = 1
    def ChangeVisibility(self , vis = 1 ):
        for obj in self.objects :
            obj.ChangeVisibility(vis)
        self.visibilty = vis
        
    def Test(self):
        """ Just for testing , will be deleted later ;) """
        self.test = QPushButton("CObj Test ! " , self.parent)
        self.Test = QPushButton("CObj Test ! " , self.parent)
        self.test.move(600 , 200 )
        self.Test.move(600 , 250 )
        self.test.clicked.connect(self.Move)
        self.Test.clicked.connect(self.Eaten)

    def Say(self ,text = "Joon ! " , time = 3): # changed
        self.cloud.raise_()
        self.cloud.FadeIn(.5)
        Text = QLabel(self.parent)
        Text.setText(text)
        Text.move(self.cloud.x+40,self.cloud.y+20)
        Text.setFont(QFont("Comic Sans MS" , 13))
        Text.show()
        QTimer.singleShot(time*1000 ,Text , SLOT("hide()"))
        QTimer.singleShot(time*1000 ,self.cloud, SLOT("FadeOut()"))

    def MakeRandom(self , effect =  1 ):
        newW = []
        newH = []
        for obj in self.objects :
            obj.Move(self.x + random.randrange(0 , 100 * effect ) , self.y + random.randrange(0 , 100 * effect ) , .5 , 1 )
            newH.append(obj.y)
            newW.append(obj.x)

        self.w = max(newW) - min(newW) + obj.w
        self.h = max(newH) - min(newH) + obj.h

    def Shake(self):
        for obj in self.objects :
            obj.Shake()

    def Info(self):
        for obj in self.objects :
            obj.Info()

    def FadeSide(self):
        for obj in self.objects :
            obj.FadeSide()
            
    def Eaten(self , killer) : 
        for obj in self.objects : 
            obj.Eaten(killer) 


if __name__ == "__main__":
	App = QApplication(sys.argv)
	win = Window()
	kian = Object( "wolf" ,win , 1 , 1 , 500 , 500)
	sheep = Object( "sheep" , win , 1 , 1 , 200 , 200 )
	sheep.Test()
	win.show()
	App.exec_()
	
