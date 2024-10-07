# desafio-tempo-medio-entre-picos 
Desafio de programação - Tempo Médio Entre Picos

# Dificuldade do desafio
Este desafio tem dificuldade média

# Introdução
Bem-vindo ao desafio TMEP: desafio Tempo Médio Entre Picos!

O desafio TMEP é um desafio de programação que tem como objetivo incentivar o raciocínio lógico e algoritmico!

# Regras

- Fork esse repositório.
- Implemente uma solução para o desafio usando qualquer linguagem de programação que você quiser! (veja mais detalhes abaixo)
- Descreva a sua solução em um arquivo chamado ```SOLUTION.md``` usando o markdown do github (veja mais detalhes abaixo)
- Commit/Push sua solução mais o arquivo ```SOLUTION.md``` para o **SEU FORK**!
- Envie o link do seu fork para o nosso time de recrutamento
- Aguarde nosso feedback!

# Descreva a sua solução
No arquivo ```SOLUTION.md``` você deve explicar:

- Como você implementou a sua solução (suas ideias e estratégias)
- Como você gerou os dados para validar a sua solução
- Exemplos de entradas para testar a sua implementação
- Quais as maiores dificuldades ou dúvidas que você encontrou quando estava desenvolvendo a sua solução
- Como executar a sua solução (compilar? Instalar algum interpretador?)

# Desafio
Considere a seguinte imagem:

![image](https://github.com/norelod/desafio-tempo-medio/assets/37966960/971a85af-ba38-4524-bda7-2a0744f4f7cf)

Essa imagem representa a leitura de um sensor que está mendindo um processo que oscila continuamente para cima e para baixo.

Todo sensor tem ruído. No caso desse sensor, o ruído gera alguns "picos" falsos aleatórios principalmente quando o valor está decaindo.

Nessa imagem, podemos ver 4 "picos" verdadeiros. Os picos verdadeiros são os pontos máximios locais destacados em vermelho na imagem abaixo:

![image](https://github.com/norelod/desafio-tempo-medio/assets/37966960/152617d7-b002-4ed8-a005-20109be4934c)

Note que os pontos de cor azul não são picos verdadeiros.

A diferença entre um ponto do gráfico e o ponto seguinte é sempre de 1 segundo. O valor mínimo de um ponto (eixo y) é zero e o máximo é 100. O valor mínimo de um pico é 50.

Calcule o **tempo médio entre os picos** dado um intervalo contendo dados. Por exemplo, na última imagem, o tempo médio será: 

TMEP = (18 + 15 + 14) / 3 = 15

De forma simples, o tempo médio entre picos será a **soma de tempo entre os picos dividido pela quantidade de picos menos 1**.

Escreva a sua solução para gerar o tempo médio usando minutos e segundos. Por exemplo: 11:32, 08:43, 13:02, 00:35, etc.

# Dicas

- Use boas práticas de algoritmos
- A sua descição em ```SOLUTION.md``` é tão importante quanto o seu código
- Use boas práticas de programação, como métodos e variáveis com nomes intuitivos
- Não perca muito tempo com formatação do markdown. Ai menos é mais.
- Sentiu falta de alguma coisa? Seja criativo!
