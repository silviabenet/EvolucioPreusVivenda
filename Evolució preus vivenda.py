#!/usr/bin/env python
# coding: utf-8

# ## Web scraping

# In[4]:


import bs4 as bs
import urllib
import urllib.request
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import urllib.robotparser

# In[5]:


HTML = "https://www.trovimap.com/precio-vivienda/barcelona"


# In[6]:


# Amb .read_html() podem obtenir fàcilment la taula que ens mostra la web.

df = pd.read_html(HTML)
df[0].head()


# In[7]:


# Amb BeautifulSoup, podrem obtenir tot el String del codi HTML per si volem obtenir més informació.

historypage = urllib.request.urlopen(HTML)
soup = bs.BeautifulSoup(historypage,'html.parser')
makeitastring = ''.join(map(str, soup))

#soup
#makeitastring


# In[8]:



#retorna un llistat de ciutats i la seva variació de preu segons el html ja llegit per BeatifulSoup que li hem passat. Aquest html està format segons 
# la provincia. Per exemple: HTML = "https://www.trovimap.com/precio-vivienda/barcelona" retornarà un llistat amb les
# ciutats que es troben en aquesta pàgina que son les ciutats de Barcelona i les seves variacions de preus mensual, els últims 3 mesos
# anual i preu euro/ metre quadrat.

#def obtenirCiutatsiVariacio(htmlSoup):
#    tableProv = soup.find('table', {'class':'table table-condensed precio-medio-table'})

#    tbody = tableProv.find('tbody')

#    llistaVarCiutats=[]
#    for row in tbody.findAll("tr"):
#        cells = row.findAll('td')    
#        link = cells[0].find('a')
#        ciutat = link.find(text=True)
#        #print(ciutat)
#        varMensual = cells[1].find(text=True)
#        var3mesos = cells[2].find(text=True)
#        varAnual = cells[3].find(text=True)
#        eumetre = cells[4].find(text=True)
#        element=[ciutat,varMensual,var3mesos,varAnual,eumetre]
#        llistaVarCiutats.append(element)
        
        
 #   return llistaVarCiutats




def generarCSV(taula,nomFitxer):
    
    taula.to_csv(nomFitxer + '.csv', header=True, index = False)
    
#df_numeros.to_csv('numeros.csv', header=False, index=False)



#HTML = "https://www.trovimap.com/precio-vivienda/barcelona"

#VarCiutat = obtenirCiutatsiVariacio(soup)

#print(VarCiutat[0])


# In[ ]:





# In[ ]:





# In[9]:


HTML = "https://www.trovimap.com/precio-vivienda/"

# mirem a robots.txt per veure si hi ha pàgines bloquejades a robots

rp = urllib.robotparser.RobotFileParser()
rp.set_url('https://www.trovimap.com/robots.txt')
rp.read()
user_agent= '*'


# In[10]:

pais = "espana"

HTMLEspana = HTML + pais

# Comprovem si està definit a reobots.txt que ens deixa fer web scrapping d'aquesta url

if rp.can_fetch(user_agent, HTMLEspana):
    
    df = pd.read_html(HTMLEspana)
    dfProvinciesEspana = df[0]
    dfProvinciesEspana = dfProvinciesEspana.rename(columns={"Unnamed: 0": 'Provincies'})

    dfProvinciesEspana.head()


# ### Obtenim una taula amb la variació menusal de cada provincia de l'estat.

# ### Si volem obtenir una taula, tenint per files les ciutats més importants de cada provincia tal com hem fet anteriorment amb la de Barcelona:

# In[11]:


    dfProvinciesEspana.iloc[0]['Provincies']
else :
    print ("Pàgina bloquejada per robots,txt: " + HTMLEspana)

# ### Si volem obtenir una taula, tenint per files les ciutats més importants de Catalunta:

# In[12]:

    
# Agafar la taula per cada una de les quatre provincies de Catalunya.
    dfBarcelona = pd.read_html(HTML+"barcelona")
    dfTarragona = pd.read_html(HTML+"tarragona")
    dfGirona = pd.read_html(HTML+"girona")
    dfLleida = pd.read_html(HTML+"lleida")
    dfBarcelona = dfBarcelona[0]
    dfTarragona = dfTarragona[0]
    dfGirona = dfGirona[0]
    dfLleida = dfLleida[0]

# Concatenar Taules.
    dfCatalunya = pd.concat([dfBarcelona, dfTarragona], ignore_index=True)
    dfCatalunya = pd.concat([dfCatalunya, dfGirona], ignore_index=True)
    dfCatalunya = pd.concat([dfCatalunya, dfLleida], ignore_index=True)

# Renombrar columnes.
    dfCatalunya = dfCatalunya.rename(columns={"Unnamed: 0": 'Ciutat', "Variación Mensual": 'Variació mensual',
                                          "Variación 3 meses": 'Variació tres messos', "Variación anual": 'Variació anual'})

    dfCatalunya.tail()


# -------

# ### Ara volem treure totes les ciutats importants de España. Per fer això necesitem totes les url de cada provincia  a partir de el html.

# In[43]:


historypage = urllib.request.urlopen(HTMLEspana)
soup = bs.BeautifulSoup(historypage,'html.parser')
makeitastring = ''.join(map(str, soup))
#soup
#makeitastring

# Buscar el patró dins del html on es guarda els noms de les provincies per despres buscar-les en url. 
capitals = '/'.join(map(str, re.findall("precio-vivienda(.+?)\">",makeitastring)))
capitals = capitals[46:570]
#print(capitals)

# Ja tenim un array amb tots els noms de les provincies que haurem de posar a la url.
capitalsArray = capitals.split('//')
capitalsArray


# In[48]:


HTML = "https://www.trovimap.com/precio-vivienda/"
HTMLCapitals = HTML + capitalsArray[25]


    
df = pd.read_html(HTML + capitalsArray[25])
df[0].head()


# In[64]:


# Veiem que serveix, ara només hem de posar-lo en un loop per obtenir totes les ciutats importants d'España.
dfEspana = pd.DataFrame()
for capital in capitalsArray:
    if capital != "ceuta" and capital != "soria":
        # Per a cada url agafar la taula
        if rp.can_fetch(user_agent, HTML+capital):
            
            dfAux = pd.read_html(HTML+capital)
            dfAux = dfAux[0]
            #Anar concatenant ciutats
            dfEspana = pd.concat([dfEspana, dfAux], ignore_index=True)
            print(capital)
        else: 
            print ("Pàgina bloquejada per robots,txt: " + HTML+capital)
    
# Renombrar columnes.
dfEspana = dfEspana.rename(columns={"Unnamed: 0": 'Ciutat', "Variación Mensual": 'Variació mensual',
                                "Variación 3 meses": 'Variació tres messos', "Variación anual": 'Variació anual'})
    
dfEspana.tail()


# ### Ja tenim taules amb les variacions econòmiques de les ciutats més importants tant de Catalunya com d'España.

# gravem a fixter csv totes les poblacions d'espanya amb les seves variacions de preu

generarCSV (dfEspana,pais)

# gravem també un altre csv amb les variacions generals de cada província d'espanya

generarCSV(dfProvinciesEspana,'Provincies')



# ---------
