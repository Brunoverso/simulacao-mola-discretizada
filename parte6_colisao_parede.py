import numpy as np
from PIL import Image, ImageDraw, ImageFont

from parte1_matriz_elastica import matriz_elastica
from parte4_evolucao_temporal import evoluir_temporalmente


def matriz_colisao_parede(N, k=1.0, k_muro=1.0):
    """Matriz elastica para uma cadeia com a ultima massa ligada a parede."""
    k_fixos = np.zeros(N)
    k_fixos[-1] = k_muro / k
    return matriz_elastica(N, k_fixos)


def encontrar_tempo_descolamento(tempos, posicoes):
    """Encontra o primeiro instante em que x_N volta a ficar negativo."""
    x_ponta = posicoes[:, -1]
    ja_entrou_na_parede = False

    for i in range(1, len(tempos)):
        if x_ponta[i - 1] > 0 or x_ponta[i] > 0:
            ja_entrou_na_parede = True

        if ja_entrou_na_parede and x_ponta[i - 1] > 0 and x_ponta[i] <= 0:
            t0, t1 = tempos[i - 1], tempos[i]
            y0, y1 = x_ponta[i - 1], x_ponta[i]
            t_descola = t0 + (0.0 - y0) * (t1 - t0) / (y1 - y0)
            return t_descola

    raise RuntimeError("Nao foi encontrado descolamento no intervalo simulado.")


def interpolar_linhas(tempos_origem, valores_origem, tempos_destino):
    """Interpola cada coluna de valores_origem nos tempos_destino."""
    valores_destino = np.empty((len(tempos_destino), valores_origem.shape[1]))
    for coluna in range(valores_origem.shape[1]):
        valores_destino[:, coluna] = np.interp(
            tempos_destino, tempos_origem, valores_origem[:, coluna]
        )
    return valores_destino


def estimar_velocidade_sinal(
    tempos,
    velocidades,
    v_inicial,
    L=1.0,
    limiar_relativo=0.10,
    distancia_minima=5.0,
    distancia_maxima=None,
    t_maximo=None,
):
    """Estima a velocidade da frente de perturbacao.

    O criterio usado e: a perturbacao chega na massa i quando sua velocidade
    difere da velocidade inicial por pelo menos `limiar_relativo * |v_inicial|`.
    Depois ajustamos

        t_chegada = a * distancia + b

    e estimamos c como 1/a.
    """
    tempos = np.asarray(tempos, dtype=float)
    velocidades = np.asarray(velocidades, dtype=float)

    N = velocidades.shape[1]
    limiar = limiar_relativo * abs(v_inicial)
    if limiar <= 0:
        raise ValueError("v_inicial deve ser diferente de zero.")

    chegadas = []

    for i in range(N):
        desvio = np.abs(velocidades[:, i] - v_inicial)
        indices = np.where(desvio >= limiar)[0]
        if len(indices) == 0:
            continue

        j = indices[0]
        if j == 0:
            t_chegada = tempos[0]
        else:
            t0, t1 = tempos[j - 1], tempos[j]
            d0, d1 = desvio[j - 1], desvio[j]
            if np.isclose(d1, d0):
                t_chegada = t1
            else:
                t_chegada = t0 + (limiar - d0) * (t1 - t0) / (d1 - d0)

        distancia = (N - 1 - i) * L
        chegadas.append((i + 1, distancia, t_chegada))

    chegadas = np.array(chegadas, dtype=float)
    if distancia_maxima is None:
        distancia_maxima = 0.80 * (N - 1) * L
    if t_maximo is None:
        t_maximo = tempos[-1]

    mascara = (
        (chegadas[:, 1] >= distancia_minima)
        & (chegadas[:, 1] <= distancia_maxima)
        & (chegadas[:, 2] <= t_maximo)
    )

    dados_ajuste = chegadas[mascara]
    if len(dados_ajuste) < 2:
        raise RuntimeError("Poucos pontos para estimar a velocidade do sinal.")

    coef_angular, intercepto = np.polyfit(dados_ajuste[:, 1], dados_ajuste[:, 2], 1)
    c_estimado = 1.0 / coef_angular

    return {
        "limiar": limiar,
        "chegadas": chegadas,
        "dados_ajuste": dados_ajuste,
        "coef_angular": coef_angular,
        "intercepto": intercepto,
        "c_estimado": c_estimado,
    }


def criar_grafico_chegadas(resultado, c_teorico, arquivo_saida):
    """Cria um grafico PNG simples com chegada do sinal versus distancia."""
    dados = resultado["dados_ajuste"]
    chegadas = resultado["chegadas"]
    a = resultado["coef_angular"]
    b = resultado["intercepto"]

    largura, altura = 900, 520
    margem_esq, margem_dir = 80, 35
    margem_top, margem_base = 45, 70

    img = Image.new("RGB", (largura, altura), "white")
    draw = ImageDraw.Draw(img)

    try:
        fonte = ImageFont.truetype("arial.ttf", 16)
        fonte_titulo = ImageFont.truetype("arial.ttf", 21)
        fonte_pequena = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        fonte = ImageFont.load_default()
        fonte_titulo = ImageFont.load_default()
        fonte_pequena = ImageFont.load_default()

    x_min, x_max = 0.0, max(chegadas[:, 1]) * 1.03
    y_min, y_max = 0.0, max(chegadas[:, 2]) * 1.08

    def px(x):
        return margem_esq + (x - x_min) / (x_max - x_min) * (largura - margem_esq - margem_dir)

    def py(y):
        return altura - margem_base - (y - y_min) / (y_max - y_min) * (altura - margem_top - margem_base)

    draw.line((margem_esq, py(0), largura - margem_dir, py(0)), fill=(40, 40, 40), width=2)
    draw.line((margem_esq, margem_top, margem_esq, altura - margem_base), fill=(40, 40, 40), width=2)

    for valor in range(0, int(x_max) + 1, 10):
        x = px(valor)
        draw.line((x, py(0), x, py(0) + 5), fill=(40, 40, 40), width=1)
        draw.text((x - 10, py(0) + 10), str(valor), fill=(40, 40, 40), font=fonte_pequena)

    passo_y = 10
    for valor in range(0, int(y_max) + 1, passo_y):
        y = py(valor)
        draw.line((margem_esq - 5, y, margem_esq, y), fill=(40, 40, 40), width=1)
        draw.text((margem_esq - 42, y - 7), str(valor), fill=(40, 40, 40), font=fonte_pequena)

    for _, distancia, t_chegada in chegadas:
        draw.ellipse((px(distancia) - 3, py(t_chegada) - 3, px(distancia) + 3, py(t_chegada) + 3), fill=(160, 160, 160))

    for _, distancia, t_chegada in dados:
        draw.ellipse((px(distancia) - 4, py(t_chegada) - 4, px(distancia) + 4, py(t_chegada) + 4), fill=(35, 95, 170))

    x0, x1 = min(dados[:, 1]), max(dados[:, 1])
    draw.line((px(x0), py(a * x0 + b), px(x1), py(a * x1 + b)), fill=(210, 70, 55), width=3)

    draw.text((margem_esq, 15), "Estimativa da velocidade de propagacao", fill=(20, 20, 20), font=fonte_titulo)
    draw.text((largura // 2 - 110, altura - 35), "distancia ate a parede", fill=(40, 40, 40), font=fonte)
    draw.text((12, 18), "tempo", fill=(40, 40, 40), font=fonte)
    draw.text((margem_esq + 18, margem_top + 10), f"c teorico = {c_teorico:.3f}", fill=(20, 20, 20), font=fonte)
    draw.text((margem_esq + 18, margem_top + 34), f"c estimado = {resultado['c_estimado']:.3f}", fill=(20, 20, 20), font=fonte)

    img.save(arquivo_saida)
    return arquivo_saida


def criar_animacao_colisao(tempos, posicoes, velocidades, arquivo_saida, L=1.0, fps=24):
    """Cria uma animacao GIF da colisao da mola discretizada com a parede."""
    tempos = np.asarray(tempos, dtype=float)
    posicoes = np.asarray(posicoes, dtype=float)
    velocidades = np.asarray(velocidades, dtype=float)

    num_frames, N = posicoes.shape
    equilibrio = np.arange(N) * L
    fisicas = equilibrio[np.newaxis, :] + posicoes
    parede = equilibrio[-1]

    largura, altura = 1100, 520
    margem_x = 70
    y_cadeia = 155
    y_grafico_top = 275
    y_grafico_base = 455

    x_min = min(np.min(fisicas), -1.0)
    x_max = max(np.max(fisicas), parede + 0.5)
    y_min = np.min(posicoes) * 1.15
    y_max = np.max(posicoes) * 1.15
    if np.isclose(y_min, y_max):
        y_min, y_max = -1.0, 1.0

    def px_cadeia(x):
        return margem_x + (x - x_min) / (x_max - x_min) * (largura - 2 * margem_x)

    def px_indice(i):
        return margem_x + i / (N - 1) * (largura - 2 * margem_x)

    def py_deslocamento(y):
        return y_grafico_base - (y - y_min) / (y_max - y_min) * (y_grafico_base - y_grafico_top)

    try:
        fonte = ImageFont.truetype("arial.ttf", 16)
        fonte_titulo = ImageFont.truetype("arial.ttf", 20)
        fonte_pequena = ImageFont.truetype("arial.ttf", 12)
    except OSError:
        fonte = ImageFont.load_default()
        fonte_titulo = ImageFont.load_default()
        fonte_pequena = ImageFont.load_default()

    frames = []
    v_inicial = velocidades[0, 0]
    max_desvio = np.max(np.abs(velocidades - v_inicial))
    if np.isclose(max_desvio, 0.0):
        max_desvio = 1.0

    for frame, t in enumerate(tempos):
        img = Image.new("RGB", (largura, altura), "white")
        draw = ImageDraw.Draw(img)

        xs = [px_cadeia(x) for x in fisicas[frame]]
        x_parede = px_cadeia(parede)

        draw.text((25, 18), "Colisao da mola discretizada com a parede", fill=(20, 20, 20), font=fonte_titulo)
        draw.text((25, 50), f"t = {t:.2f}", fill=(20, 20, 20), font=fonte)

        draw.rectangle((x_parede, 82, x_parede + 14, 230), fill=(70, 70, 70))
        for yy in range(86, 228, 16):
            draw.line((x_parede + 14, yy, x_parede + 30, yy - 12), fill=(120, 120, 120), width=2)

        draw.line((margem_x, y_cadeia, largura - margem_x, y_cadeia), fill=(230, 230, 230), width=1)

        for i in range(N - 1):
            draw.line((xs[i], y_cadeia, xs[i + 1], y_cadeia), fill=(85, 115, 145), width=2)

        for i, x in enumerate(xs):
            desvio = abs(velocidades[frame, i] - v_inicial) / max_desvio
            vermelho = int(50 + 190 * min(desvio, 1.0))
            azul = int(180 - 120 * min(desvio, 1.0))
            cor = (vermelho, 90, azul)
            raio = 4 if N > 25 else 8
            if i == N - 1:
                raio += 2
            draw.ellipse((x - raio, y_cadeia - raio, x + raio, y_cadeia + raio), fill=cor, outline=(30, 30, 30))

        draw.text((25, 238), "Perfil dos deslocamentos x_i(t)", fill=(20, 20, 20), font=fonte)
        y_zero = py_deslocamento(0.0)
        draw.line((margem_x, y_zero, largura - margem_x, y_zero), fill=(210, 210, 210), width=1)
        draw.rectangle((margem_x, y_grafico_top, largura - margem_x, y_grafico_base), outline=(80, 80, 80), width=1)

        pontos = [(px_indice(i), py_deslocamento(posicoes[frame, i])) for i in range(N)]
        draw.line(pontos, fill=(30, 95, 170), width=2)
        for i in range(0, N, 5):
            x, y = pontos[i]
            draw.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(30, 95, 170))

        draw.text((margem_x, y_grafico_base + 12), "massa 1", fill=(40, 40, 40), font=fonte_pequena)
        draw.text((largura - margem_x - 55, y_grafico_base + 12), f"massa {N}", fill=(40, 40, 40), font=fonte_pequena)
        draw.text((x_parede - 38, 64), "parede", fill=(40, 40, 40), font=fonte_pequena)
        draw.text((25, altura - 28), "Cor mais avermelhada indica maior desvio da velocidade inicial.", fill=(80, 80, 80), font=fonte_pequena)

        frames.append(img)

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
    N = 50
    k = 1.0
    m = 1.0
    L = 1.0
    v = 0.2
    k_muro = 1.0

    c_teorico = np.sqrt(k * L**2 / m)
    A = matriz_colisao_parede(N, k=k, k_muro=k_muro)

    x0 = np.zeros(N)
    v0 = np.full(N, v)

    t_busca = 3.0 * (N - 1) * L / c_teorico
    tempos_busca = np.linspace(0.0, t_busca, 12000)
    pos_busca, vel_busca, *_ = evoluir_temporalmente(A, x0, v0, tempos_busca, k=k, m=m)

    t_descola = encontrar_tempo_descolamento(tempos_busca, pos_busca)

    mascara = tempos_busca <= t_descola
    tempos_contato = tempos_busca[mascara]
    pos_contato = pos_busca[mascara]
    vel_contato = vel_busca[mascara]

    resultado_velocidade = estimar_velocidade_sinal(
        tempos_contato,
        vel_contato,
        v_inicial=v,
        L=L,
        limiar_relativo=0.10,
        distancia_minima=5.0 * L,
        distancia_maxima=40.0 * L,
        t_maximo=t_descola,
    )

    num_frames = 240
    tempos_animacao = np.linspace(0.0, t_descola, num_frames)
    pos_animacao = interpolar_linhas(tempos_busca, pos_busca, tempos_animacao)
    vel_animacao = interpolar_linhas(tempos_busca, vel_busca, tempos_animacao)

    gif = criar_animacao_colisao(
        tempos_animacao,
        pos_animacao,
        vel_animacao,
        arquivo_saida="parte6_colisao_parede.gif",
        L=L,
        fps=24,
    )

    png = criar_grafico_chegadas(
        resultado_velocidade,
        c_teorico=c_teorico,
        arquivo_saida="parte6_velocidade_sinal.png",
    )

    erro_relativo = abs(resultado_velocidade["c_estimado"] - c_teorico) / c_teorico

    print("Parametros")
    print(f"N = {N}")
    print(f"k = {k}")
    print(f"m = {m}")
    print(f"L = {L}")
    print(f"v = {v}")
    print(f"k_muro = {k_muro}")
    print()
    print(f"tempo de descolamento = {t_descola:.5f}")
    print(f"deslocamento maximo da massa N = {np.max(pos_contato[:, -1]):.5f}")
    print()
    print(f"c teorico = {c_teorico:.5f}")
    print(f"c estimado = {resultado_velocidade['c_estimado']:.5f}")
    print(f"erro relativo = {100 * erro_relativo:.2f}%")
    print(f"limiar de chegada = {resultado_velocidade['limiar']:.5f}")
    print(f"pontos usados no ajuste = {len(resultado_velocidade['dados_ajuste'])}")
    print()
    print("arquivos gerados:")
    print(gif)
    print(png)
