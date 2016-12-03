#!/usr/local/bin/python3.3
# -*- coding: utf-8 -*-
# Crée par Marc-Alexandre Blanchard

from tkinter import *
import os,time,tkinter.messagebox,signal,subprocess,sys

class Application(object):
    """ SHOCK """

    _Version,_debug=1.0,False
    _MusicProcessPID = 999999
    _ONPLAY,_Alive,_HEALTH,_POWER,_BOSSLIFE,_Walking,_Attacking,_Jumping,_INVULNERABILITY,_CurrentLVL,_nbCoins,_PaddingX,_PaddingY,_step,_direction,_condition,_WIDTH,_HEIGHT,_posX,_posY,_BallposX,_BallposY,_BallDirection,_state,_Border,_Ground,_danger,_RDV = False,True,5,0,0,False,False,False,False,1,0,0,0,"B","R","1",750,510,12,15,0,0,"R",1,["002","00B","0T0","0T1","0T2","T01","T01","T02","T03","T04","T05","T06","BK1","BK2"],["001","002","0T0","0T2","BK1","BK2"],["A01","B01"],[]
    _Menu,_BACKGROUND0,_TILESBACKGROUND0,_BACKGROUND1,_TILESBACKGROUND1,_MAP,_TILESMAP,_ITEMS,_TILESITEMS,_ENEMIES,_TILESENEMIES,_PowerBallTile,_HealthBar,_CoinDisplay,_LightningDisplay=None,[],[],[],[],[],[],[],[],[],[],[],[None,None,None,None,None],[None,None,None],[None,None,None]
    _invulnerabilityTime,_positionCheckTime,_propagationTime,_gravityTime,_stepTime,_enemiesTime,_coinRotationTime,_coreRotationTime,_lightningMvtTime,_soundLevelTime=1000,50,50,300,100,500,100,100,200,12000
            
    def __init__(self):
        self._tk = Tk()
        self._tk.title("SHOCK")
        self.createMenuBar()
        self._tk.lift()
        self._tk.resizable(width=False, height=False)
        self._tk.geometry("+%d+%d" % ((self._tk.winfo_screenwidth() - self._tk.winfo_reqwidth()) / 4, (self._tk.winfo_screenheight() - self._tk.winfo_reqheight()) / 4))
        self._FRAME = Canvas(self._tk, width=self._WIDTH, height=self._HEIGHT)
        if(sys.platform.startswith("darwin")):
            self._tk.bind_all('<Command-q>',self.quit)
            self._tk.bind_all('<Command-Q>',self.quit)
        self._FRAME.bind_all('<Key>',self.onKeyPress)
        self._FRAME.bind_all('<Left>',self.onLeftPress)
        self._FRAME.bind_all('<Right>',self.onRightPress)
        self._FRAME.bind_all('<Up>',self.onUpPress)
        self._FRAME.bind_all('<Down>',self.onDownPress)
        self._FRAME.pack()
        self.drawScreen("startscreen")

    def mainloop(self):
        self._tk.mainloop()

    def initialisation(self,HP,COINS,POWER,idlevel,X,Y,state,condition):
        self._tk.title("SHOCK")
        self.cancelation()
        self._FRAME.delete(ALL)
        self._ONPLAY,self._Alive,self._HEALTH,self._nbCoins,self._POWER,self._CurrentLVL,self._posX,self._posY,self._state,self._PaddingX,self._PaddingY,self._Menu,self._BACKGROUND0,self._TILESBACKGROUND0,self._BACKGROUND1,self._TILESBACKGROUND1,self._MAP,self._TILESMAP,self._ITEMS,self._TILESITEMS,self._ENEMIES,self._TILESENEMIES,self._PowerBallTile,self._HealthBar,self._CoinDisplay,self._LightningDisplay,self._condition=True,True,HP,COINS,POWER,idlevel,X,Y,state,0,0,None,[],[],[],[],[],[],[],[],[],[],[],[None,None,None,None,None],[None,None,None],[None,None,None],condition
        self.load()
        self.draw()        
        self.drawMan(Y)
        self.drawDisplays(self._HEALTH,self._nbCoins,self._POWER)
        self.Animation(1,4,1,"_COIN","tiles/I0",self._coinRotationTime,None)
        self.Animation(6,9,6,"_CORE","tiles/I0",self._coreRotationTime,None)
        self.Animation(10,13,10,"_LIGHTNING","tiles/I",self._lightningMvtTime,None)
        self._BOSSLIFE = 12 if(self._CurrentLVL==3) else 0
        self.positionCheck()
        self.toggleEnemies()
        self.killSound()
        if(self._CurrentLVL !=3):
            self.playSound("music_level_"+str(self._CurrentLVL)+".m4a",True)
        if(self._CurrentLVL%2!=0):
            self.moveEnemies(-30,0)
        elif(self._CurrentLVL%2==0):
            self.moveEnemies(0,30)
        self._enemiesTime = 250 if(self._CurrentLVL==3) else 500

    def onKeyPress(self,event):
        if(event.char=="q" or event.char=="Q"):
            self.toTheLeft()
        elif(event.char=="d" or event.char=="D"):
            self.toTheRight()
        elif(event.char=="z" or event.char=="Z" or event.char==" "):
            self.jump()
        elif(event.char=="x" or event.char=="X"):
            self.attack()
        elif(event.char=="j" or event.char=="J"):
            self.save()
        elif(event.char=="l" or event.char=="L"):
            self.loadsave()
        elif(event.char=="a" or event.char=="A"):
            self.about()
        elif(event.char=="h" or event.char=="H"):
            self.help()
        elif((event.char=="p" or event.char=="P") and self._debug):
            self.screenshot()
        elif(event.char=="v" or event.char=="V"):
            self.version()
        elif(event.char=="r" or event.char=="R"):
            self.initialisation(3,0,0,1,12,15,1,"1")

    def createMenuBar(self):
        self._tk.protocol("WM_DELETE_WINDOW", self.onQuit)
        self.menubar = Menu(self._tk)
        self.appmenu = Menu(self.menubar, tearoff=0)
        self.appmenu.add_command(label="Load", command=self.loadsave)
        self.appmenu.add_command(label="Save", command=self.save)
        self.appmenu.add_command(label="Quit", command=self._tk.destroy)
        self.menubar.add_cascade(label="SHOCK", menu=self.appmenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.about)
        self.helpmenu.add_command(label="Help & How-To", command=self.help)
        self.helpmenu.add_command(label="Version", command=self.version)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self._tk.config(menu=self.menubar)

    def onQuit(self):
        self.cancelation()
        self.killSound()
        self._tk.destroy()

    def quit(self,event):
        self.onQuit()

    def about(self):
        tkinter.messagebox.showinfo("About", "Created, designed & imagined by\n\nMarc-Alexandre Blanchard\n\nmarc-alx@outlook.com")

    def help(self):
        tkinter.messagebox.showinfo("Help & How-To", "About : A\nHelp & How-To : H\nVersion : V\n\nMove : Q D ← →\nJump : Z ↑ Spacebar\nAttack : S ↓\n\nLoad : L\nRestart : R\nSave : J")
    
    def version(self):
        tkinter.messagebox.showinfo("Version", "Version "+str(self._Version))

    def load(self):
        self.loadFile("levels/"+str(self._CurrentLVL)+"/background_1.txt",self._BACKGROUND1,self._TILESBACKGROUND1)
        self.loadFile("levels/"+str(self._CurrentLVL)+"/background_0.txt",self._BACKGROUND0,self._TILESBACKGROUND0)
        self.loadFile("levels/"+str(self._CurrentLVL)+"/level.txt",self._MAP,self._TILESMAP)
        self.loadFile("levels/"+str(self._CurrentLVL)+"/items.txt",self._ITEMS,self._TILESITEMS)
        self.loadFile("levels/"+str(self._CurrentLVL)+"/enemies.txt",self._ENEMIES,self._TILESENEMIES)

    def save(self):
        if(not os.path.exists("saves")):
            os.mkdir("saves")
        f = open("saves/save.txt","w")
        f.write(str(self._HEALTH)+"#"+str(self._nbCoins)+"#"+str(self._POWER)+"#"+str(self._CurrentLVL)+"#"+str(self._posX)+"#"+str(self._posY)+"#"+str(self._state)+"#"+str(self._condition))
        f.close()

    def loadsave(self):
        if(os.path.isfile("saves/save.txt")):
            f = open("saves/save.txt","r")
            lignes  = f.readlines()
            f.close()
            res = lignes[0].split('#')
            self.initialisation(int(res[0]),int(res[1]),int(res[2]),int(res[3]),int(res[4]),int(res[5]),int(res[6]),res[7])
        else:
            self.initialisation(3,0,0,1,12,15,1,"1")

    def draw(self):
        for j in range(0,len(self._MAP),1):
            for i in range (0,len(self._MAP[j]),1):
                self._TILESBACKGROUND1[j][i]=PhotoImage(file="tiles/"+self._BACKGROUND1[j][i]+".gif")
                self._FRAME.create_image(30*i,30*j, image=self._TILESBACKGROUND1[j][i], tag="_BACKGROUND1")

                self._TILESBACKGROUND0[j][i]=PhotoImage(file="tiles/"+self._BACKGROUND0[j][i]+".gif")
                self._FRAME.create_image(30*i,30*j, image=self._TILESBACKGROUND0[j][i], tag="_BACKGROUND0")

                self._TILESMAP[j][i]=PhotoImage(file="tiles/"+self._MAP[j][i]+".gif")
                self._FRAME.create_image(30*i,30*j, image=self._TILESMAP[j][i], tag=("_MAP","ELMT_"+str(j)+"_"+str(i)))

                self._TILESITEMS[j][i]=PhotoImage(file="tiles/"+self._ITEMS[j][i]+".gif")
                if(self._ITEMS[j][i]=="I01"):
                    self._FRAME.create_image(30*i,30*j, image=self._TILESITEMS[j][i], tag=("_ITEM","_COIN",self._ITEMS[j][i],"IDITEM_"+str(j)+"_"+str(i)))
                if(self._ITEMS[j][i]=="I05"):
                    self._FRAME.create_image(30*i,30*j, image=self._TILESITEMS[j][i], tag=("_ITEM","_CAP","IDITEM_"+str(j)+"_"+str(i)))
                if(self._ITEMS[j][i]=="I06"):
                    self._FRAME.create_image(30*i,30*j, image=self._TILESITEMS[j][i], tag=("_ITEM","_CORE",self._ITEMS[j][i],"IDITEM_"+str(j)+"_"+str(i)))
                if(self._ITEMS[j][i]=="I10"):
                    self._FRAME.create_image(30*i,30*j, image=self._TILESITEMS[j][i], tag=("_ITEM","_LIGHTNING",self._ITEMS[j][i],"IDITEM_"+str(j)+"_"+str(i)))

                self._TILESENEMIES[j][i]=PhotoImage(file="tiles/"+self._ENEMIES[j][i]+".gif")
                if(self._ENEMIES[j][i]=="A01"):
                    self._FRAME.create_image(30*i,30*j, image=self._TILESENEMIES[j][i], tag=("_ENEMIES","_GHOST","IDENEMY_"+str(j)+"_"+str(i)))
                else:
                    self._FRAME.create_image(30*i,30*j, image=self._TILESENEMIES[j][i], tag=("_ENEMIES","IDENEMY_"+str(j)+"_"+str(i)))
        self._FRAME.tag_raise("_GHOST")

    def playSound(self,filename,repetitive):
        if(sys.platform.startswith("darwin")):
            process = subprocess.Popen(["afplay", "sounds/"+filename])
            if(repetitive):
                self._MusicProcessPID=process.pid
                self._RDV.append(self._FRAME.after(self._soundLevelTime,lambda x = filename : self.playSound(x,repetitive)))

    def killSound(self):
        if(self._MusicProcessPID!=999999):
            os.kill(self._MusicProcessPID,signal.SIGKILL)
            
    def move(self,X,Y):
        self._FRAME.move("_BACKGROUND1",X,Y)
        self._FRAME.move("_BACKGROUND0",X,Y)
        self._FRAME.move("_MAP",X,Y)
        self._FRAME.move("_ITEM",X,Y)
        self._FRAME.move("_ENEMIES",X,Y)

    def moveEnemies(self,X,Y):
        if(self._CurrentLVL%2!=0):
            if(X==-30 and self._PaddingX == -2):
                X,self._PaddingX=30,self._PaddingX+1
            elif(X==30 and self._PaddingX == 2):
                X,self._PaddingX=-30,self._PaddingX-1
            else:
                self._PaddingX = (self._PaddingX-1) if(X==(-30)) else (self._PaddingX+1)
        elif(self._CurrentLVL%2==0):
            if(Y==-30 and self._PaddingY == -2):
                Y,self._PaddingY=30,self._PaddingY+1
            elif(Y==30 and self._PaddingY == 2):
                Y,self._PaddingY=-30,self._PaddingY-1
            else:
                self._PaddingY = (self._PaddingY-1) if(Y==(-30)) else (self._PaddingY+1) 
        self._FRAME.move("_ENEMIES",X,Y)
        self._RDV.append(self._FRAME.after(self._enemiesTime,lambda a = X : self.moveEnemies(a,Y)))

    def toggleEnemies(self):
        for j in range(0,len(self._MAP),1):
            for i in range (0,len(self._MAP[j]),1):
                if(self._ENEMIES[j][i][0]=='A'):
                    self._ENEMIES[j][i]='B'+self._ENEMIES[j][i][1]+self._ENEMIES[j][i][2]
                    self._TILESENEMIES[j][i]=PhotoImage(file="tiles/"+self._ENEMIES[j][i]+".gif")
                    self._FRAME.itemconfigure("IDENEMY_"+str(j)+"_"+str(i),image=self._TILESENEMIES[j][i])
                elif(self._ENEMIES[j][i][0]=='B'):
                    self._ENEMIES[j][i]='A'+self._ENEMIES[j][i][1]+self._ENEMIES[j][i][2]
                    self._TILESENEMIES[j][i]=PhotoImage(file="tiles/"+self._ENEMIES[j][i]+".gif")
                    self._FRAME.itemconfigure("IDENEMY_"+str(j)+"_"+str(i),image=self._TILESENEMIES[j][i])
        self._RDV.append(self._FRAME.after(self._enemiesTime,self.toggleEnemies))

    def propagation(self):
        self._BallposX,n = (self._BallposX+1) if(self._BallDirection=="R") else (self._BallposX-1),30 if(self._BallDirection=="R") else -30
        self._FRAME.move("_POWERBALL",n,0)
        if((self._MAP[self._BallposY][self._BallposX] not in self._Border) and (self._MAP[self._BallposY-1][self._BallposX] not in self._Border)):
            if(((self._ENEMIES[self._BallposY-self._PaddingY][self._BallposX-self._PaddingX] != "I00") and len(self._FRAME.find_withtag("IDENEMY_"+str(self._BallposY-self._PaddingY)+"_"+str(self._BallposX-self._PaddingX)))==1) or ((self._ENEMIES[self._BallposY-1-self._PaddingY][self._BallposX-self._PaddingX] != "I00") and len(self._FRAME.find_withtag("IDENEMY_"+str(self._BallposY-1-self._PaddingY)+"_"+str(self._BallposX-self._PaddingX)))==1)):
                self._FRAME.delete("IDENEMY_"+str(self._BallposY-self._PaddingY)+"_"+str(self._BallposX-self._PaddingX))
                self._FRAME.delete("IDENEMY_"+str(self._BallposY-1-self._PaddingY)+"_"+str(self._BallposX-self._PaddingX))
                self._FRAME.delete("_POWERBALL")
                self.playSound("DestroyGhostSound.m4a",False)
                self._Attacking=False
                if(self._CurrentLVL==3):
                    self._BOSSLIFE-=1
            else:
                self._FRAME.after(self._propagationTime,self.propagation)
        else:
            self._FRAME.delete("_POWERBALL")
            self._Attacking=False

    def positionCheck(self):
        TAG_I_U,TAG_I_D="IDITEM_"+str(self._posY-1)+"_"+str(self._posX),"IDITEM_"+str(self._posY)+"_"+str(self._posX)
        TAG_E_U,TAG_E_D="IDENEMY_"+str(self._posY-1-self._PaddingY)+"_"+str(self._posX-self._PaddingX),"IDENEMY_"+str(self._posY-self._PaddingY)+"_"+str(self._posX-self._PaddingX)
        if(self._ITEMS[self._posY][self._posX]=="I01" and len(self._FRAME.find_withtag(TAG_I_D))==1):
            self._FRAME.delete(TAG_I_D)
            self.gainCoin()
        if(self._ITEMS[self._posY-1][self._posX]=="I01" and len(self._FRAME.find_withtag(TAG_I_U))==1):
            self._FRAME.delete(TAG_I_U)
            self.gainCoin()
        if(self._ITEMS[self._posY][self._posX]=="I05" and len(self._FRAME.find_withtag(TAG_I_D))==1):
            self._FRAME.delete(TAG_I_D)
            self._condition="2"
            self.playSound("CapSound.m4a",False)
        if(self._ITEMS[self._posY][self._posX]=="I06" and len(self._FRAME.find_withtag(TAG_I_D))==1):
            self._FRAME.delete(TAG_I_D)
            self.healthPlus()
        if(self._ITEMS[self._posY-1][self._posX]=="I06" and len(self._FRAME.find_withtag(TAG_I_U))==1):
            self._FRAME.delete(TAG_I_U)
            self.healthPlus()
        if(self._ITEMS[self._posY][self._posX]=="I10" and len(self._FRAME.find_withtag(TAG_I_D))==1):
            self._FRAME.delete(TAG_I_D)
            self.playSound("LightningPlusSound.m4a",False)
            self.ActualisePower(self._POWER+1)
        if(self._ITEMS[self._posY-1][self._posX]=="I10" and len(self._FRAME.find_withtag(TAG_I_U))==1):
            self._FRAME.delete(TAG_I_U)
            self.playSound("LightningPlusSound.m4a",False)
            self.ActualisePower(self._POWER+1)
        if(self._MAP[self._posY][self._posX]=="END"):
            self._CurrentLVL+=1
            self.initialisation(self._HEALTH,self._nbCoins,self._POWER,self._CurrentLVL,12,15,self._state,self._condition)
        if(((self._ENEMIES[self._posY-1-self._PaddingY][self._posX-self._PaddingX] in self._danger and len(self._FRAME.find_withtag(TAG_E_U))==1) or (self._ENEMIES[self._posY-self._PaddingY][self._posX-self._PaddingX] in self._danger and len(self._FRAME.find_withtag(TAG_E_D))==1)) and not self._INVULNERABILITY):
            self._INVULNERABILITY=True
            self.healthLoss()
        if((self._CurrentLVL==3) and self._BOSSLIFE==0):
            self._ONPLAY,self._MusicProcessPID = False,999999
            self.cancelation()
            self.drawScreen("endScreen")
        self._RDV.append(self._FRAME.after(self._positionCheckTime,self.positionCheck))

    def loadFile(self,filename,ids,tiles):
        f = open(filename,'r',encoding='utf-8')
        lignes  = f.readlines()
        f.close()
        for ligne in lignes:
            res = ligne.split()
            ids.append(res)
            l = [None] * len(res)
            tiles.append(l)

    def screenshot(self):
        if(os.path.exists("screenshots")):
            self._FRAME.postscript(file="screenshots/screenshot_"+time.strftime('%d-%m-%y_%Hh%M',time.localtime())+".eps")
        else:
            os.mkdir("screenshots")
            self._FRAME.postscript(file="screenshots/screenshot_"+time.strftime('%d-%m-%y_%Hh%M',time.localtime())+".eps")

    def drawScreen(self,screenName):
        self._Menu=PhotoImage(file="screens/"+screenName+".gif")
        self._FRAME.create_image(self._WIDTH/2,self._HEIGHT/2, image=self._Menu, tag=("_MENU"))

    def drawMan(self,y):
        self._ME=PhotoImage(file="tiles/_step_"+self._step+"_"+self._condition+"_"+self._direction+".gif")
        self._MAN = self._FRAME.create_image(12*30,(y*30)-15, image = self._ME, tag="_ME")
        if(self._posX>=12):
            for i in range(12,self._posX,1):
                self.move(-30,0)
        else:
            for i in range(self._posX,12,-1):
                self.move(30,0)

    def drawDisplays(self,health,coins,lightnings):
        self._CoinDisplay[0],self._LightningDisplay[0]=PhotoImage(file="tiles/I01.gif"),PhotoImage(file="tiles/I10.gif")
        if(coins<10):
            self._CoinDisplay[1],self._CoinDisplay[2]=PhotoImage(file="tiles/0C0.gif"),PhotoImage(file="tiles/0C"+str(coins)+".gif")
        elif(coins<100):
            D,U=coins/10,coins%10
            self._CoinDisplay[1],self._CoinDisplay[2]=PhotoImage(file="tiles/0C"+str(int(D))+".gif"),PhotoImage(file="tiles/0C"+str(int(U))+".gif")
        if(lightnings<10):
            self._LightningDisplay[1],self._LightningDisplay[2]=PhotoImage(file="tiles/0C0.gif"),PhotoImage(file="tiles/0C"+str(lightnings)+".gif")
        elif(lightnings<100):
            D,U=lightnings/10,lightnings%10
            self._LightningDisplay[1],self._LightningDisplay[2]=PhotoImage(file="tiles/0C"+str(int(D))+".gif"),PhotoImage(file="tiles/0C"+str(int(U))+".gif")
        for i in range(0,health,1):
            self._HealthBar[i]=PhotoImage(file="tiles/I06.gif")
            self._FRAME.create_image(30*i+30,30*1, image=self._HealthBar[i], tag=("_CORE","_HEALTH"+str(i)))
        self._FRAME.create_image(30*7,30*1, image=self._CoinDisplay[0], tag=("_COIN"))
        self._FRAME.create_image(30*11,30*1, image=self._LightningDisplay[0], tag=("_LIGHTNING"))
        for i in range(1,3,1):
            self._FRAME.create_image(30*i+(30*7),30*1, image=self._CoinDisplay[i], tag=("_NUMBER_C_"+str(i)))
            self._FRAME.create_image(30*i+(30*11),30*1, image=self._LightningDisplay[i], tag=("_NUMBER_L_"+str(i)))

    def cancelation(self):
        for i in self._RDV:
            self._FRAME.after_cancel(i)

    def onLeftPress(self,event):
        self.toTheLeft()

    def onRightPress(self,event):
        self.toTheRight()

    def onUpPress(self,event):
        self.jump()

    def onDownPress(self,event):
        self.attack()

    def toTheLeft(self):
        if(not self._Walking and self._ONPLAY):
            self._Walking=True
            self.gravityCheck()
            if(self._direction=="R"):
                   self._direction="L"
            elif((self._MAP[self._posY][self._posX-1] not in self._Border) and (self._MAP[self._posY-1][self._posX-1] not in self._Border)):
                self._posX-=1
                self.move(30,0)
            self.step()

    def toTheRight(self):
        if(not self._Walking and self._ONPLAY):
            self._Walking=True
            self.gravityCheck()
            if(self._direction=="L"):
                self._direction="R"
            elif((self._MAP[self._posY][self._posX+1] not in self._Border) and (self._MAP[self._posY-1][self._posX+1] not in self._Border)):
                self._posX+=1
                self.move(-30,0)    
            self.step()

    def jump(self):
        if(not self._Jumping and self._ONPLAY):
            self.playSound("JumpSound.m4a",False)
            self._Jumping=True
            self.gravityCheck()
            if(self._MAP[self._posY-2][self._posX] not in self._Border):
                self._posY-=1
                self._FRAME.move("_ME",0,-30)
                self.step()

    def attack(self):
        if(not self._Attacking and self._POWER>0 and self._ONPLAY):
            self.playSound("ThrowBallSound.m4a",False)
            self._Attacking,self._PowerBallTile,self._BallposY,self._BallDirection=True,PhotoImage(file="tiles/PWB.gif"),self._posY,self._direction
            self._BallposX = self._posX+1 if(self._BallDirection=="R") else (self._posX-1)
            n = 13 if(self._BallDirection=="R") else 11
            self.step()
            self.ActualisePower(self._POWER-1)
            self._FRAME.create_image(n*30,self._BallposY*30-15, image=self._PowerBallTile, tag=("_POWERBALL"))
            self._FRAME.after(self._propagationTime,self.propagation)

    def step(self):
        self._step="A"
        self._ME=PhotoImage(file="tiles/_step_"+self._step+"_"+self._condition+"_"+self._direction+".gif")
        self._FRAME.itemconfigure(self._MAN,image=self._ME)
        self._FRAME.after(self._stepTime,self.toggle)

    def toggle(self):
        self._step="B"
        self._ME=PhotoImage(file="tiles/_step_"+self._step+"_"+self._condition+"_"+self._direction+".gif")
        self._FRAME.itemconfigure(self._MAN,image=self._ME)
        self._Walking=self._Jumping=False

    def gravity(self):
        if(self._MAP[self._posY+1][self._posX] not in self._Ground):
            self._FRAME.move("_ME",0,+30)
            self._posY+=1
            self._RDV.append(self._FRAME.after(self._gravityTime,self.gravity))

    def gravityCheck(self):
        self._FRAME.after(self._gravityTime,self.gravity)
        if(self._MAP[self._posY][self._posX]==self._MAP[self._posY+1][self._posX]):
            self._RDV.append(self._FRAME.after(self._gravityTime,self.gravity))

    def Animation(self,n,MAX,MIN,TAG,PATH,TIME,tmp):
        tmp=PhotoImage(file=PATH+str(n)+".gif")
        self._FRAME.itemconfigure(TAG,image=tmp)
        n = n+1 if(n<MAX) else MIN
        self._RDV.append(self._FRAME.after(TIME,lambda x = n : self.Animation(x,MAX,MIN,TAG,PATH,TIME,tmp)))

    def gainCoin(self):
        self._nbCoins+=1
        self.playSound("CoinSound.m4a",False)
        if(self._nbCoins<10):
            self._CoinDisplay[1],self._CoinDisplay[2]=PhotoImage(file="tiles/0C0.gif"),PhotoImage(file="tiles/0C"+str(self._nbCoins)+".gif")
        elif(self._nbCoins<100):
            D,U=self._nbCoins/10,self._nbCoins%10
            self._CoinDisplay[1],self._CoinDisplay[2]=PhotoImage(file="tiles/0C"+str(int(D))+".gif"),PhotoImage(file="tiles/0C"+str(int(U))+".gif")
        for i in range(1,3,1):
            self._FRAME.itemconfigure("_NUMBER_C_"+str(i),image=self._CoinDisplay[i])

    def ActualisePower(self,n):
        self._POWER=n
        if(self._POWER<10):
            self._LightningDisplay[1],self._LightningDisplay[2]=PhotoImage(file="tiles/0C0.gif"),PhotoImage(file="tiles/0C"+str(self._POWER)+".gif")
        elif(self._POWER<100):
            D,U=self._POWER/10,self._POWER%10
            self._LightningDisplay[1],self._LightningDisplay[2]=PhotoImage(file="tiles/0C"+str(int(D))+".gif"),PhotoImage(file="tiles/0C"+str(int(U))+".gif")
        for i in range(1,3,1):
            self._FRAME.itemconfigure("_NUMBER_L_"+str(i),image=self._LightningDisplay[i])

    def healthPlus(self):
        self.playSound("HeartSound.m4a",False)
        if(self._HEALTH<5):
            self._HealthBar[self._HEALTH]=PhotoImage(file="tiles/I06.gif")
            self._FRAME.create_image(30*self._HEALTH+30,30*1, image=self._HealthBar[self._HEALTH], tag=("_CORE","_HEALTH"+str(self._HEALTH)))
            self._HEALTH+=1

    def healthLoss(self):
        if(self._HEALTH>0):
            self.playSound("HeartLossSound.m4a",False)
            self._HEALTH-=1
            self._FRAME.delete("_HEALTH"+str(self._HEALTH))
            self._HealthBar[self._HEALTH]=None
            if(self._HEALTH==0):
                self._Alive=False
                self.initialisation(3,0,0,self._CurrentLVL,12,15,self._state,self._condition)
        self._FRAME.after(self._invulnerabilityTime,self.leaveInvulnerability)

    def leaveInvulnerability(self):
        self._INVULNERABILITY=False

if __name__ == '__main__':
    Application().mainloop()
