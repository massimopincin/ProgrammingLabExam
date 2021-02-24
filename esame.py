class ExamException(Exception):
        pass

class CSVTimeSeriesFile():
    def __init__(self,name):
        self.name=name
    def get_data(self):
        data=[] #lista che ritorno
        current=0 #per controllare se l'epoch sia maggiore del precedente
        try: 
            myfile=open(self.name,"r")
        except:
            raise ExamException("Impossibile aprire il file!")
        for i in myfile:
            elements=i.split(",")
            try: 
                float(elements[1]) #controllo se il valore di temp. è un numero
            except:
                continue
            if elements[0]!="epoch" and float(elements[1])!=0:
                try:
                    float(elements[0])  #controllo se il valore epoch è un numero
                except:
                    continue
                if float(elements[0])<=current: #controllo se l'epoch letto è maggiore del precedente
                        raise ExamException("Errore nella lista degli epoch!")
                elements[1]=float(elements[1]) #conversione da string a float
                if "." in elements[0]:
                    elements[0]=int(round(float(elements[0]))) #se l'epoch è un float, lo arrotondo
                else:
                    elements[0]=int(elements[0]) #conversione da string a int
                data.append(elements)
                current=elements[0]        
        myfile.close()
        return data

def hourly_trend_changes(series):
    epoch=[]
    values=[]
    crescenza=[]
    inversioni=[]
    hours=[]
    unique=[]
    nfinale=[]
    
    for i in series:
        epoch.append(i[0])
        values.append(i[1])
    for i in range(1,len(values)): #parte dalla posizione 1, non 0 siccome devo considerare l'elemento precedente
        if values[i]>values[i-1]: 
            crescenza.append(1) #se al punto i la serie cresce, assegno 1
        elif values[i]==values[i-1]:
            crescenza.append(0) #se è costante, assegno 0
        else:
            crescenza.append(-1) #se decresce, assegno -1

    cycle=crescenza[0] #per portarsi dietro 1 o -1 in modo da vedere quando la crescenza cambia

    inversioni.append(0) #assegno 0 al primo elemento per semplicità di lavoro con le lunghezze degli array 

    for i in range(0,len(crescenza)):
        if crescenza[i]==0:     #se la crescenza non cambia, assegno 0
            inversioni.append(0)
        elif crescenza[i]==cycle:
            inversioni.append(0)
        else:
            inversioni.append(1)      #se la crescenza cambia, assegno 1
            cycle=crescenza[i]

    for i in epoch:
        hours.append(int(i/3600))     #formo una lista di ore 

    for i in hours:
        if i not in unique:
            unique.append(i)              #rimuovo i duplicati dalla lista di ore

    for i in range(0,len(unique)):
        nfinale.append(0)                  #formo una lista dove salvare il numero di inversioni per ogni ora

    for i in range(0,len(inversioni)): 
        if inversioni[i]==1:               #se c'è un'inversione...
            for j in range(0,len(unique)):
                if hours[i]==unique[j]:    #...controllo a che ora appartiene
                    nfinale[j]+=1          #aggiungo l'inversione alla rispettiva ora
    return nfinale

time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
hourly_trend_changes(time_series)