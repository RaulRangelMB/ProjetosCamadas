#importe as bibliotecas
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import kaiserord, lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
from scipy.fftpack import fft, fftshift
import sys

def cc(t):
    fc = 14000
    C = 1
    return C*np.sin(2*np.pi*fc*t)

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    #y  = np.append(signal, np.zeros(len(signal)*fs))
    N  = len(signal)
    T  = 1/fs
    xf = np.linspace(-1.0/(2.0*T), 1.0/(2.0*T), N)
    yf = fft(signal)
    return(xf, fftshift(yf))

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando")
    
    duracao = 5 #tempo do som em segundos
    fs = 44100 # taxa de amostragem
    A = 1  #Amplitude do sinal

    t = np.linspace(0, duracao, duracao*fs)

    # yModulado = [(1 + yFiltrado[i])*c(i/len(yFiltrado)) for i in range(len(yFiltrado))]
    yModulado, samplerate = sf.read('modulado.wav')

    yFiltrado = [yModulado[0], yModulado[1]]
    a = 0.1121
    b = 0.07663
    c = 1   
    d = -1.131
    e = 0.3199
    for i in range(2, len(yModulado)):
        yFiltrado.append(-d*yFiltrado[i-1] - e*yFiltrado[i-2] + a*yModulado[i-1] + b*yModulado[i-2])

    yModuladoXportadora = [yFiltrado[i]*cc(t[i]) for i in range(len(yModulado))]

    print(len(yModuladoXportadora))

    xf, yf = calcFFT(yModuladoXportadora, fs)

    plt.figure("Fourier")
    plt.title("Fourier")
    plt.plot(xf, np.abs(yf))

    index = peakutils.indexes(np.abs(yf), thres=0.4, min_dist=20)
    print("index de picos {}" .format(index)) #yf é o resultado da transformada de fourier

    #printe os picos encontrados! 
    # Aqui você deverá tomar o seguinte cuidado: A funcao  peakutils.indexes retorna as POSICOES dos picos. Não os valores das frequências onde ocorrem! Pense a respeito
    
    for freq in xf[index]:
        print(f'Pico encontrado em {freq} hz')
    
    # plt.figure("wves")
    
    # plt.plot(t, s2)

    # Exibe gráficos
    
    # nyq_rate = samplerate/2
    # width = 5.0/nyq_rate
    # ripple_db = 60.0 #dB
    # N , beta = kaiserord(ripple_db, width)
    # cutoff_hz = 4000.0
    # taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    # yFiltrado = lfilter(taps, 1.0, yModulado)
    
    # plt.title("Ondas somadas no tempo")
    # plt.xlabel("tempo (s)")
    # plt.xlim([0, 0.01])
    
    # signalMeu().plotFFT(sinal, fs)

    play = False

    if play:
        # print("Emitindo o som filtrado")
        # sd.play(yFiltrado, fs)
        # sd.wait()

        print("Emitindo o som modulado")
        sd.play(yModulado, fs)
        sd.wait()
    
    plt.show()

if __name__ == "__main__":
    main()