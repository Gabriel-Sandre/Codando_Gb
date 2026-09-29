"""Gera tp2.html a partir do modelo, preenchendo a tabela ator x caso de uso
e os diagramas UML com os mesmos dados, para que os dois nunca divirjam."""

import math
from html import escape
from pathlib import Path

AQUI = Path(__file__).parent

# Atores: chave -> (nome no diagrama, tipo de figura)
ATORES = {
    "RH": ("Analista de RH", "pessoa"),
    "GES": ("Gestor da área", "pessoa"),
    "EST": ("Estudante", "pessoa"),
    "COO": ("Coordenador da IE", "pessoa"),
    "MAIL": ("Serviço de E-mail", "sistema"),
    "TEMPO": ("Temporizador", "tempo"),
}
ORDEM_ATORES = ["RH", "GES", "EST", "COO", "MAIL", "TEMPO"]

# F = fornecedor de informação, C = consumidor, FC = ambos
REQUERIDOS = [
    ("UC01", "Solicitar abertura de vaga", {"GES": "F", "RH": "C"}),
    ("UC02", "Revisar e divulgar vaga", {"RH": "FC", "GES": "C"}),
    ("UC03", "Consultar vagas e candidatar-se", {"EST": "FC"}),
    ("UC04", "Acompanhar processo seletivo", {"RH": "FC", "GES": "FC", "EST": "C"}),
    ("UC05", "Agendar entrevista", {"RH": "F", "GES": "F", "EST": "C", "MAIL": "C"}),
    ("UC06", "Confirmar vínculo com a IE", {"RH": "FC", "COO": "FC", "MAIL": "C"}),
    ("UC07", "Registrar contratação", {"RH": "F", "GES": "C", "EST": "C", "COO": "C"}),
    ("UC08", "Manter plano de atividades", {"GES": "F", "EST": "C"}),
    ("UC09", "Registrar avaliação periódica", {"GES": "F", "EST": "C", "RH": "C"}),
    ("UC10", "Notificar prazos a vencer",
     {"TEMPO": "F", "MAIL": "C", "RH": "C", "GES": "C", "COO": "C"}),
    ("UC11", "Registrar encerramento ou prorrogação",
     {"RH": "F", "GES": "F", "EST": "C", "COO": "C"}),
    ("UC12", "Consultar situação do estágio", {"EST": "C"}),
    ("UC13", "Gerar relatórios de acompanhamento", {"RH": "FC", "COO": "C"}),
]

ADICIONAIS = [
    ("UC14", "Autenticar e gerir perfis de acesso",
     {"RH": "F", "GES": "F", "EST": "F", "COO": "F"}),
    ("UC15", "Manter instituições de ensino", {"RH": "F", "COO": "C"}),
    ("UC16", "Registrar relatório de atividades", {"EST": "F", "GES": "FC", "COO": "C"}),
    ("UC17", "Gerir documentos do contrato", {"RH": "F", "EST": "FC", "COO": "FC"}),
    ("UC18", "Registrar recesso do estagiário", {"GES": "F", "EST": "FC", "RH": "C"}),
    ("UC19", "Desistir de candidatura", {"EST": "F", "RH": "C", "GES": "C"}),
    ("UC20", "Configurar parâmetros do programa", {"RH": "F"}),
]

ROTULO = {"F": "F", "C": "C", "FC": "F/C"}


# ---------------------------------------------------------------- tabela

def linhas_tabela(casos, classe=""):
    out = []
    for cod, nome, papeis in casos:
        celulas = "".join(
            f'<td class="p {papeis.get(a, "").lower()}">{ROTULO.get(papeis.get(a, ""), "")}</td>'
            for a in ORDEM_ATORES
        )
        out.append(f'<tr class="{classe}"><td class="uc"><b>{cod}</b> {escape(nome)}</td>{celulas}</tr>')
    return "\n".join(out)


def tabela_mapeamento():
    cab = "".join(f"<th>{escape(ATORES[a][0])}</th>" for a in ORDEM_ATORES)
    return f"""<table class="mapa">
<thead><tr><th class="uc">Caso de uso</th>{cab}</tr></thead>
<tbody>
<tr class="grupo"><td colspan="7">Casos de uso requeridos (RF01–RF12 e regras do TP1)</td></tr>
{linhas_tabela(REQUERIDOS)}
<tr class="grupo"><td colspan="7">Casos de uso adicionais, a validar com os usuários</td></tr>
{linhas_tabela(ADICIONAIS, "extra")}
</tbody></table>"""


# ---------------------------------------------------------------- diagrama

LARG = 760
CX = LARG / 2
RX, RY = 128, 21
X_ESQ, X_DIR = 62, LARG - 62


def _seta(x1, y1, x2, y2, tam=8):
    """Ponta de seta aberta em (x2, y2), vinda de (x1, y1)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    pts = []
    for d in (+0.42, -0.42):
        pts.append((x2 - tam * math.cos(ang + d), y2 - tam * math.sin(ang + d)))
    return (f'<polyline points="{pts[0][0]:.1f},{pts[0][1]:.1f} {x2:.1f},{y2:.1f} '
            f'{pts[1][0]:.1f},{pts[1][1]:.1f}" class="ponta"/>')


def _figura(chave, x, y):
    nome, tipo = ATORES[chave]
    partes = nome.split(" ", 1) if len(nome) > 14 else [nome]
    texto_y = y + 44
    if tipo == "sistema":
        corpo = (f'<rect x="{x-38}" y="{y-24}" width="76" height="48" class="caixa"/>'
                 f'<text x="{x}" y="{y-6}" class="estereo">«sistema»</text>'
                 f'<text x="{x}" y="{y+10}" class="icone">✉</text>')
        texto_y = y + 40
    else:
        corpo = (f'<circle cx="{x}" cy="{y-26}" r="9" class="traco"/>'
                 f'<line x1="{x}" y1="{y-17}" x2="{x}" y2="{y+8}" class="traco"/>'
                 f'<line x1="{x-15}" y1="{y-8}" x2="{x+15}" y2="{y-8}" class="traco"/>'
                 f'<line x1="{x}" y1="{y+8}" x2="{x-12}" y2="{y+26}" class="traco"/>'
                 f'<line x1="{x}" y1="{y+8}" x2="{x+12}" y2="{y+26}" class="traco"/>')
        if tipo == "tempo":
            corpo += f'<text x="{x}" y="{y-44}" class="estereo">«tempo»</text>'
    rotulo = "".join(
        f'<text x="{x}" y="{texto_y + i*13}" class="ator">{escape(p)}</text>'
        for i, p in enumerate(partes)
    )
    return f'<g>{corpo}{rotulo}</g>'


def diagrama(casos, lado, y_atores, titulo, extends=(), passo=64, topo=110):
    """lado: ator -> 'E' ou 'D'; y_atores: ator -> y do centro da figura."""
    ys = {cod: topo + i * passo for i, (cod, _, _) in enumerate(casos)}
    altura = topo + (len(casos) - 1) * passo + 90

    # distribui os pontos de chegada ao redor da borda de cada elipse
    chegadas = {}
    for cod, _, papeis in casos:
        for s in "ED":
            atores = sorted((a for a in papeis if lado[a] == s), key=lambda a: y_atores[a])
            n = len(atores)
            for i, a in enumerate(atores):
                desloc = (i - (n - 1) / 2) * 0.32
                ang = math.pi + desloc if s == "E" else -desloc
                chegadas[(cod, a)] = (CX + RX * math.cos(ang), ys[cod] + RY * math.sin(ang))

    # e também ao lado de cada ator, para as pontas de seta não se sobreporem
    saidas = {}
    for a in lado:
        ligados = sorted((ys[cod], cod) for cod, _, p in casos if a in p)
        n = len(ligados)
        for i, (_, cod) in enumerate(ligados):
            saidas[(cod, a)] = y_atores[a] - 4 + (i - (n - 1) / 2) * min(5, 36 / max(n - 1, 1))

    linhas = []
    for cod, _, papeis in casos:
        for a, papel in papeis.items():
            ax = X_ESQ + 22 if lado[a] == "E" else X_DIR - 22
            if ATORES[a][1] == "sistema":
                ax = X_ESQ + 40 if lado[a] == "E" else X_DIR - 40
            ay = saidas[(cod, a)]
            ux, uy = chegadas[(cod, a)]
            linhas.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{ux:.1f}" y2="{uy:.1f}" class="assoc"/>')
            if "F" in papel:
                linhas.append(_seta(ax, ay, ux, uy))
            if "C" in papel:
                linhas.append(_seta(ux, uy, ax, ay))

    elipses = []
    for cod, nome, _ in casos:
        y = ys[cod]
        elipses.append(
            f'<ellipse cx="{CX}" cy="{y}" rx="{RX}" ry="{RY}" class="uc"/>'
            f'<text x="{CX}" y="{y-3}" class="cod">{cod}</text>'
            f'<text x="{CX}" y="{y+11}" class="nome">{escape(nome)}</text>'
        )

    ext = []
    for origem, destino, rot in extends:
        y1, y2 = ys[origem] - RY, ys[destino] + RY
        ext.append(f'<line x1="{CX}" y1="{y1}" x2="{CX}" y2="{y2+1}" class="tracejada"/>')
        ext.append(_seta(CX, y1, CX, y2 + 1, 7))
        ext.append(f'<text x="{CX+8}" y="{(y1+y2)/2+4}" class="estereo" text-anchor="start">{rot}</text>')

    atores = [
        _figura(a, X_ESQ if lado[a] == "E" else X_DIR, y_atores[a])
        for a in lado
        if any(a in p for _, _, p in casos)
    ]

    caixa = (f'<rect x="{CX-RX-34}" y="40" width="{2*(RX+34)}" height="{altura-52}" class="fronteira"/>'
             f'<text x="{CX}" y="62" class="sistema">{escape(titulo)}</text>')

    return (f'<svg viewBox="0 0 {LARG} {altura}" xmlns="http://www.w3.org/2000/svg" class="uml">'
            f'{caixa}{"".join(linhas)}{"".join(elipses)}{"".join(ext)}{"".join(atores)}</svg>')


LADO = {"GES": "E", "RH": "E", "EST": "D", "COO": "D", "MAIL": "D", "TEMPO": "D"}


def main():
    d1 = diagrama(
        REQUERIDOS, LADO,
        {"GES": 290, "RH": 690, "EST": 330, "COO": 600, "MAIL": 780, "TEMPO": 900},
        "Sistema de Gestão de Programas de Estágio",
        extends=[("UC05", "UC04", "«extend»")],
    )
    d2 = diagrama(
        ADICIONAIS, LADO,
        {"GES": 190, "RH": 420, "EST": 170, "COO": 380},
        "Casos de uso adicionais propostos",
    )
    modelo = (AQUI / "tp2.template.html").read_text(encoding="utf-8")
    html = (modelo.replace("{{TABELA_MAPA}}", tabela_mapeamento())
                  .replace("{{DIAGRAMA_REQUERIDOS}}", d1)
                  .replace("{{DIAGRAMA_ADICIONAIS}}", d2))
    (AQUI / "tp2.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
