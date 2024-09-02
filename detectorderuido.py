import numpy as np
import sounddevice as sd
import random
import time
import matplotlib.pyplot as graficos
import cv2 as opencv


#Variáveis
ListaDeVolumes = []
TodosPicosRegistrados = []
ListaTempoPicos = []
TodosValoresCapturados = []
DetectorPicos = {}
PossivelPico = False
tempo = 0


def medir_volume(*dados): 
    volume = np.linalg.norm(dados[0]) * 100
    ListaDeVolumes.append(int(volume))

def calcular_media():
    if len(ListaTempoPicos) > 0:
        substituto = ListaTempoPicos.copy()
        substituto.reverse()
        contar = 0
        Media = 0
        for e in substituto:
            if (contar + 1) != len(ListaTempoPicos):
                contar += 1
                Media += (e - substituto[contar])
        if len(ListaTempoPicos) == 1:
            return ListaTempoPicos[0]
        return int(Media / contar)
    else:
        return "Sem Picos"

def criar_graficos():
    graficos.plot(range(1,len(TodosValoresCapturados) + 1), TodosValoresCapturados, c="b")
    graficos.title("Volume Ruído")
    media = calcular_media()
    if type(media) == int or type(media) == float:
        graficos.xlabel(f"Tempo (Tempo Médio entre picos: {int(media//60):02}:{int(media%60):02})")
    else:
        graficos.xlabel(f"Tempo (Não houve picos, pois não houve nenhum pico súbito ou acima de 50.)")
    graficos.ylabel("Volume")
    try:
        graficos.savefig("graficos.png")
        img = opencv.imread("graficos.png")
        opencv.imshow("Gráfico", img)
        opencv.waitKey(0)
        opencv.destroyAllWindows()
    except Exception as erro:
        print(f"Ocorreu o erro {erro} ao tentar exibir os gráficos, veja se o script tem a permissão necessária.")


def perguntar(pergunta, respostaspermitidas):
    resposta = ""
    respostaspermitidas = [str(numero) for numero in respostaspermitidas]
    while resposta not in respostaspermitidas:
        resposta = str(input(pergunta))
    return resposta

def principal(tipo, retorno2, volumemaximo, skipar=None):
    global PossivelPico, tempo

    if not tipo and not volumemaximo:
        volumemaximo = random.randint(0,100)
        if not skipar:
            time.sleep(1)
    elif tipo and not volumemaximo:
        with sd.Stream(callback=medir_volume):
            sd.sleep(800)
        volumemaximo = int(np.clip(max(ListaDeVolumes), 0, 100))

    if PossivelPico:
        if volumemaximo <= 50 or (DetectorPicos[0] - volumemaximo) >= 20:
            Positivos = 0
            for index, valor in DetectorPicos.items():
                if index != 0:
                    if DetectorPicos[0] >= valor or valor <= 50:
                        Positivos += 1
            if Positivos == (len(DetectorPicos) - 1):
                TodosPicosRegistrados.append(DetectorPicos[0])
                ListaTempoPicos.append(tempo - (len(DetectorPicos) - 1))
                DetectorPicos.clear()
                PossivelPico = False
        else:
            calculo = (50 / 100) * volumemaximo
            if DetectorPicos[len(DetectorPicos) - 1] < calculo:
                TodosPicosRegistrados.append(DetectorPicos[0])
                ListaTempoPicos.append(tempo - (len(DetectorPicos) - 1))
                DetectorPicos.clear()
                DetectorPicos[0] = volumemaximo
            elif volumemaximo > DetectorPicos[0]:
                DetectorPicos.clear()
                DetectorPicos[len(DetectorPicos)] = volumemaximo
            else:
                DetectorPicos[len(DetectorPicos)] = volumemaximo

    if volumemaximo >= 50 and not PossivelPico:
        if len(TodosValoresCapturados) >= 2 and volumemaximo > TodosValoresCapturados[len(TodosValoresCapturados) - 1] and volumemaximo - TodosValoresCapturados[len(TodosValoresCapturados) - 1] >= 15:
            if (volumemaximo - TodosValoresCapturados[len(TodosValoresCapturados) - 1]) != (TodosValoresCapturados[len(TodosValoresCapturados) - 1] - TodosValoresCapturados[len(TodosValoresCapturados) - 2]) and (volumemaximo - TodosValoresCapturados[len(TodosValoresCapturados) - 1]) - (TodosValoresCapturados[len(TodosValoresCapturados) - 1] - TodosValoresCapturados[len(TodosValoresCapturados) - 2]) >= 4:
                if TodosValoresCapturados[len(TodosValoresCapturados) - 1] >= 50:
                    calculo = volumemaximo - TodosValoresCapturados[len(TodosValoresCapturados) - 1]
                    if calculo >= 15:
                        PossivelPico = True 
                        DetectorPicos[len(DetectorPicos)] = volumemaximo
                else:
                    PossivelPico = True
                    DetectorPicos[len(DetectorPicos)] = volumemaximo

        elif len(TodosValoresCapturados) < 2:
            PossivelPico = True
            DetectorPicos[len(DetectorPicos)] = volumemaximo

    TodosValoresCapturados.append(volumemaximo)
    ListaDeVolumes.clear()
    tempo += 1

    if tempo == int(retorno2) and PossivelPico:
        TodosPicosRegistrados.append(DetectorPicos[0])
        ListaTempoPicos.append(tempo - (len(DetectorPicos) - 1))
    print(f"Tempo decorrido:{tempo//60:02}:{tempo%60:02}")

def iniciar(tipo, ModoInput, skipar=False):
    retorno2 = perguntar("Qual tempo deseja de captura do ruído(em segundos)(10-300)? ", list(range(10,300)))
    while tempo < int(retorno2):
        if not ModoInput:
            principal(tipo, retorno2, None, skipar)
        else:
            valor = perguntar(f"Qual o valor do tempo {tempo + 1}?(0-100)", list(range(0,101)))
            principal(tipo, retorno2, int(valor))

    retorno = perguntar("Deseja ver os gráficos? S/N ", ["s", "S", "n", "N"])
    if retorno in "sS":
        criar_graficos()


retorno = perguntar("Deseja gerar valores baseado em: 1-Random 2-Volume do S.O 3-Input? ", [1, 2, 3])
if retorno == "1":
    retorno = perguntar("Deseja skipar o tempo de espera e obter logo o resultado?(Ss/Nn) ", ["S", "s", "n", "N"])
    if retorno in "Ss":
        iniciar(False, False, True)
    else:
        iniciar(False, False)
elif retorno == "2":
    iniciar(True, False, False)
else:
    iniciar(False, True, True)

media = calcular_media()
print("------------------Resultado Final------------------")
if type(media) == int or type(media) == float:
    print(f"Média entre picos: {(media//60):02}:{(media%60):02}")
    print(f"Todos picos registrados: {TodosPicosRegistrados}")
else:
    print("Não houve picos, pois não houve nenhum pico súbito ou acima de 50.")   
 
print(f"Todos valores de ruído capturados:{TodosValoresCapturados}")
print("-"*51)