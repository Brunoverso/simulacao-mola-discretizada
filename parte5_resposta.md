# Parte 5 - Rotinas numericas e visualizacao

Nesta parte usamos o que ja foi construido nas partes anteriores para montar
uma rotina numerica completa.

O objetivo e calcular, para varios tempos:

```text
x(t) = deslocamentos das massas
v(t) = velocidades das massas
```

No enunciado, `x(t)` representa o deslocamento de cada massa em relacao a sua
posicao de equilibrio. Para desenhar a cadeia, usamos tambem as posicoes de
equilibrio separadas por uma distancia `L`.

## Rotina numerica

A rotina principal esta no arquivo `parte5_rotinas_numericas.py`.

```python
def simular_sistema(N, A, x0, v0, k, m, t_inicial, t_final, num_tempos):
    tempos = np.linspace(t_inicial, t_final, num_tempos)
    posicoes, velocidades, *_ = evoluir_temporalmente(A, x0, v0, tempos, k=k, m=m)

    return tempos, posicoes, velocidades
```

Ela recebe:

- `N`: numero de massas;
- `A`: matriz elastica;
- `x0`: deslocamentos iniciais;
- `v0`: velocidades iniciais;
- `k`: constante elastica das molas;
- `m`: massa de cada particula;
- `t_inicial` e `t_final`: intervalo de simulacao;
- `num_tempos`: numero de instantes calculados.

Ela retorna:

```text
tempos
posicoes
velocidades
```

onde:

```text
tempos.shape = (num_tempos,)
posicoes.shape = (num_tempos, N)
velocidades.shape = (num_tempos, N)
```

Cada linha de `posicoes` contem os deslocamentos de todas as massas em um
instante. Cada linha de `velocidades` contem as velocidades correspondentes.

## Exemplo usado

Usamos:

```text
N = 8
k = 1
m = 1
t de 0 ate 12
160 instantes de tempo
```

com as condicoes iniciais:

```text
x0 = [0, 0, 0, 1, -1, 0, 0, 0]
v0 = [0, 0, 0.5, 0, 0, -0.5, 0, 0]
```

O script confirmou:

```text
tempos.shape = (160,)
posicoes.shape = (160, 8)
velocidades.shape = (160, 8)
```

e em `t = 0` recuperou:

```text
primeira posicao = [ 0.  0. -0.  1. -1.  0. -0.  0.]
primeira velocidade = [ 0.  -0.   0.5 -0.   0.  -0.5  0.  -0. ]
```

Ou seja, a simulacao comeca exatamente nas condicoes iniciais escolhidas.

## Visualizacao animada

Como `matplotlib` nao esta instalado no ambiente, a animacao foi feita usando
`Pillow`. O arquivo gerado foi:

```text
parte5_animacao.gif
```

A animacao possui:

```text
160 frames
tamanho 900 x 260 pixels
```

Para desenhar o sistema:

- as massas sao representadas por circulos;
- as molas sao representadas por linhas em zigue-zague;
- a posicao horizontal de cada massa e a posicao de equilibrio mais o
  deslocamento calculado;
- os deslocamentos foram amplificados apenas para melhorar a visualizacao.

Assim, a animacao mostra a evolucao temporal dos modos normais combinados pelas
condicoes iniciais.
