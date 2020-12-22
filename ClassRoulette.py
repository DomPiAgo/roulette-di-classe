
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:33:10 2020

@author: ago
"""
import numpy as np
import random
import pandas as pd
import math

class Strategia:

    def __init__(self,sequenza,bilancio):
        self.sequenza = sequenza
        self.bilancio = bilancio     
        self.nlanci=0
        self.nvinti=0
        
        self.lspin=[]
        self.lposta=[]
        self.lbilancio=[]
        self.lvinti=[]
        
        self.rosso={1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
        self.nero={2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
        self.pari={2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36}
        self.dispari={1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35}
        self.basso={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18}
        self.alto={19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36}
        self.zero={0}
        
        # random.seed(9)
        
    def get_sequenza(self):
        return self.sequenza

    def set_sequenza(self, sequenza):
        self.sequenza = sequenza
    
    def get_bilancio(self):
        return self.bilancio
    
    def set_bilancio(self, bilancio):
        self.bilancio = bilancio
        
    def get_percvinti(self):
        percentuale_vinti=self.nvinti/self.nlanci
        print()
        print("Lanci " + str(self.nlanci) + ", vinti " + str(self.nvinti) + "! Percentuale vincite " + str("{:.2%}".format(percentuale_vinti)))
        return
    
    def ruota(self):
        spin=random.randint(0,36)
        self.nlanci+=1
        self.lspin.append(spin)
        return bool(spin in self.rosso)
        
    def szaurea(self,posta):
            y=1.6180*posta
            return np.round(y,0)


class Nessuna(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nLA DEA FORTUNA\n')
    
    def get_giocata(self,sequenza, bilancio):
               
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[-1]    
      
        if posta > bilancio:
            # print ("Lascia non hai più abbastanza",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio+posta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio-posta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)

    
class Aurum(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nSTRATEGIA AUREA\n')
    
    def get_giocata(self,sequenza, bilancio):
               
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[-1]    
      
        if posta > bilancio:
            print ("Lascia non hai più abbastanza",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio+posta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            y=self.szaurea(posta)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[y], bilancio-posta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)


class Martingala(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nLASCIA O RADDOPPIA\n')
    
    def get_giocata(self,sequenza, bilancio):
               
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[-1]    
      
        if posta > bilancio:
            print ("Lascia non hai più abbastanza",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio+posta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[2*posta], bilancio-posta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)
    
    
class Paroli(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nRADDOPPIA o LASCIA\n')
    
    def get_giocata(self,sequenza, bilancio):
               
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[-1]    
      
        if posta > bilancio:
            print ("Lascia non hai più abbastanza",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[2*posta], bilancio+posta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio-posta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)
    
class Dalembert(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\npiù O MENO\n')
    
    def get_giocata(self,sequenza, bilancio):
               
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[-1]    
        
        if posta==0:
            print('La posta e zero',sequenza,bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
        if posta > bilancio:
            print ("Lascia non hai più abbastanza fondi",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta-1], bilancio+posta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta+1], bilancio-posta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio) 
    
    
class Labouchere(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nCANCELLA LA VINCITA\n')
     
    def get_giocata(self,sequenza, bilancio):
   
        if len(sequenza) < 1:
            print("Lascia perchè la sequenza è vuota",sequenza,bilancio)   
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[0] + sequenza[-1]    
      
        if posta > bilancio:
            print ("Lascia non hai più abbastanza",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza[1:-1], bilancio+posta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio-posta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)

class Fibonacci(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
        self.fb=1
        self.sequenza=[1]         
        print('\nDUE PASSI INDIETRO, UNO AVANTI\n')
    
    def fibonacci(self, n):
        if n == 1 or n == 2:
            return 1
        else:
            return self.fibonacci(n-1) + self.fibonacci(n-2)
    
    def get_giocata(self,sequenza, bilancio):
        
        if self.nlanci == 100:
            print('Lanci = 100')
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
        if len(sequenza) == 1:
          vecchiaposta = sequenza[0]
        else:
            vecchiaposta= self.fibonacci(self.fb)  
        
        if vecchiaposta > bilancio:
            print ("Lascia non hai più abbastanza fondi",sequenza, bilancio)
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        
    
        #print ("Scommetti " + str(vecchiaposta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(sequenza))
       
        self.lposta.append(vecchiaposta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            #print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.fb=max(self.fb-2,1)
            nuovaposta=self.fibonacci(self.fb)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[nuovaposta], bilancio+vecchiaposta)         
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        else:
            #print ("Perso")
            self.lvinti.append(vinto)
            self.fb+=1
            nuovaposta=self.fibonacci(self.fb)
            self.lspin,self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[nuovaposta], bilancio-vecchiaposta)          
            return self.lspin, self.lposta,self.lvinti,self.lbilancio
        
    def get_giocataF(self,sequenza,bilancio):
        #self.lposta=[]
        while bilancio > 0:
            self.posta = self.fibonacci(self.fb)
            if self.nlanci ==10:
                print('Lanci = 10')
                return self.lspin, self.lposta,self.lvinti,self.lbilancio
            if self.posta > bilancio:
                print("Non hai più abbastanza fondi") 
                return self.lspin, self.lposta,self.lvinti,self.lbilancio
            
            #print ("Scommetti " + str(self.posta) + " con un bilancio di " + str(bilancio) + " e la sequenza " + str(self.lposta))
            
            vinto=self.ruota()
            
            if vinto:
                #print ("vinto")
                self.lvinti.append(vinto)
                self.nvinti+=1
                self.fb=max(self.fb-2,1)
                bilancio += self.posta
            else:
                #print ("Perso")
                self.lvinti.append(vinto)
                bilancio -= self.posta
                self.fb += 1
            self.lposta.append(self.posta)
            self.lbilancio.append(bilancio)
        return self.lspin, self.lposta,self.lvinti,self.lbilancio
            
diz_strategie={0:Martingala,1:Paroli,2:Dalembert,3:Labouchere,4:Fibonacci,5:Aurum,6:Nessuna}


for i in range(7):
    print('\nTest strategie\n')
    s=diz_strategie[i]([1],100)
    if i==2: 
        lspin,lposta,lvinti,lbilancio=s.get_giocata([3],100)
    elif i==3: 
        lspin,lposta,lvinti,lbilancio=s.get_giocata([1,2,3],100)
    elif i==4:
        lspin,lposta,lvinti,lbilancio=s.get_giocata([1],100)
    else:
         lspin,lposta,lvinti,lbilancio=s.get_giocata([1],100)
    s.get_percvinti() 
    
    df = pd.DataFrame({'Numero':
     lspin,'Vincita':lvinti,'Posta': lposta,'Bilancio': lbilancio})
        
    print('-----------------------------------------------')
    print(df)
    print('-----------------------------------------------')
    print('\n+++++++++++++++++++++++++++++++++++++++++++++++')
    dfg=pd.DataFrame({'Posta': lposta,'Bilancio': lbilancio})
    dfg.plot.line()
    print('\n+++++++++++++++++++++++++++++++++++++++++++++++')
