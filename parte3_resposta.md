# Parte 3 - Condicoes iniciais

Nesta parte definimos os deslocamentos e velocidades iniciais das massas:

```text
|x0> = vetor de deslocamentos iniciais
|v0> = vetor de velocidades iniciais
```

Para `N = 8`, escolhemos a seguinte condicao inicial:

```text
x0 = [0, 0, 0, 1, -1, 0, 0, 0]
v0 = [0, 0, 0.5, 0, 0, -0.5, 0, 0]
```

Isso significa que, inicialmente:

- a quarta massa foi deslocada para um lado;
- a quinta massa foi deslocada para o lado oposto;
- a terceira massa recebeu velocidade positiva;
- a sexta massa recebeu velocidade negativa.

Essa escolha e arbitraria, mas tem uma vantagem: a soma dos deslocamentos e das
velocidades e zero. Assim, no caso da cadeia livre, nao estamos dando uma
translacao liquida ao sistema inteiro.

## Ideia matematica

Na parte 2, encontramos os autovetores normalizados da matriz elastica:

```text
u_1, u_2, ..., u_N.
```

Esses autovetores formam uma base ortonormal. Isso quer dizer que qualquer vetor
de deslocamentos pode ser escrito como uma soma deles:

```text
|x0> = u_1^x0 |u_1> + u_2^x0 |u_2> + ... + u_N^x0 |u_N>
```

e qualquer vetor de velocidades tambem:

```text
|v0> = u_1^v0 |u_1> + u_2^v0 |u_2> + ... + u_N^v0 |u_N>.
```

Os coeficientes sao obtidos por produto interno:

```text
u_n^x0 = <u_n | x0>
u_n^v0 = <u_n | v0>
```

Como os vetores aqui sao reais, esse produto interno e apenas o produto escalar
usual:

```text
<u_n | x0> = soma_i u_n[i] x0[i].
```

Se colocarmos todos os autovetores como colunas de uma matriz `U`, os
coeficientes sao calculados por:

```text
coef_x0 = U.T @ x0
coef_v0 = U.T @ v0
```

E a reconstrucao dos vetores originais e:

```text
x0 = U @ coef_x0
v0 = U @ coef_v0
```

## Codigo

A rotina esta no arquivo `parte3_condicoes_iniciais.py`.

```python
def decompor_condicoes_iniciais(autovetores, x0, v0):
    x0 = np.asarray(x0, dtype=float)
    v0 = np.asarray(v0, dtype=float)

    coef_x0 = autovetores.T @ x0
    coef_v0 = autovetores.T @ v0

    return coef_x0, coef_v0
```

## Resultados para N = 8

### Caso I: cadeia livre

```text
n  u_n^x0      u_n^v0
1   -0.00000   -0.00000
2    0.19509    0.27779
3   -0.00000   -0.00000
4    0.55557    0.49039
5    0.00000    0.00000
6   -0.83147   -0.09755
7    0.00000    0.00000
8    0.98079   -0.41573
```

O primeiro coeficiente e zero porque o primeiro modo da cadeia livre e a
translacao rigida:

```text
u_1 proporcional a [1, 1, 1, 1, 1, 1, 1, 1].
```

Como nossa condicao inicial tem soma total zero, ela nao contem esse modo de
translacao.

Erro maximo na reconstrucao:

```text
x0: 5.55e-16
v0: 2.50e-16
```

### Caso II: extremidades presas por molas

```text
n  u_n^x0      u_n^v0
1   -0.00000   -0.00000
2   -0.32246   -0.40825
3    0.00000    0.00000
4    0.60603    0.40825
5    0.00000   -0.00000
6   -0.81650   -0.00000
7    0.00000   -0.00000
8   -0.92849    0.40825
```

Neste caso nao existe modo de translacao livre, porque as extremidades estao
presas. Mesmo assim, a ideia matematica e a mesma: os autovetores formam uma
base, e a condicao inicial e escrita como uma combinacao linear desses modos.

Erro maximo na reconstrucao:

```text
x0: 4.44e-16
v0: 2.22e-16
```

Esses erros sao extremamente pequenos e aparecem apenas por arredondamento
numerico. Portanto a decomposicao esta funcionando corretamente.
