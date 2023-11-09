#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from scipy.fftpack import fft, fftshift
import sys

dic_freq = {'1':[1209, 697], '2':[1336, 697], '3':[1477, 697], 'A':[1633, 697], 
            '4':[1209, 770], '5':[1336, 770], '6':[1477, 770], 'B':[1633, 770], 
            '7':[1209, 852], '8':[1336, 852], '9':[1477, 852], 'C':[1633, 852], 
            'X':[1209, 941], '0':[1336, 941], '#':[1477, 941], 'D':[1633, 941]}

def encontraPossiveis(freqs, delta = 7):
    possiveis_1 = []
    possiveis_2 = []
    freqs_1 = []
    freqs_2 = []
    final = []
    for i in range(len(freqs)):
        if freqs[i] > 650 and freqs[i] < 1000:
            freqs_1.append(freqs[i])
        elif freqs[i] > 1150 and freqs[i] < 1680:
            freqs_2.append(freqs[i])

    for freq in freqs_1:
        if 697 - delta < freq < 697 + delta:
            possiveis_1.extend(['1','2','3','A'])
        elif 770 - delta < freq < 770 + delta:
            possiveis_1.extend(['4','5','6','B'])
        elif 852 - delta < freq < 852 + delta:
            possiveis_1.extend(['7','8','9','C'])
        elif 941 - delta < freq < 941 + delta:
            possiveis_1.extend(['X','0','#','D'])

    for freq in freqs_2:
        if 1209 - delta < freq < 1209 + delta:
            possiveis_2.extend(['1','4','7','X'])
        elif 1336 - delta < freq < 1336 + delta:
            possiveis_2.extend(['2','5','8','0'])
        elif 1477 - delta < freq < 1477 + delta:
            possiveis_2.extend(['3','6','9','#'])
        elif 1633 - delta < freq < 1633 + delta:
            possiveis_2.extend(['A','B','C','D'])
            
    for possivel in possiveis_1:
        if possivel in possiveis_2:
            final.append(possivel)

    print(possiveis_1)
    print(possiveis_2)

    return final
    

#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    #y  = np.append(signal, np.zeros(len(signal)*fs))
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))

def main():

    #*****************************instruções********************************
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100 #taxa de amostragem
    fs = 44100
    sd.default.channels = 1 #numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    duration = 2 # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = sd.default.samplerate * duration
    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("A gravação começará em")
    # time.sleep(1)
    # print("3")
    # time.sleep(1)
    # print("2")
    # time.sleep(1)
    # print("1")
    # time.sleep(1)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada

    print("Começou")

    #para gravar, utilize
    audio = sd.rec(int(numAmostras))
    sd.wait()
    print("...     ACABOU")


    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 

    y = audio
    # print(type(audio))
    # print(audio)
    # print(audio.shape)
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!

    t = np.linspace(0, duration, numAmostras)
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas).

    y = [valor for [valor] in y]

    # plt.figure("Audio")
    # plt.title("Audio")
    # plt.plot(audio)
    
    plt.figure("Audio tempo")
    plt.title("Audio")
    plt.plot(t, y)
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = calcFFT(y, fs)
    plt.figure("Fourier")
    plt.title("Fourier")
    plt.plot(xf, np.abs(yf))
    plt.xlim(0,7000)

    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:
    index = peakutils.indexes(np.abs(yf), thres=0.4, min_dist=20)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    for freq in xf[index]:
        print(f'Pico encontrado em {freq} hz')

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

    print(encontraPossiveis(xf[index]))
      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
