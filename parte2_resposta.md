# Parte 2 - Autovalores e autovetores

Nesta parte queremos encontrar os modos normais do sistema. Matematicamente,
isso significa resolver

```text
A u_n = lambda_n u_n.
```

Aqui:

- `A` e a matriz elastica;
- `u_n` e o autovetor, isto e, a forma espacial do modo normal;
- `lambda_n` e o autovalor associado;
- a frequencia angular do modo e

```text
omega_n = sqrt((k/m) lambda_n).
```

Como `A` e uma matriz real e simetrica, usamos `numpy.linalg.eigh`, que retorna
autovalores reais e autovetores ortonormais. Depois ordenamos os pares
`(lambda_n, u_n)` por ordem crescente de autovalor.

Observacao: o sinal global de um autovetor e arbitrario. Por exemplo, `u` e
`-u` representam o mesmo modo normal.

## Rotina numerica

A rotina esta no arquivo `parte2_autovalores.py`.

```python
def autovalores_autovetores(A):
    """Calcula autovalores e autovetores normalizados de A em ordem crescente."""
    autovalores, autovetores = np.linalg.eigh(A)

    ordem = np.argsort(autovalores)
    autovalores = autovalores[ordem]
    autovetores = autovetores[:, ordem]

    return autovalores, autovetores
```

Os autovetores retornados ja estao normalizados, ou seja,

```text
|u_n|^2 = 1.
```

## Resultados para N = 8

### Caso I: cadeia livre

Este e o caso `k_i/k = 0` para todo `i`.

| n | lambda_n | omega_n / sqrt(k/m) |
|---|----------|---------------------|
| 1 | 0.00000 | 0.00000 |
| 2 | 0.15224 | 0.39018 |
| 3 | 0.58579 | 0.76537 |
| 4 | 1.23463 | 1.11114 |
| 5 | 2.00000 | 1.41421 |
| 6 | 2.76537 | 1.66294 |
| 7 | 3.41421 | 1.84776 |
| 8 | 3.84776 | 1.96157 |

Autovetores normalizados:

```text
u_1 = [0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536, 0.3536]
u_2 = [ 0.4904,  0.4157,  0.2778,  0.0975, -0.0975, -0.2778, -0.4157, -0.4904]
u_3 = [ 0.4619,  0.1913, -0.1913, -0.4619, -0.4619, -0.1913,  0.1913,  0.4619]
u_4 = [-0.4157,  0.0975,  0.4904,  0.2778, -0.2778, -0.4904, -0.0975,  0.4157]
u_5 = [ 0.3536, -0.3536, -0.3536,  0.3536,  0.3536, -0.3536, -0.3536,  0.3536]
u_6 = [-0.2778,  0.4904, -0.0975, -0.4157,  0.4157,  0.0975, -0.4904,  0.2778]
u_7 = [-0.1913,  0.4619, -0.4619,  0.1913,  0.1913, -0.4619,  0.4619, -0.1913]
u_8 = [-0.0975,  0.2778, -0.4157,  0.4904, -0.4904,  0.4157, -0.2778,  0.0975]
```

Interpretacao fisica:

O primeiro autovalor e zero. O autovetor correspondente tem todos os componentes
iguais:

```text
u_1 proporcional a [1, 1, 1, 1, 1, 1, 1, 1].
```

Isso representa uma translacao rigida da cadeia inteira. Todas as massas se
deslocam juntas, nenhuma mola estica ou comprime, e portanto nao existe forca
restauradora. Por isso `lambda_1 = 0` e `omega_1 = 0`.

Os outros autovetores representam modos de vibracao internos da cadeia. Conforme
`n` aumenta, aparecem mais alternancias de sinal ao longo da cadeia. Isso
significa comprimentos de onda menores, maior deformacao das molas e frequencias
maiores.

### Caso II: extremidades presas por molas

Este e o caso `k_1/k = 1`, `k_N/k = 1`, e os demais termos iguais a zero.

| n | lambda_n | omega_n / sqrt(k/m) |
|---|----------|---------------------|
| 1 | 0.12061 | 0.34730 |
| 2 | 0.46791 | 0.68404 |
| 3 | 1.00000 | 1.00000 |
| 4 | 1.65270 | 1.28558 |
| 5 | 2.34730 | 1.53209 |
| 6 | 3.00000 | 1.73205 |
| 7 | 3.53209 | 1.87939 |
| 8 | 3.87939 | 1.96962 |

Autovetores normalizados:

```text
u_1 = [0.1612, 0.3030, 0.4082, 0.4642, 0.4642, 0.4082, 0.3030, 0.1612]
u_2 = [-0.3030, -0.4642, -0.4082, -0.1612,  0.1612,  0.4082,  0.4642,  0.3030]
u_3 = [-0.4082, -0.4082,  0.0000,  0.4082,  0.4082, -0.0000, -0.4082, -0.4082]
u_4 = [-0.4642, -0.1612,  0.4082,  0.3030, -0.3030, -0.4082,  0.1612,  0.4642]
u_5 = [ 0.4642, -0.1612, -0.4082,  0.3030,  0.3030, -0.4082, -0.1612,  0.4642]
u_6 = [-0.4082,  0.4082, -0.0000, -0.4082,  0.4082, -0.0000, -0.4082,  0.4082]
u_7 = [-0.3030,  0.4642, -0.4082,  0.1612,  0.1612, -0.4082,  0.4642, -0.3030]
u_8 = [ 0.1612, -0.3030,  0.4082, -0.4642,  0.4642, -0.4082,  0.3030, -0.1612]
```

Interpretacao fisica:

Neste caso nao existe autovalor zero. Isso acontece porque a cadeia nao pode
mais se mover inteira sem deformar alguma mola: as extremidades estao ligadas a
pontos fixos. Portanto qualquer deslocamento produz alguma forca restauradora.

O primeiro modo tem todos os componentes com o mesmo sinal e e o modo de menor
frequencia. Ele corresponde a uma oscilacao suave da cadeia, com as massas do
meio se deslocando mais do que as massas das extremidades.

Os modos seguintes tem cada vez mais trocas de sinal. Essas trocas indicam
regioes da cadeia que se movem em sentidos opostos. Quanto mais rapido o padrao
oscila no espaco, maior e o autovalor e maior e a frequencia do modo.
