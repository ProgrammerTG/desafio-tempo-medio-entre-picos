# Solução e Estratégias
Após verificação que qualquer oscilação só pode ser considerada pico a partir dos 50 de ruído. Minha estratégia foi a detectação a partir de qualquer valor a partir dos 50 e que seja uma subida razoável, utilizando vários tipos de verificação, sendo elas:

## Exemplos de entradas
O script fornece **3** tipos de entradas, sendo elas: **Áudio do S.O**, **Randômico**, **Input**

### Áudio do S.O
O áudio do S.O é capturado, e colocado em um range de 0, a 100.

### Randômico
É utilizado a função `.randint` para criar valores de 0 a 100

### Input
O usuário vai colocar todos os valores que ele deseja(0 a 100) um por um.

## Funções Adicionais

### Função 1
É possível após a finalização da obtenção dos dados, criar um gráfico básico igual do desafio para o usuário ver como foi os picos.

### Função 2 
É possível no modo randômico o usuário pular instantâneamente para o resultado final, para que não seja necessário os segundos.

### Função 3
O usuário pode colocar o valor de 10 a 300 segundos(5 minutos) de captura.

## Dificuldades e dúvidas

### Dificuldades
As maiores dificuldades foi a distinção de pseudo-picos e picos reais, isso foi um grande desafio principalmente para colocar os filtros em prática para obter uma maior acurácia

### Dúvidas
As dúvidas foram simples, apenas precisei de maior guiação sobre destacar os pseudo-picos dos picos reais, pois não soube muito bem a distinção de um pro outro nos valores, porém com o tempo fui entendendo melhor.

## Requesitos para rodar o código
### Interpretador
[Python](https://www.python.org/downloads/)

### Permissões para o script
É necessário que o script tenha permissão para criar e ler arquivos, já que o mesmo salva o gráfico e após isso abre usando opencv.

### Bibliotecas
Instalar usando CMD(Com permissões de administrador) após a instalação do interpretador Python. 
`pip install numpy`
`pip install sounddevice`
`pip install matplotlib`
`pip install opencv-python`

## Obtenção dos valores de tempo para a média, e formatação da média
Após a finalização de um pico, o tempo que é a váriavel `tempo` na qual armazena os segundos, é gravado em uma lista chamada `ListaTempoPicos` que após a finalização da execução do script são tratados na função `calcular_media()`. Na qual é criada uma cópia da lista
e a mesma é invertida utilizando a função `.reverse()` para melhor calcular o tempo entre cada pico, por exemplo:
ListaOriginal = [5,14,20,30]
ListaCopiadaEInvertida = [30,20,14,5]
Assim, sendo necessário apenas subtrair um valor pelo outro usando um for, e após isso dividir pela quantidade de vezes que o calculo foi feito, utilizando a variável `contar`
![image](https://github.com/user-attachments/assets/cdec4df0-fc49-4469-90d4-d426eec5aa2e)


## Armazenamento de todos os dados obtidos, para verificação posterior

### Todos valores de ruídos obtidos
### Todos picos registrados
### O tempo em segundos na qual o pico o ponto mais alto dele.
### Todos os volumes obtidos se a entrada de dados for som do S.O(Sistema Operacional).

## Detectação inicial de pico
Para que o programa começe a considerar que aquele valor é um pico, é necessário que o valor obtido após coleta seja igual ou maior que 50, para que após isso seja feito 2 verificações distintas para cada situação, sendo elas:
![image](https://github.com/user-attachments/assets/209e9370-b347-488e-985f-058e0578e8e3)


### Verificação 1
Verificar se não é um pico falso, já que algumas vezes o valor pode descer de 51 pra 49, e depois 50+ novamente, assim poderia dar um falso alarme de pico. Para isso foi feita as seguintes condições:
1-Verificar se não é o inicio da coleta de valores de ruído, para isso foi necessário verificar se a váriavel `TodosValoresCapturados` tenha obtido pelo menos 2 valores.
2-Após isso, também é verificado se o valor obtido seja maior que o gravado anteriormente na váriavel `TodosValoresCapturados` para verificar se realmente o valor está subindo, e não descendo ou seja igual ao anterior.
3-É verificado se há uma diferença significativa de **15** pontos de ruído.
![image](https://github.com/user-attachments/assets/e543c7dd-411e-4e0b-8b85-906a051c78d4)


### Verificação 1A
Após a verificação 1, é passado por outro *IF* para verificar as seguintes condições:
1-Verificar se não é um ritmo constante, invês de pico. Para verificar isso é verificado se o valor obtido na leitura atual subtraindo com a leitura anterior, seja diferente da leitura anterior subtraindo da antepenúltima leitura. E que a a subtração da leitura atual,
com a leitura anterior menos a leitura anterior subtraindo com a antepenútilma, tenha uma diferença de no mínimo 4 de valor. Exemplo:
Leitura Atual:45
Leitura Anterior:30
Antepenúltima leitura:15
Cálculo: Leitura Atual - Anterior = 15 | Leitura Anterior - Antepenúltima Leitura = 15 | 15 - 15 = 0
É um ritmo constante, e não um pico.
`if (volumemaximo - TodosValoresCapturados[len(TodosValoresCapturados) - 1]) != (TodosValoresCapturados[len(TodosValoresCapturados) - 1] - TodosValoresCapturados[len(TodosValoresCapturados) - 2]) and (volumemaximo - TodosValoresCapturados[len(TodosValoresCapturados) - 1]) - (TodosValoresCapturados[len(TodosValoresCapturados) - 1] - TodosValoresCapturados[len(TodosValoresCapturados) - 2]) >= 4:`

2-Se passado na verificação para detecta se não é um ritmo constante, é verificado se o valor anterior da leitura atual é maior que 50, na qual seria considerado um pico. Se for, é subtraido a leitura atual com a anterior, para ver se há uma distância de no mínimo 15 pontos. Para evitar falsos positivos por exemplo:
52, 50, 51 assim percebendo que ainda está oscilando e não recriando um pico.

![image](https://github.com/user-attachments/assets/6886d299-b423-4624-91c0-19363139e229)


3-Se a verificação 2 for negativa, é apenas indicado que é um pico, e começa a coleta de dados sobre o pico.

![image](https://github.com/user-attachments/assets/2f75d974-0f2f-4e4c-9255-4a692ceefd3a)


## Obtenção de valores e finalização do pico após detectar que houve um pico.
Após a afirmação que houve o inicio de um possível pico, é iniciado uma série de verificações para obter a maior acurácia possível. Porém antes das verificações, todos os valores posteriores a um pico, e também o próprio pico são guardados em um dicionário no python. Por exemplo:
Leituras: 30, 90, 81, 70, 0
O dicionário do pico, seria: {0: 90, 1:81, 2:70}
O maior valor(o pico) sempre será o valor número 0 do dicionário.

### Verificação 1
É utilizado para detectar se houve o fim do pico, caso não, seja incrementado valores no dicionário do pico.
1-É verificado se o valor de leitura atual, é menor que 50, ou há uma distância de 20 ou mais pontos pra baixo, da leitura máxima do pico. Se alguma das duas verificaçõs do IF estiverem correta, vai ocorrer outra verificação para finalizar o pico. Sendo ela a verificação **1A**

![image](https://github.com/user-attachments/assets/f894283b-a5a9-4027-8439-fd1ddedfb17c)


### Verificação 1A
1-É feito uma verificação na lista que armazena todos valores de um pico. Já que o pico pode ter uma oscilação grande para após isso descer, o dicionário que armazena os valores do pico não tem um tamanho fixo. Porém a verificação é feita de forma dinâmica, utilizando a seguinte lógica:
Após a verificação 1 tenha sido afirmativa, é feito uma verificação em todo o dicionário do Pico, usando **for index, valor in DetectorPicos.items()** e utilizando a variável `Positivos`. O for terá a verificação para verificar que os valores após o valor inicial(O 0 do dicionário que seria o pico)
seja menor que o pico, ou menor que 50. Se sim o positivo é acrescentado mais um ponto, para que após da verificação total da lista, seja feito a seguinte verificação **if Positivos == (len(DetectorPicos - 1)):** na qual se for afirmativa, o pico será finalizado e armazenado.

![image](https://github.com/user-attachments/assets/9e07f5fa-e16e-4f9b-a6af-88d4fb7a6a66)


### Verificação 2
Caso a verificação 1 seja negativa, será feita agora cálculos para adição de valores no dicionário de detectação de picos, ou para detectar se houve outro grande pico após o pico anterior, porém com um valor considerável para não ser considerado um pseudo-pico.


### Verificação 2A
1-É feito um cálculo para a detectação de outro grande pico, utilizando a lógica de que se a metade do valor da leitura atual seja maior que o valor da leitura anterior, seja detectado que houve outro grande pico, podendo usar o seguinte exemplo:
Leituras: 0,55, 46, 100
Nessa leitura, houve um grande pico no 59, porém após a possível queda dele, houve outro grande pico, sendo assim 2 grandes picos consideráveis. Porém se a leitura fosse [0,55,50,100] não seria dois grandes picos, já que não desceu o suficiente para fazer outro grande pico, sendo assim só seria contabilizado um pico.

![image](https://github.com/user-attachments/assets/52d79c17-ee00-4b48-b28a-b1463e19a9f3)


### Verificação 2B 
Caso o valor da leitura atual seja maior que a do pico, então o pico ainda não acabou, assim o dicionário é limpo e a leitura se reinicia com o valor da leitura atual sendo o pico.

![image](https://github.com/user-attachments/assets/b75fb70f-0884-44cd-a6a5-51c7b85b0e5e)


### Verificação 2C
Caso as verificações 2A e 2B sejam negativas, a verificação atual apenas colocará o valor da leitura atual no dicionário do Pico, já que não é maior que o pico e nem tem um grande intervalo.

![image](https://github.com/user-attachments/assets/21316466-2a77-4dd6-899e-d9943c176f2b)



