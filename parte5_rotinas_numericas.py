import numpy as np
from PIL import Image, ImageDraw, ImageFont

from parte1_matriz_elastica import matriz_elastica
from parte3_condicoes_iniciais import exemplo_condicoes_iniciais
from parte4_evolucao_temporal import evoluir_temporalmente


def simular_sistema(N, A, x0, v0, k, m, t_inicial, t_final, num_tempos):
    """Calcula posicoes e velocidades das N massas em varios instantes.

    Argumentos:
        N: numero de massas.
        A: matriz elastica N x N.
        x0: deslocamentos iniciais.
        v0: velocidades iniciais.
        k: constante elastica das molas entre vizinhos.
        m: massa de cada particula.
        t_inicial, t_final: intervalo de simulacao.
        num_tempos: numero de instantes calculados.

    Retorna:
        tempos, posicoes, velocidades.

    A linha `posicoes[j]` contem as posicoes no instante `tempos[j]`.
    A linha `velocidades[j]` contem as velocidades no instante `tempos[j]`.
    """
    x0 = np.asarray(x0, dtype=float)
    v0 = np.asarray(v0, dtype=float)
    A = np.asarray(A, dtype=float)

    if A.shape != (N, N):
        raise ValueError("A deve ter dimensao N x N.")
    if x0.shape != (N,) or v0.shape != (N,):
        raise ValueError("x0 e v0 devem ter N componentes.")
    if num_tempos < 2:
        raise ValueError("num_tempos deve ser pelo menos 2.")

    tempos = np.linspace(t_inicial, t_final, num_tempos)
    posicoes, velocidades, *_ = evoluir_temporalmente(A, x0, v0, tempos, k=k, m=m)

    return tempos, posicoes, velocidades


def pontos_mola(x_a, x_b, y, amplitude=8, voltas=8):
    """Gera pontos de uma mola em zigue-zague entre x_a e x_b."""
    if x_b < x_a:
        x_a, x_b = x_b, x_a

    comprimento = x_b - x_a
    margem = min(16, comprimento / 5)
    inicio = x_a + margem
    fim = x_b - margem

    pontos = [(x_a, y), (inicio, y)]

    if fim > inicio:
        total = 2 * voltas
        for j in range(total + 1):
            frac = j / total
            x = inicio + frac * (fim - inicio)
            if j == 0 or j == total:
                y_j = y
            else:
                y_j = y + amplitude * (1 if j % 2 else -1)
            pontos.append((x, y_j))

    pontos.extend([(fim, y), (x_b, y)])
    return pontos


def criar_animacao(
    tempos,
    posicoes,
    arquivo_saida="parte5_animacao.gif",
    L=1.0,
    escala_deslocamento=0.35,
    fps=24,
    largura=900,
    altura=260,
):
    """Cria uma animacao GIF da cadeia massa-mola usando Pillow."""
    tempos = np.asarray(tempos, dtype=float)
    posicoes = np.asarray(posicoes, dtype=float)

    if posicoes.ndim != 2:
        raise ValueError("posicoes deve ter forma (num_tempos, N).")

    num_tempos, N = posicoes.shape
    equilibrio = np.arange(N) * L
    posicoes_fisicas = equilibrio[np.newaxis, :] + escala_deslocamento * posicoes

    x_min = np.min(posicoes_fisicas) - 0.75 * L
    x_max = np.max(posicoes_fisicas) + 0.75 * L
    if np.isclose(x_max, x_min):
        x_max = x_min + 1.0

    margem_x = 70
    y_mola = altura // 2
    raio = 11

    def converter_x(x):
        frac = (x - x_min) / (x_max - x_min)
        return margem_x + frac * (largura - 2 * margem_x)

    try:
        fonte = ImageFont.truetype("arial.ttf", 16)
        fonte_pequena = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        fonte = ImageFont.load_default()
        fonte_pequena = ImageFont.load_default()

    frames = []

    for indice, t in enumerate(tempos):
        imagem = Image.new("RGB", (largura, altura), "white")
        draw = ImageDraw.Draw(imagem)

        xs = [converter_x(x) for x in posicoes_fisicas[indice]]

        draw.line((margem_x, y_mola, largura - margem_x, y_mola), fill=(230, 230, 230), width=1)

        for i in range(N - 1):
            mola = pontos_mola(xs[i] + raio, xs[i + 1] - raio, y_mola, amplitude=7, voltas=6)
            draw.line(mola, fill=(70, 105, 140), width=2, joint="curve")

        for i, x in enumerate(xs):
            cor = (45, 95, 170)
            draw.ellipse((x - raio, y_mola - raio, x + raio, y_mola + raio), fill=cor, outline=(20, 45, 80), width=2)
            draw.text((x - 4, y_mola + 20), str(i + 1), fill=(30, 30, 30), font=fonte_pequena)

        draw.text((20, 20), f"t = {t:.2f}", fill=(20, 20, 20), font=fonte)
        draw.text((20, altura - 32), "Massas ligadas por molas - deslocamentos amplificados para visualizacao", fill=(80, 80, 80), font=fonte_pequena)

        frames.append(imagem)

    duracao_ms = int(1000 / fps)
    frames[0].save(
        arquivo_saida,
        save_all=True,
        append_images=frames[1:],
        duration=duracao_ms,
        loop=0,
    )

    return arquivo_saida


if __name__ == "__main__":
    N = 8
    k = 1.0
    m = 1.0

    k_fixos = np.zeros(N)
    A = matriz_elastica(N, k_fixos)

    x0, v0 = exemplo_condicoes_iniciais(N)
    tempos, posicoes, velocidades = simular_sistema(
        N=N,
        A=A,
        x0=x0,
        v0=v0,
        k=k,
        m=m,
        t_inicial=0.0,
        t_final=12.0,
        num_tempos=160,
    )

    arquivo = criar_animacao(
        tempos=tempos,
        posicoes=posicoes,
        arquivo_saida="parte5_animacao.gif",
        L=1.0,
        escala_deslocamento=0.35,
        fps=24,
    )

    print("Simulacao concluida.")
    print("tempos.shape =", tempos.shape)
    print("posicoes.shape =", posicoes.shape)
    print("velocidades.shape =", velocidades.shape)
    print("animacao =", arquivo)
    print("primeira posicao =", np.array2string(posicoes[0], precision=4, suppress_small=True))
    print("primeira velocidade =", np.array2string(velocidades[0], precision=4, suppress_small=True))
