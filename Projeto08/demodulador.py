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

    # yModulado = [(1 + yFiltrado[i])*c(i/len(yFiltrado)) for i in range(len(yFiltrado))]
    yModulado, samplerate = sf.read('modulado.wav')
    yModuladoCerto, samplerate = sf.read('moduladocerto.wav')

    xfModulado, yfModulado = calcFFT(yModulado, samplerate)
    xfModuladoCerto, yfModuladoCerto = calcFFT(yModuladoCerto, samplerate)

    t = np.linspace(0, duracao, duracao*samplerate)

    yDemodulado = [yModulado[i]*cc(t[i]) for i in range(len(yModulado))]

    yFiltrado = [yDemodulado[0], yDemodulado[1]]
    a = 0.1121
    b = 0.07663
    c = 1   
    d = -1.131
    e = 0.3199
    for i in range(2, len(yModulado)):
        yFiltrado.append(-d*yFiltrado[i-1] - e*yFiltrado[i-2] + a*yDemodulado[i-1] + b*yDemodulado[i-2])

    yDemoduladoCerto = [yModuladoCerto[i]*cc(t[i]) for i in range(len(yModulado))]

    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = kaiserord(ripple_db, width)
    cutoff_hz = 4000.0
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    yFiltradoCerto = lfilter(taps, 1.0, yDemoduladoCerto)

    xf, yf = calcFFT(yFiltrado, samplerate)
    xfCerto, yfCerto = calcFFT(yFiltradoCerto, samplerate)

    play = True

    if play:
        print("Emitindo o som demodulado")
        sd.play(yDemodulado, samplerate)
        sd.wait()

        print("Emitindo o som filtrado")
        sd.play(yFiltrado, samplerate)
        sd.wait()

        print("Emitindo o som modulado certo")
        sd.play(yDemoduladoCerto, samplerate)
        sd.wait()
        
        print("Emitindo o som filtrado certo")
        sd.play(yFiltradoCerto, samplerate)
        sd.wait()

    show = True

    if show:
        plt.figure("Fourier")
        plt.title("Fourier")
        plt.plot(xf, np.abs(yf))

        plt.figure("Fourier certo")
        plt.title("Fourier certo")
        plt.plot(xfCerto, np.abs(yfCerto))

        plt.figure("Fourier modulado")
        plt.title("Fourier modulado")
        plt.plot(xfModulado, np.abs(yfModulado))

        plt.figure("Fourier modulado certo")
        plt.title("Fourier modulado certo")
        plt.plot(xfModuladoCerto, np.abs(yfModuladoCerto))

    

        
    
    plt.show()

if __name__ == "__main__":
    main()