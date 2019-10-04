import numpy as np
import scipy as sp
from scipy import stats

def Analisis():
     
    λ = 5/10 #Entradas 
    λs = 6/10 #Salidas
    a_i = [] #Llegas
    s_i = [] #Servicios
    data = 0.0 #Acumulador

    #Se generan los valores aleatorios hasta que el ciclo culmine
    while (data<=480):


        data2 = sp.stats.expon(scale = 1/ λs).rvs() #RVS (genera variables aleatoria por cada iteración)
        data += sp.stats.expon(scale = 1/ λ).rvs() #Acumuladora para determinar el rompimiento del while
        a_i.append(data) #Valores para la lista de llegadas
        s_i.append(data2) #Valores para la lista de servicios
    
    #Retornamos las listas para operarlas adelante
    return a_i, s_i
    
#Nuestro servidor de cola única     
def SSS(a_i,s_i):

    i = 0 #jobs
    di = [] #delay time
    Ci = []
    Co = 0.0 #Salida inicial

    n = len(a_i) #Tamaño de la lista generada
    while (i<n):
    
        if (a_i[i] < Co):
            aux = Co-a_i[i]
            di.append(aux)

        else:
            aux = 0.0
            di.append(aux)

        Ci.append(a_i[i]+di[i]+s_i[i])
        Co = Ci[i]

        i = i+1
    return di, Co

#Calculamos los intervalos de confianza
def confidence_interval(datos, confidence = 0.95):


    a = 1*np.array(datos)
    n = len (a)
    m, se = np.mean(a), sp.stats.sem(a)
    h = se* sp.stats.t._ppf((1+confidence)/2., n-1)

    #Guardamos la media, el valor inicial y de ultimo el final
    return m, m-h, m+h

#Aqui usamos nuestras funciones
if __name__ == '__main__':

    #Replicas para los estadisiticos de trabajo
    av_a_ai = []
    av_di = []
    av_si = []
    av_w = []
    av_a_rate = []
    av_s_rate = []

    #Replicas para los estadisiticos de tiempo
    q = []
    x = []
    l = []

    #Inicializar las replicas para hacerlo 1000 veces
    for i in range (1000):

        a_i, s_i = Analisis() #Usamos los valores de la funcion analisis    
        job = len(a_i) #Tomamos el tamaño de nuestras listas
        di,Co = SSS(a_i,s_i) #De la funcion SSS retornamos los valores de di Co

        #Hacemos las operaciones y vamos guardando en las listas
        av_a_ai.append((a_i[job-1])/job)
        av_di.append(sum(di)/job)
        av_si.append(sum(s_i)/job)
        av_w.append((av_si[i]+av_di[i]))

        av_a_rate.append(1/av_a_ai[i])
        av_s_rate.append(1/av_si[i])

        q.append((job/Co)*av_di[i])
        x.append((job/Co)*av_si[i])
        l.append(q[i]+x[i])
        
        #Cantidad de trabajos procesados
        procces = len (a_i)

    #Impresion de datos
    print ("\n\t\t\t***WORK STATISTICAL AVERAGES***\n")

    print("The statistical values are given in a list of 3 [mean, initial, final]\n")

    print("Average interarrival: {0}\nAverage Delay: {1}\nAverage service time: {2}".format(confidence_interval(av_a_ai),confidence_interval(av_di),confidence_interval(av_si)))
    print("Wait in node:{0}\nArrival rate {1}\nService Rate: {2}\nJobs Served: {3}".format(confidence_interval(av_w),confidence_interval(av_a_rate),confidence_interval(av_s_rate),confidence_interval(a_i)))

    print ("\n\t\t\t***TIME STATISTICAL AVERAGES***\n")
    print("Number of jobs in the queue: {0}\nNumber of jobs in service: {1}\nNumber of jobs in the service node: {2}".format(confidence_interval(q),confidence_interval(x),confidence_interval(l)))

    print ("\n")