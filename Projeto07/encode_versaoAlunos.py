#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)



def main():
    
   
    #***************instruções**************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")
    print("Aguardando usuário")
    num = ''
    dic_freq = {'1':[1209, 697], '2':[1336, 697], '3':[1477, 697], 'A':[1633, 697], '4':[1209, 770], '5':[1336, 770], '6':[1477, 770], 'B':[1633, 770], '7':[1209, 852], '8':[1336, 852], '9':[1477, 852], 'C':[1633, 852], 'X':[1209, 941], '0':[1336, 941], '#':[1477, 941], 'D':[1633, 941]}
    while num not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'X', '#']:
        num = input('Insira uma tecla do teclado DTMF: ')
    
    duracao = 5 #tempo do som em segundos
    fs = 44100 # taxa de amostragem
    A = 1  #Amplitude do sinal
    
    t = np.linspace(0, duracao, duracao*fs)
    print("Gerando Tons base")
    
    s1 = A*np.sin(dic_freq[num][0]*2*np.pi*t)
    s2 = A*np.sin(dic_freq[num][1]*2*np.pi*t)
    
    # plt.figure("wves")
    
    # plt.plot(t, s2)
    
    
    signal = signalMeu()
    sinal = s1 + s2
    
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(num))
    sd.play(sinal, fs)
    # Exibe gráficos
    
    plt.plot(t, sinal, label = "Resultante")
    plt.plot(t, s1, label = (str(dic_freq[num][0]) + " Hz"))
    plt.plot(t, s2, label = (str(dic_freq[num][1]) + " Hz"))
    plt.legend()
    
    plt.title("Ondas somadas no tempo")
    plt.xlabel("tempo (s)")
    plt.xlim([0, 0.01])
    
    
    
    # aguarda fim do audio
    sd.wait()
    signalMeu().plotFFT(sinal, fs)
    plt.show()

if __name__ == "_main_":
    main()