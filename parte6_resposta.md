# Parte 6 - Colisao com a parede

Nesta parte simulamos uma mola macroscopica discretizada colidindo com uma
parede. Usamos `N = 50` massas ligadas por molas e colocamos uma mola extra
ligando a ultima massa a uma parede fixa.

## Modelo usado

As condicoes iniciais sao

```text
x0 = [0, 0, ..., 0]
v0 = [v, v, ..., v]
```

Ou seja, inicialmente todas as massas estao em suas posicoes de equilibrio e
todas se movem com a mesma velocidade em direcao a parede.

A parede foi modelada como uma mola extra atuando apenas na ultima massa:

```text
V = (k_muro/k) e_N e_N^T.
```

Na pratica, isso significa somar `k_muro/k` ao ultimo elemento diagonal da
matriz elastica.

Se `A_livre` e a matriz da cadeia livre, entao a matriz usada na colisao e

```text
A = A_livre + V.
```

## Parametros escolhidos

Escolhemos unidades simples:

```text
N = 50
k = 1
m = 1
L = 1
v = 0.2
k_muro = 1
```

Com essa escolha, a velocidade teorica de propagacao do sinal e

```text
c = sqrt(k L^2 / m) = 1.
```

Escolher `k_muro = k` faz com que a parede tenha rigidez comparavel a das molas
internas. Assim o contato dura tempo suficiente para observar a perturbacao se
propagando pela cadeia.

## Tempo de descolamento

A simulacao foi feita enquanto a ultima massa tinha deslocamento positivo em
relacao a parede. O descolamento foi definido como o primeiro instante em que

```text
x_N(t) < 0.
```

Numericamente, encontramos:

```text
tempo de descolamento = 101.91470
deslocamento maximo da massa N = 0.21844
```

Esse valor faz sentido fisicamente. Como a cadeia tem comprimento aproximado

```text
(N - 1)L = 49,
```

o tempo para o sinal ir da parede ate a extremidade livre e voltar seria da
ordem de

```text
2 * 49 / c = 98.
```

O tempo encontrado, `101.91`, e proximo desse valor. A diferenca aparece porque
o sistema e discreto, a parede e modelada por uma mola finita, e o criterio de
descolamento depende da evolucao completa dos modos normais.

## Estimativa da velocidade de propagacao

Para estimar a velocidade do sinal, usamos o seguinte criterio:

1. Para cada massa, calculamos quando sua velocidade comeca a diferir da
   velocidade inicial `v`.
2. Definimos que o sinal chegou quando

```text
|v_i(t) - v| >= 0.10 v.
```

Como `v = 0.2`, o limiar usado foi

```text
0.10 v = 0.02.
```

3. Para cada massa, medimos a distancia ate a parede:

```text
d_i = (N - i)L.
```

4. Ajustamos uma reta:

```text
t_chegada = a d + b.
```

Como velocidade e distancia dividida por tempo, estimamos:

```text
c_estimado = 1/a.
```

Usando massas entre as distancias `5L` e `40L`, obtivemos:

```text
c teorico = 1.00000
c estimado = 1.02142
erro relativo = 2.14%
pontos usados no ajuste = 36
```

Portanto a simulacao recupera bem o valor teorico

```text
c = sqrt(k L^2 / m).
```

## Arquivos gerados

O codigo esta em:

```text
parte6_colisao_parede.py
```

A animacao da colisao ate o descolamento foi salva em:

```text
parte6_colisao_parede.gif
```

O grafico usado para estimar a velocidade do sinal foi salvo em:

```text
parte6_velocidade_sinal.png
```

Na animacao, a cor das massas fica mais avermelhada quando a velocidade daquela
massa se afasta mais da velocidade inicial. Isso ajuda a visualizar a frente da
perturbacao se propagando da parede para o restante da cadeia.
