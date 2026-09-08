"""Gera os prints do terminal (compilação e execução) usados no anexo do PDF.

Executa de fato o javac/java e transforma a saída real em imagem, no estilo de
um terminal. Uso: python3 gerar_prints.py
"""

import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
PRINTS = BASE / "prints"

FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONTE_NEGRITO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
TAMANHO = 26
MARGEM = 26
FUNDO = (30, 30, 30)
TEXTO = (222, 222, 222)
PROMPT = (126, 200, 126)
COMANDO = (235, 235, 235)
TITULO_BARRA = (60, 60, 60)


def executar(comando):
    processo = subprocess.run(
        comando, shell=True, cwd=BASE, capture_output=True, text=True
    )
    saida = processo.stdout + processo.stderr
    # descarta o aviso do JAVA_TOOL_OPTIONS do ambiente, que não faz parte do exercício
    linhas = [l for l in saida.splitlines() if not l.startswith("Picked up JAVA_TOOL_OPTIONS")]
    return "\n".join(linhas).rstrip()


def desenhar(nome_arquivo, titulo, blocos):
    """blocos: lista de (comando, saida)."""
    fonte = ImageFont.truetype(FONTE, TAMANHO)
    fonte_negrito = ImageFont.truetype(FONTE_NEGRITO, TAMANHO)
    altura_linha = TAMANHO + 8

    linhas = []
    for comando, saida in blocos:
        linhas.append(("prompt", comando))
        linhas.extend(("saida", linha) for linha in saida.splitlines())
        linhas.append(("saida", ""))

    largura_texto = max(len(texto) for _, texto in linhas) + 12
    largura = MARGEM * 2 + int(largura_texto * TAMANHO * 0.602)
    altura = MARGEM * 2 + 44 + altura_linha * len(linhas)

    imagem = Image.new("RGB", (largura, altura), FUNDO)
    desenho = ImageDraw.Draw(imagem)

    desenho.rectangle([0, 0, largura, 44], fill=TITULO_BARRA)
    for indice, cor in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        desenho.ellipse([18 + indice * 26, 15, 32 + indice * 26, 29], fill=cor)
    desenho.text((110, 12), titulo, font=fonte_negrito, fill=(200, 200, 200))

    y = 44 + MARGEM
    for tipo, texto in linhas:
        if tipo == "prompt":
            desenho.text((MARGEM, y), "$ ", font=fonte_negrito, fill=PROMPT)
            desenho.text((MARGEM + TAMANHO * 1.2, y), texto, font=fonte_negrito, fill=COMANDO)
        else:
            desenho.text((MARGEM, y), texto, font=fonte, fill=TEXTO)
        y += altura_linha

    PRINTS.mkdir(exist_ok=True)
    imagem.save(PRINTS / nome_arquivo)
    print(f"print gerado: prints/{nome_arquivo}")


def main():
    compilacao = executar("rm -rf out && mkdir -p out && javac -encoding UTF-8 -d out src/*.java && ls out")
    desenhar(
        "01-compilacao.png",
        "Terminal — compilação",
        [("javac -encoding UTF-8 -d out src/*.java", ""), ("ls out", compilacao)],
    )

    blocos = []
    for classe, exercicios in [
        ("Main", "exercício 1"),
        ("AppProduto", "exercícios 4, 5 e 6"),
    ]:
        saida = executar(f"java -Dstdout.encoding=UTF-8 -cp out {classe}")
        blocos.append((f"java -cp out {classe}    # {exercicios}", saida))
    desenhar("02-execucao-produto.png", "Terminal — Carro e Produto", blocos)

    blocos = []
    for classe, exercicios in [
        ("TestaConta", "exercício 9"),
        ("TestaFiguras", "exercício 12"),
    ]:
        saida = executar(f"java -Dstdout.encoding=UTF-8 -cp out {classe}")
        blocos.append((f"java -cp out {classe}    # {exercicios}", saida))
    desenhar("03-execucao-conta-figuras.png", "Terminal — Conta e Figuras", blocos)


if __name__ == "__main__":
    main()
