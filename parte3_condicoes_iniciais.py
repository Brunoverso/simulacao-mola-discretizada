import numpy as np

from parte1_matriz_elastica import matriz_elastica
from parte2_autovalores import autovalores_autovetores


def decompor_condicoes_iniciais(autovetores, x0, v0):
    """Projeta x0 e v0 na base ortonormal formada pelos autovetores.

    Se as colunas de autovetores sao u_1, ..., u_N, entao os coeficientes sao

        u_n^{x0} = <u_n | x0>
        u_n^{v0} = <u_n | v0>

    Em notacao matricial, isso e simplesmente U.T @ x0 e U.T @ v0.
    """
    x0 = np.asarray(x0, dtype=float)
    v0 = np.asarray(v0, dtype=float)

    if x0.shape != v0.shape:
        raise ValueError("x0 e v0 devem ter o mesmo tamanho.")

    if autovetores.shape[0] != x0.shape[0]:
        raise ValueError("O numero de linhas de autovetores deve bater com x0.")

    coef_x0 = autovetores.T @ x0
    coef_v0 = autovetores.T @ v0

    return coef_x0, coef_v0


def reconstruir_vetor(autovetores, coeficientes):
    """Reconstrui um vetor a partir dos coeficientes na base dos autovetores."""
    return autovetores @ coeficientes


def exemplo_condicoes_iniciais(N):
    """Define uma condicao inicial simples para N = 8."""
    if N != 8:
        raise ValueError("Este exemplo foi escolhido especificamente para N = 8.")

    x0 = np.array([0, 0, 0, 1, -1, 0, 0, 0], dtype=float)
    v0 = np.array([0, 0, 0.5, 0, 0, -0.5, 0, 0], dtype=float)

    return x0, v0


def imprimir_decomposicao(nome, x0, v0, coef_x0, coef_v0, erro_x0, erro_v0):
    print(nome)
    print("x0 =", x0)
    print("v0 =", v0)
    print()
    print("n  u_n^x0      u_n^v0")
    print("-" * 29)

    for n, (cx, cv) in enumerate(zip(coef_x0, coef_v0), start=1):
        print(f"{n:1d}  {cx:9.5f}  {cv:9.5f}")

    print()
    print(f"erro maximo na reconstrucao de x0: {erro_x0:.2e}")
    print(f"erro maximo na reconstrucao de v0: {erro_v0:.2e}")
    print()


if __name__ == "__main__":
    N = 8
    x0, v0 = exemplo_condicoes_iniciais(N)

    casos = []

    k_fixos_I = np.zeros(N)
    casos.append(("Caso I: cadeia livre", k_fixos_I))

    k_fixos_II = np.zeros(N)
    k_fixos_II[0] = 1
    k_fixos_II[-1] = 1
    casos.append(("Caso II: extremidades presas por molas", k_fixos_II))

    for nome, k_fixos in casos:
        A = matriz_elastica(N, k_fixos)
        _, autovetores = autovalores_autovetores(A)

        coef_x0, coef_v0 = decompor_condicoes_iniciais(autovetores, x0, v0)

        x0_reconstruido = reconstruir_vetor(autovetores, coef_x0)
        v0_reconstruido = reconstruir_vetor(autovetores, coef_v0)

        erro_x0 = np.max(np.abs(x0 - x0_reconstruido))
        erro_v0 = np.max(np.abs(v0 - v0_reconstruido))

        imprimir_decomposicao(nome, x0, v0, coef_x0, coef_v0, erro_x0, erro_v0)
