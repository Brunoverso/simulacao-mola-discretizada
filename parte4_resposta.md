# Parte 4 - Evolucao temporal

Na parte 3 escrevemos as condicoes iniciais como combinacoes dos autovetores da
matriz elastica:

```text
|x0> = soma_n u_n^x0 |u_n>
|v0> = soma_n u_n^v0 |u_n>.
```

Agora usamos isso para calcular o movimento em qualquer instante de tempo.

## Equacao de movimento

A equacao de movimento do sistema massa-mola e

```text
m |x''(t)> = -k A |x(t)>.
```

Dividindo por `m`:

```text
|x''(t)> = -(k/m) A |x(t)>.
```

Como os autovetores de `A` formam uma base, escrevemos a posicao como

```text
|x(t)> = soma_n tau_n(t) |u_n>.
```

Cada `tau_n(t)` diz quanto do modo normal `n` esta presente no instante `t`.

Substituindo na equacao de movimento:

```text
soma_n tau_n''(t) |u_n> = -(k/m) A soma_n tau_n(t) |u_n>.
```

Como

```text
A |u_n> = lambda_n |u_n>,
```

temos

```text
soma_n tau_n''(t) |u_n>
= soma_n [-(k/m) lambda_n tau_n(t)] |u_n>.
```

Portanto, para cada modo normal separadamente:

```text
tau_n''(t) = -omega_n^2 tau_n(t),
```

onde

```text
omega_n = sqrt((k/m) lambda_n).
```

Ou seja: cada modo normal se comporta como um oscilador harmonico simples.

## Solucao para cada modo

Para o modo `n`, a solucao e

```text
tau_n(t) = u_n^x0 cos(omega_n t)
           + (u_n^v0 / omega_n) sin(omega_n t).
```

Derivando no tempo:

```text
tau_n'(t) = -omega_n u_n^x0 sin(omega_n t)
            + u_n^v0 cos(omega_n t).
```

Voltando para o vetor completo:

```text
|x(t)> = soma_n [
    u_n^x0 cos(omega_n t)
    + (u_n^v0 / omega_n) sin(omega_n t)
] |u_n>
```

e

```text
|v(t)> = soma_n [
    -omega_n u_n^x0 sin(omega_n t)
    + u_n^v0 cos(omega_n t)
] |u_n>.
```

Essas sao exatamente as formulas pedidas no enunciado.

## Observacao sobre o modo com omega = 0

No caso da cadeia livre, existe um autovalor zero. Ele representa a translacao
rigida do sistema inteiro. Nesse caso

```text
omega_n = 0.
```

A expressao

```text
sin(omega_n t) / omega_n
```

deve ser interpretada pelo limite:

```text
lim_{omega -> 0} sin(omega t) / omega = t.
```

Entao, para um modo de frequencia zero:

```text
tau_n(t) = u_n^x0 + u_n^v0 t
tau_n'(t) = u_n^v0.
```

Isso corresponde a movimento uniforme do centro de massa.

## Codigo

A rotina esta no arquivo `parte4_evolucao_temporal.py`.

Ela recebe:

- a matriz elastica `A`;
- os vetores iniciais `x0` e `v0`;
- os tempos desejados;
- os parametros `k` e `m`.

A funcao principal e:

```python
def evoluir_temporalmente(A, x0, v0, tempos, k=1.0, m=1.0):
    lambdas, autovetores = autovalores_autovetores(A)
    coef_x0, coef_v0 = decompor_condicoes_iniciais(autovetores, x0, v0)
    omegas = np.sqrt(np.maximum((k / m) * lambdas, 0.0))

    ...

    return posicoes, velocidades, lambdas, omegas, autovetores, coef_x0, coef_v0
```

## Exemplo numerico

Usamos novamente `N = 8`, `k = 1`, `m = 1` e

```text
x0 = [0, 0, 0, 1, -1, 0, 0, 0]
v0 = [0, 0, 0.5, 0, 0, -0.5, 0, 0].
```

Para os tempos

```text
t = 0.0, 0.5, 1.0, 1.5, 2.0
```

a rotina calcula os vetores `x(t)` e `v(t)`.

No caso I, cadeia livre, por exemplo:

```text
t = 0.00
x(t) = [ 0.,  0., -0.,  1., -1.,  0., -0.,  0.]
v(t) = [ 0. , -0. ,  0.5, -0. ,  0. , -0.5,  0. , -0. ]

t = 1.00
x(t) = [ 0.0049,  0.1009,  0.6752, -0.0645,  0.0645, -0.6752, -0.1009, -0.0049]
v(t) = [ 0.0245,  0.2915,  0.4372, -1.4418,  1.4418, -0.4372, -0.2915, -0.0245]

t = 2.00
x(t) = [ 0.1311,  0.5214,  0.3311, -0.5462,  0.5462, -0.3311, -0.5214, -0.1311]
v(t) = [ 0.2810,  0.3641, -1.0173,  0.6698, -0.6698,  1.0173, -0.3641, -0.2810]
```

No caso II, extremidades presas por molas, o movimento e parecido para tempos
curtos, mas com pequenas diferencas nas extremidades porque agora elas sentem as
molas presas aos pontos fixos.

## Verificacao

A rotina deve devolver exatamente as condicoes iniciais quando `t = 0`.

Os erros maximos encontrados foram:

```text
Caso I:
erro maximo em x(0): 5.55e-16
erro maximo em v(0): 2.50e-16

Caso II:
erro maximo em x(0): 4.44e-16
erro maximo em v(0): 2.22e-16
```

Esses erros sao apenas erros numericos de arredondamento. Portanto a evolucao
temporal esta consistente com as condicoes iniciais.
