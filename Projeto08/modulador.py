#importe as bibliotecas
# https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import kaiserord, lfilter, firwin, freqz
from scipy.fftpack import fft, fftshift
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show
import sys

def cc(t):
    fc = 14000
    C = 1
    return C*np.sin(2*np.pi*fc*t)

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def calcFFT(signal, samplerate):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    #y  = np.append(signal, np.zeros(len(signal)*samplerate))
    N  = len(signal)
    T  = 1/samplerate
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

    yAudio, samplerate = sf.read('output.wav')

    print(len(yAudio))
    print(yAudio)

    # yAudio = yAudio[:,0]

    print(samplerate)

    maxAudio = abs(max(yAudio))
    minAudio = abs(min(yAudio))

    if minAudio > maxAudio:
        yAudioNormalizado = yAudio/minAudio
    else:
        yAudioNormalizado = yAudio/maxAudio

    yFiltrado = [yAudioNormalizado[0], yAudioNormalizado[1]]
    # Feito com frequencia de corte igual a 1200
    a = 0.01305
    b = 0.01165
    c = 1   
    d = -1.686
    e = 0.7104
    for i in range(2, len(yAudioNormalizado)):
        yFiltrado.append(-d*yFiltrado[i-1] - e*yFiltrado[i-2] + a*yAudioNormalizado[i-1] + b*yAudioNormalizado[i-2])

    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = kaiserord(ripple_db, width)
    cutoff_hz = 4000.0
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    yFiltradoCerto = lfilter(taps, 1.0, yAudioNormalizado)

    t = np.linspace(0, len(yAudio)/samplerate, len(yAudio))

    yModulado = [(yFiltrado[i])*cc(t[i]) for i in range(len(yFiltrado))]
    yModuladoCerto = [(yFiltradoCerto[i])*cc(t[i]) for i in range(len(yFiltrado))]

    play = True

    if play:
        print("Emitindo o som")
        sd.play(yAudio, samplerate)
        sd.wait()

        print("Emitindo o som filtrado")
        sd.play(yFiltrado, samplerate)
        sd.wait()

        print("Emitindo o som modulado")
        sd.play(yModulado, samplerate)
        sd.wait()

    filename = "modulado.wav"
    sf.write(filename, yModulado, samplerate)

    filename = "moduladocerto.wav"
    sf.write(filename, yModuladoCerto, samplerate)

    xfAudioNormalizado, yfAudioNormalizado = calcFFT(yAudioNormalizado, samplerate)
    xfAudioFiltrado, yfAudioFiltrado = calcFFT(yFiltrado, samplerate)
    xfAudioFiltradoCerto, yfAudioFiltradoCerto = calcFFT(yFiltradoCerto, samplerate)

    show = True

    if show:
        # Exibe gráficos
        # plt.figure('audio')
        # plt.plot(t, yAudio)

        # plt.figure('filtrado')
        # plt.plot(t, yFiltrado)

        # plt.figure('filtrado certo')
        # plt.plot(t, yFiltradoCerto)

        plt.figure('normalizado')
        plt.plot(t, yAudioNormalizado)

        plt.figure('modulado')
        plt.plot(t, yModulado)

        plt.figure('modulado certo')
        plt.plot(t, yModuladoCerto)
        
        plt.figure('fourier normalizado')
        xlim(0,10000)
        plt.plot(xfAudioNormalizado, np.abs(yfAudioNormalizado))

        plt.figure('fourier filtrado')
        xlim(0,10000)
        plt.plot(xfAudioFiltrado, np.abs(yfAudioFiltrado))

        plt.figure('fourier filtrado certo')
        xlim(0,10000)
        plt.plot(xfAudioFiltradoCerto, np.abs(yfAudioFiltradoCerto))

        plt.show()

if __name__ == "__main__":
    main()