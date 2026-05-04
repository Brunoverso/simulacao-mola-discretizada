# Parte 1 - Matriz elastica

O sistema fisico e uma cadeia unidimensional com `N` massas iguais. Cada massa
pode se deslocar ao longo de uma direcao. Chamamos esses deslocamentos de

```text
x_1, x_2, ..., x_N
```

e agrupamos todos eles no vetor

```text
x = [x_1, x_2, ..., x_N]^T.
```

A matriz elastica `A` e a matriz que transforma o vetor de deslocamentos em uma
combinacao proporcional as forcas elasticas:

```text
m x'' = -k A x.
```

Ou seja, `A` guarda a informacao de quais massas estao ligadas por molas.

## Como montar a matriz

Para uma massa no interior da cadeia, isto e, uma massa que tem vizinho dos dois
lados, a forca elastica e

```text
F_i = -k(x_i - x_{i-1}) + k(x_{i+1} - x_i).
```

Reorganizando:

```text
F_i = -k(2x_i - x_{i-1} - x_{i+1}).
```

Por isso, uma linha interior da matriz tem a forma

```text
... -1   2   -1 ...
```

Se a massa tambem estiver presa a um ponto fixo por uma mola de constante `k_i`,
ela sente uma forca extra

```text
F_i extra = -k_i x_i.
```

Dividindo essa constante por `k`, a diagonal da matriz recebe o termo adicional
`k_i/k`. Assim, a diagonal fica

```text
numero de vizinhos + k_i/k.
```

Para uma cadeia aberta, as massas das pontas tem apenas um vizinho. Entao:

- a primeira massa tem diagonal `1 + k_1/k`;
- as massas do meio tem diagonal `2 + k_i/k`;
- a ultima massa tem diagonal `1 + k_N/k`;
- as posicoes imediatamente ao lado da diagonal principal recebem `-1`.

Uma forma compacta de escrever isso e

```text
A_ij = (2 + k_i/k) delta_ij
       - delta_i,j+1
       - delta_i,j-1
       - delta_ij delta_i1
       - delta_ij delta_iN.
```

Os dois ultimos termos corrigem as extremidades, porque a primeira e a ultima
massas possuem apenas um vizinho.

## Codigo

A rotina esta no arquivo `parte1_matriz_elastica.py`. Ela monta a matriz para
qualquer `N >= 2` e qualquer vetor de razoes `k_i/k`.

## Exemplo com N = 8

### Caso I: `k_i/k = 0` para todo `i`

Neste caso nenhuma massa esta presa a um ponto fixo. A matriz fica

```text
[[ 1 -1  0  0  0  0  0  0]
 [-1  2 -1  0  0  0  0  0]
 [ 0 -1  2 -1  0  0  0  0]
 [ 0  0 -1  2 -1  0  0  0]
 [ 0  0  0 -1  2 -1  0  0]
 [ 0  0  0  0 -1  2 -1  0]
 [ 0  0  0  0  0 -1  2 -1]
 [ 0  0  0  0  0  0 -1  1]]
```

Significado fisico: a cadeia esta livre nas extremidades. A primeira e a ultima
massas so estao ligadas a uma mola, enquanto as massas internas estao ligadas a
duas molas. Se todas as massas se deslocarem juntas da mesma forma, nenhuma mola
estica ou comprime. Por isso esse sistema possui um modo de translacao livre.

### Caso II: `k_1/k = 1`, `k_N/k = 1`, e os demais iguais a zero

Neste caso a primeira e a ultima massas estao presas a pontos fixos por molas de
mesma constante elastica `k` das molas internas. A matriz fica

```text
[[ 2 -1  0  0  0  0  0  0]
 [-1  2 -1  0  0  0  0  0]
 [ 0 -1  2 -1  0  0  0  0]
 [ 0  0 -1  2 -1  0  0  0]
 [ 0  0  0 -1  2 -1  0  0]
 [ 0  0  0  0 -1  2 -1  0]
 [ 0  0  0  0  0 -1  2 -1]
 [ 0  0  0  0  0  0 -1  2]]
```

Significado fisico: agora a cadeia nao pode se deslocar inteira livremente sem
deformar molas, porque as extremidades estao conectadas a pontos fixos. Isso
remove o modo de translacao livre. Fisicamente, e uma mola discreta presa nas
duas pontas.
