import numpy as np

from parte1_matriz_elastica import matriz_elastica
from parte2_autovalores import autovalores_autovetores
from parte3_condicoes_iniciais import (
    decompor_condicoes_iniciais,
    exemplo_condicoes_iniciais,
)


def evoluir_temporalmente(A, x0, v0, tempos, k=1.0, m=1.0):
    """Calcula x(t) e v(t) usando a decomposicao em modos normais.

    Retorna:
        posicoes: array com forma (len(tempos), N)
        velocidades: array com forma (len(tempos), N)
        lambdas: autovalores de A
        omegas: frequencias angulares sqrt((k/m) lambda_n)
        autovetores: matriz U com autovetores nas colunas
        coef_x0, coef_v0: coeficientes das condicoes iniciais
    """
    tempos = np.asarray(tempos, dtype=float)
    x0 = np.asarray(x0, dtype=float)
    v0 = np.asarray(v0, dtype=float)

    if x0.shape != v0.shape:
        raise ValueError("x0 e v0 devem ter o mesmo tamanho.")

    if A.shape != (x0.size, x0.size):
        raise ValueError("A deve ter dimensao N x N, com N = len(x0).")

    lambdas, autovetores = autovalores_autovetores(A)
    coef_x0, coef_v0 = decompor_condicoes_iniciais(autovetores, x0, v0)
    omegas = np.sqrt(np.maximum((k / m) * lambdas, 0.0))

    posicoes = np.zeros((tempos.size, x0.size), dtype=float)
    velocidades = np.zeros((tempos.size, x0.size), dtype=float)

    for n, omega in enumerate(omegas):
        u_n = autovetores[:, n]
        ux0 = coef_x0[n]
        uv0 = coef_v0[n]

        if np.isclose(omega, 0.0):
            # Limite omega -> 0: sin(omega t)/omega -> t.
            tau = ux0 + uv0 * tempos
            tau_ponto = np.full_like(tempos, uv0)
        else:
            omega_t = omega * tempos
            tau = ux0 * np.cos(omega_t) + (uv0 / omega) * np.sin(omega_t)
            tau_ponto = -omega * ux0 * np.sin(omega_t) + uv0 * np.cos(omega_t)

        posicoes += tau[:, np.newaxis] * u_n[np.newaxis, :]
        velocidades += tau_ponto[:, np.newaxis] * u_n[np.newaxis, :]

    return posicoes, velocidades, lambdas, omegas, autovetores, coef_x0, coef_v0


def imprimir_amostras(nome, tempos, posicoes, velocidades):
    print(nome)
    print("Cada linha mostra x(t) e v(t) para as 8 massas.")
    print()

    for t, x_t, v_t in zip(tempos, posicoes, velocidades):
        x_texto = np.array2string(x_t, precision=4, suppress_small=True, separator=", ")
        v_texto = np.array2string(v_t, precision=4, suppress_small=True, separator=", ")
        print(f"t = {t:.2f}")
        print(f"x(t) = {x_texto}")
        print(f"v(t) = {v_texto}")
        print()


if __name__ == "__main__":
    N = 8
    k = 1.0
    m = 1.0
    tempos = np.array([0.0, 0.5, 1.0, 1.5, 2.0])
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
        posicoes, velocidades, *_ = evoluir_temporalmente(A, x0, v0, tempos, k=k, m=m)

        erro_x0 = np.max(np.abs(posicoes[0] - x0))
        erro_v0 = np.max(np.abs(velocidades[0] - v0))

        imprimir_amostras(nome, tempos, posicoes, velocidades)
        print(f"erro maximo em x(0): {erro_x0:.2e}")
        print(f"erro maximo em v(0): {erro_v0:.2e}")
        print("=" * 80)
        print()
