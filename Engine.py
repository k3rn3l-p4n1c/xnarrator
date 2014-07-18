from PySide.QtCore import  *
from PySide.QtGui import  *
from X_Interpreter import compile,set
from Object import Object,Obj
from time import sleep
from unicodedata import normalize
from math import pi,sin,cos
import math
import random
import time
import PySide.QtHelp
import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window ,self).__init__()
        self.setWindowTitle("X Narrator")
        self.setGeometry(0,0,800,800)
        self.interpreter = QLineEdit("# NEW sheep 1",self)
        self.interpreter.move(50,650)
        self.interpreter2 = QTextEdit("tell your story:",self)
        self.interpreter2.setGeometry(50,550,200,100)
        self.interpreter2.setReadOnly(True)
        self.engine = Engine(self)
        self.interpreter.returnPressed.connect(self.engine.run)


class Engine():
    def __init__(self,parent):
        self.objects = {}
        self.MainForm = parent
        self.configure_interpreter()
        self.source_code = ""
        self.turn  = 0
        self.trash_count = 0
        
    def setVirtualObjects(self):
    	UP = Object("up",self.MainForm.mainview,1)
    	UP.Move(self.MainForm.mainview.width()/2 -70 ,20 -40 ,1)
    	DOWN = Object("down",self.MainForm.mainview,1)
    	DOWN.Move(self.MainForm.mainview.width()/2 -70 ,self.MainForm.mainview.height()-20 -120 ,1)
    	RIGHT = Object("right",self.MainForm.mainview,1)
    	RIGHT.Move(self.MainForm.mainview.width()-20 -50 ,self.MainForm.mainview.height()/2 -70 ,1)
    	LEFT = Object("left",self.MainForm.mainview,1)
    	LEFT.Move(20 -50 ,self.MainForm.mainview.height()/2 -70 ,1)
    	CENTER = Object("center",self.MainForm.mainview,1)
    	CENTER.Move(self.MainForm.mainview.width()/2 -90 ,self.MainForm.mainview.height()/2 -90 ,1)
    	OUT = Object("out",self.MainForm.mainview,1)
    	OUT.Move(self.MainForm.mainview.width()*2 -70 ,self.MainForm.mainview.height()*2 -70 ,1)
    	
    	self.objects["up"] = UP
    	self.objects["down"] = DOWN
    	self.objects["right"] = RIGHT
    	self.objects["left"] = LEFT
    	self.objects["center"] = CENTER
    	self.objects["out"] = OUT
    	
    def configure_interpreter(self):
        self.setup_inputs = Obj.KeyObjects()+['up','down','right','left','center','out']
        set(self.setup_inputs)
        	
    def run(self):
    	toPrev = self.MainForm.interpreter.text()
    	try:
    		toPrev = normalize('NFKD', toPrev).encode('ascii','ignore')
    	except:
    		pass
        self.MainForm.prev.insertPlainText("\n" + toPrev)
    	if toPrev[:2] == '>>':
    		newin = toPrev[4:]
    	elif toPrev[:2] == './':
    		newin =open(toPrev).read()
    	elif toPrev[:2] == '# ':
    		self.run_line(toPrev[2:])
    		return
    	else:
    		raise TypeError()
    	if newin[-1] != '.':
    		newin += '.'

    	self.source_code += '\n' + newin
    	set(self.setup_inputs)
    	lines = compile(self.source_code)
	for line in lines[self.turn:]:
		self.MainForm.InsertInfo(line)
		self.run_line(line)
	self.MainForm.interpreter.clear()
        self.MainForm.interpreter.setText(">>> ")
     
    def run_line(self,line):
	    self.turn += 1
	    self.setVirtualObjects()
            cmd = line.split()[0]
            if cmd == "NEW":
                obj_type = line.split()[1]
                obj_count = int(line.split()[2])
                newObj = Object(obj_type,self.MainForm.mainview,obj_count)
                newObj.MakeRandom()
                location = self.GetFree(newObj)
                n = 0
                while Engine.notinscreen(newObj,self.MainForm.mainview,location):
                    n+=1
                    location = self.GetFree(newObj)
                    if n > 500:
                        break

                newObj.Move(location[0],location[1])
                newObj.ChangeVisibility(1)
                if newObj.name in ['up','down','right','left','center','out']:
                	return
                if newObj.name not in self.objects.keys():
                    self.objects[newObj.name] = newObj
                    self.objects[newObj.name].MakeRandom()
                else:
                    name = self.trash_name(newObj.name)
                    self.objects[newObj.name].SetName(name)
                    self.objects[name] = self.objects[newObj.name]
                    self.objects[newObj.name] = newObj
                    self.objects[newObj.name].MakeRandom()
                self.Indent_config()

            elif cmd == "SETNAME":
                self.objects[line.split()[1]].SetName(line.split()[2])
                self.objects[line.split()[2]] = self.objects[line.split()[1]]
                self.objects.pop(line.split()[1])
            elif cmd.split()[0] == "MOVE":
            	obj_name = line.split()[1]
            	if line.split()[2] == 'out':
            		print 'FadeSide'
            		self.objects[obj_name].FadeSide()
            		sleep(1)
            		return
                n=0
                if line.split()[3] != 'IN':
                	pos = self.FindPos(self.objects[line.split()[1]],self.objects[line.split()[2]],line.split()[3])
                	pos = (pos[0] - self.objects[line.split()[1]].w/2 , pos[1] - self.objects[line.split()[1]].h/2 )
                else:
                	pos = (self.objects[line.split()[2]].x,self.objects[line.split()[2]].y)
    	        self.objects[obj_name].Move(pos[0],pos[1],Engine.FindMag(self.objects[obj_name],self.objects[line.split()[2]],line.split()[3]))
                self.objects[obj_name].indent = Engine.FindIndent(self.objects[line.split()[1]],self.objects[line.split()[2]],line.split()[3])
                self.objects[line.split()[1]].MakeRandom()
		
            elif cmd.split()[0] == "SAY": 
             self.objects[line.split()[1]].Say(line.split()[2])
             self.objects[line.split()[1]].Shake()
            elif cmd.split()[0] == "EAT":
                self.objects[line.split()[1]].Eat(self.objects[line.split()[2]])
            sleep(1)
      
    def trash_name(self):
    	self.trash_count += 1
    	return str(self.trash_count)
    	
    def FindPos(self,obj1,obj2,dir):
        xcm = obj2.x + obj2.w/2
        ycm = obj2.y + obj2.h/2

        r = math.pi + random.random()*math.pi
        rand = 0.5+random.random()/2
        
        radius = random.randint(1,int(math.sqrt(obj2.h**2+obj2.w**2)*2))
        radius2 = random.randint(1,min(obj2.h,obj2.w)+min(obj1.h,obj1.w))
        while radius > 0:
		dirdic = {
		"NEAR":( radius2*math.cos(r), radius2*math.sin(-r)),
		"RIGHT":(obj2.w/2 , 0),
		"LEFT":(-obj2.w/2 , 0),
		"TOP":(0 , -obj2.h/2 ),
		"BOTTOM":(0 , obj2.h/2),
		"ON":( (radius*math.cos(r)/20) , (radius*math.sin(-r)/20) ),
		"UNDER":( (radius*math.cos(r)/3),(radius*math.sin(-r)/3) ),
		"INSIDE":( (radius*math.cos(r)/10) , (radius*math.sin(-r)/10) ),
		"IN":( 0.0 , 0.0 )}
		x= xcm+dirdic[dir][0] - obj1.w/2
		y=ycm+dirdic[dir][1] - obj1.h/2
		if 0<x<self.MainForm.mainview.width() and 0<y<self.MainForm.mainview.height() and 0<x+obj1.w<self.MainForm.mainview.width() and 0<y+obj1.h<self.MainForm.mainview.height():
        		return (x+obj1.w/2,y+obj1.h/2)
        	radius -= 10
        return (obj1.x,obj1.y)
    @staticmethod
    def FindMag(obj1,obj2,dir):
        m = 1 
        if dir == "INSIDE" or dir == "IN": # later these two ifs will be separated!
            avobj1 = float((float(obj1.w) + float(obj1.h)))/2
            avobj2 = float((float(obj2.w) + float(obj2.h)))/2
            m = avobj1 / avobj2
        return m


    @staticmethod
    def FindIndent(obj1,obj2,dir):
        if dir == "UNDER" or dir == "INSIDE":
            if obj1.indent >= obj2.indent:
                Engine.setindent(obj1,obj2)
                return obj2.indent -1
        elif dir == "ON" or dir =="IN":
            if obj1.indent <= obj2.indent:
                Engine.setindent(obj2,obj1)
                return obj2.indent +1
        return obj1.indent
        
    @staticmethod
    def notinscreen(obj,window,cor):
        if cor[0] + obj.w > window.width()+window.x() or cor[1] + obj.h > window.height()+window.y() :
            return True
        return False
    @staticmethod
    def setindent(obj1,obj2):
        for obj in obj1.objects:
            obj.stackUnder(obj2.objects[0])

    def Indent_config(self):
        indlist = list()
        for i in self.objects.values():
            indlist.append((i.indent,i))
        for j in sorted(indlist):
            j[1].SetIndent()

    def RandomPos(self,newobj):
    	radius = 50*random.random()
    	alpha = 2*pi*random.random()
        return (radius*cos(alpha)+self.MainForm.mainview.width()/2 - newobj.w/2 , radius*sin(alpha)+self.MainForm.mainview.height()/2 - newobj.h/2 + 70)
        
    def GetFree(self,newobj):
        info = []
        choices =  []
        l1=[]
        for obj in self.objects.values():
            if obj.indent == newobj.indent or (abs(obj.indent - newobj.indent)==1 and(obj.indent> -6 or obj.indent>0 or newobj.indent>0)): 
                l1.append(obj.x)
                l1.append(obj.y)
                l1.append(obj.w)
                l1.append(obj.h)
                info.append(l1)
            l1=[]
        if len(self.objects) == 0 or len(info)==0 :
            return self.RandomPos(newobj)
        else:
            for y in range(10,self.MainForm.mainview.height()-10,5):
                for x in range(10,self.MainForm.mainview.width()-10,5):
                    around = 0
                    flag= True
                    for i in info:
                        if (y <= i[1]+60 <= y+newobj.h) or (y<=i[1]+i[3]-60<=y+newobj.h) or (i[1]+60<=y<=i[1]+i[3]-60) or (i[1]+60<=y+newobj.h<=i[1]+i[3]-60):
                            around += 1
                            if (x >= i[0]+i[2] or x+newobj.w <= i[0]) and not(self.notinscreen(newobj,self.MainForm.mainview,[x,y])):
                                choices.append([x,y])
                            else:
                                flag = False
                    if flag:
                        return [x,y]
                    if around == 0 and not(self.notinscreen(newobj,self.MainForm.mainview,[x,y])):
                        return [x,y]
            if len(choices)==0:
                t = self.RandomPos(newobj)
                while Engine.notinscreen(newobj,self.MainForm.mainview,t):
                    t = self.RandomPos(newobj)
                return t
            
if __name__ == "__main__":
	App = QApplication(sys.argv)
	MainForm = Window()
	MainForm.show() 
	App.exec_()


    
