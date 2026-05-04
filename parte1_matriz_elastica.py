import numpy as np


def matriz_elastica(N, k_fixos=None):
    """Constroi a matriz elastica A para uma cadeia aberta de N massas.

    As massas vizinhas sao ligadas por molas de constante k. O vetor k_fixos
    contem as razoes k_i/k das molas extras que prendem cada massa a um ponto
    fixo. Por exemplo, k_fixos[0] = 1 significa que a primeira massa esta
    presa a uma parede por uma mola de constante k.
    """
    if N < 2:
        raise ValueError("N deve ser pelo menos 2.")

    if k_fixos is None:
        k_fixos = np.zeros(N)
    else:
        k_fixos = np.asarray(k_fixos, dtype=float)
        if k_fixos.shape != (N,):
            raise ValueError("k_fixos deve ter exatamente N elementos.")

    A = np.zeros((N, N), dtype=float)

    for i in range(N):
        numero_de_vizinhos = 0

        if i > 0:
            A[i, i - 1] = -1.0
            numero_de_vizinhos += 1

        if i < N - 1:
            A[i, i + 1] = -1.0
            numero_de_vizinhos += 1

        A[i, i] = numero_de_vizinhos + k_fixos[i]

    return A


def imprimir_matriz(nome, A):
    print(nome)
    print(A.astype(int) if np.allclose(A, A.astype(int)) else A)
    print()


if __name__ == "__main__":
    np.set_printoptions(linewidth=120)

    N = 8

    # Caso I: nenhuma massa presa a ponto fixo.
    k_fixos_I = np.zeros(N)
    A_I = matriz_elastica(N, k_fixos_I)

    # Caso II: primeira e ultima massas presas por molas de constante k.
    k_fixos_II = np.zeros(N)
    k_fixos_II[0] = 1
    k_fixos_II[-1] = 1
    A_II = matriz_elastica(N, k_fixos_II)

    imprimir_matriz("Caso I: k_i/k = 0 para todo i", A_I)
    imprimir_matriz("Caso II: k_1/k = 1, k_N/k = 1 e demais zero", A_II)
