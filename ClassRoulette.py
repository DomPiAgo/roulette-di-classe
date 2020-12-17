# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 23:06:08 2020

@author: ago
"""
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
        
        self.lposta=[]
        self.lbilancio=[]
        self.lvinti=[]
        
        self.rosso={1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
        self.nero={2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}
        self.zero={0}
        
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
        spin= random.randint(0,36)
        return bool(spin in self.rosso)
    
    
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
            print ("Lascia non hai piu abbastanza",sequenza, bilancio)
            return self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        self.nlanci+=1
    
        print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " dovuto alla sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio+posta)         
            return self.lposta,self.lvinti,self.lbilancio
        else:
            print ("perso")
            self.lvinti.append(vinto)
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[2*posta], bilancio-posta)          
            return self.lposta,self.lvinti,self.lbilancio
        
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
            print ("Lascia non hai piu abbastanza",sequenza, bilancio)
            return self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        self.nlanci+=1
    
        print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " dovuto alla sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[2*posta], bilancio+posta)         
            return self.lposta,self.lvinti,self.lbilancio
        else:
            print ("perso")
            self.lvinti.append(vinto)
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio-posta)          
            return self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)
    
class Dalembert(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nPIU O MENO\n')
    
    def get_giocata(self,sequenza, bilancio):
               
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[-1]    
        
        if posta==0:
            print('La posta e zero',sequenza,bilancio)
            return self.lposta,self.lvinti,self.lbilancio
        
        if posta > bilancio:
            print ("Lascia non hai piu abbastanza",sequenza, bilancio)
            return self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        self.nlanci+=1
    
        print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " dovuto alla sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta-1], bilancio+posta)         
            return self.lposta,self.lvinti,self.lbilancio
        else:
            print ("perso")
            self.lvinti.append(vinto)
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta+1], bilancio-posta)          
            return self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio) 
    
    
class Labouchere(Strategia):
    def __init__(self,sequenza,bilancio):
        super().__init__(sequenza,bilancio)
    
        print('\nCANCELLA LA VINCITA\n')
     
    def get_giocata(self,sequenza, bilancio):
   
        if len(sequenza) < 1:
            print("Lascia perche la sequenza e vuota",sequenza,bilancio)   
            return self.lposta,self.lvinti,self.lbilancio
       
        if len(sequenza) == 1:
            posta = sequenza[0]
        else:
            posta = sequenza[0] + sequenza[-1]    
      
        if posta > bilancio:
            print ("Lascia non hai piu abbastanza",sequenza, bilancio)
            return self.lposta,self.lvinti,self.lbilancio
       
        vinto = self.ruota()
        self.nlanci+=1
    
        print ("Scommetti " + str(posta) + " con un bilancio di " + str(bilancio) + " dovuto alla sequenza " + str(sequenza))
       
        self.lposta.append(posta)
        self.lbilancio.append(bilancio)
        
        if vinto:
            print ("vinto")
            self.lvinti.append(vinto)
            self.nvinti+=1
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza[1:-1], bilancio+posta)         
            return self.lposta,self.lvinti,self.lbilancio
        else:
            print ("perso")
            self.lvinti.append(vinto)
            self.lposta,self.lvinti,self.lbilancio = self.get_giocata(sequenza+[posta], bilancio-posta)          
            return self.lposta,self.lvinti,self.lbilancio
        
    def get_gioco(self):
        return self.get_giocata(self.sequenza,self.bilancio)


diz_strategie={0:Martingala,1:Paroli,2:Dalembert,3:Labouchere}

for i in range(4):
    print('\nTest strategie\n')
    s=diz_strategie[i]([1],10)
    if i==3: 
        lposta,lvinti,lbilancio=s.get_giocata([1,2,3],100)
    else:
        lposta,lvinti,lbilancio=s.get_giocata([1],10)
        
    s.get_percvinti()   
    #print('\lposta,lvinti,lbilancio,nposte,vinti,bilancio', lposta,lvinti,lbilancio,poste,vinti,bilancio)  
    df = pd.DataFrame({'Vincita':lvinti,'Posta': lposta,'Bilancio': lbilancio,})
    
    print('-----------------------------------------------')
    print(df)
    print('-----------------------------------------------')
    print('\n+++++++++++++++++++++++++++++++++++++++++++++++')
    dfg=pd.DataFrame({'Posta': lposta,'Bilancio': lbilancio})
    dfg.plot.line()
    print('\n+++++++++++++++++++++++++++++++++++++++++++++++')