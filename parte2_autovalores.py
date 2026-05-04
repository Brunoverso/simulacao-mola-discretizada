import numpy as np

from parte1_matriz_elastica import matriz_elastica


def autovalores_autovetores(A):
    """Calcula autovalores e autovetores normalizados de A em ordem crescente."""
    autovalores, autovetores = np.linalg.eigh(A)

    ordem = np.argsort(autovalores)
    autovalores = autovalores[ordem]
    autovetores = autovetores[:, ordem]

    # O sinal de um autovetor e arbitrario. Esta convencao deixa a impressao
    # dos resultados deterministica e mais facil de comparar.
    for n in range(autovetores.shape[1]):
        indice_maior_componente = np.argmax(np.abs(autovetores[:, n]))
        if autovetores[indice_maior_componente, n] < 0:
            autovetores[:, n] *= -1

    return autovalores, autovetores


def imprimir_resultados(nome, autovalores, autovetores):
    print(nome)
    print("n  lambda_n    omega_n / sqrt(k/m)    autovetor u_n")
    print("-" * 78)

    for n, valor in enumerate(autovalores, start=1):
        omega_adimensional = np.sqrt(max(valor, 0.0))
        vetor = np.array2string(
            autovetores[:, n - 1],
            precision=4,
            suppress_small=True,
            separator=", ",
        )
        print(f"{n:1d}  {valor:8.5f}        {omega_adimensional:8.5f}        {vetor}")

    print()


if __name__ == "__main__":
    N = 8

    k_fixos_I = np.zeros(N)
    A_I = matriz_elastica(N, k_fixos_I)
    lambdas_I, vetores_I = autovalores_autovetores(A_I)

    k_fixos_II = np.zeros(N)
    k_fixos_II[0] = 1
    k_fixos_II[-1] = 1
    A_II = matriz_elastica(N, k_fixos_II)
    lambdas_II, vetores_II = autovalores_autovetores(A_II)

    imprimir_resultados("Caso I: cadeia livre", lambdas_I, vetores_I)
    imprimir_resultados("Caso II: extremidades presas por molas", lambdas_II, vetores_II)
