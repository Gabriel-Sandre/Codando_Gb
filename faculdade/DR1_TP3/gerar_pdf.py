"""Gera o PDF de entrega do DR1 - TP3 a partir dos fontes Java em src/.

Uso: python3 gerar_pdf.py
Requer: reportlab (pip install reportlab)
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

BASE = Path(__file__).parent
SRC = BASE / "src"
SAIDAS = BASE / "saidas"
DESTINO = BASE / "gabriel_alves_sandre_da_silva_DR1_TP3.PDF"

AZUL = colors.HexColor("#1F3864")
CINZA_TEXTO = colors.HexColor("#333333")
FUNDO_CODIGO = colors.HexColor("#F4F6FA")
BORDA_CODIGO = colors.HexColor("#C9D2E3")
FUNDO_SAIDA = colors.HexColor("#F2F2F2")
BORDA_SAIDA = colors.HexColor("#CCCCCC")

estilos = getSampleStyleSheet()

ESTILO_TITULO = ParagraphStyle(
    "TituloTrabalho", parent=estilos["Title"], fontName="Helvetica-Bold",
    fontSize=20, leading=24, textColor=AZUL, spaceAfter=2,
)
ESTILO_SUBTITULO = ParagraphStyle(
    "SubtituloTrabalho", parent=estilos["Normal"], fontName="Helvetica",
    fontSize=13, leading=17, textColor=CINZA_TEXTO, alignment=1, spaceAfter=14,
)
ESTILO_ALUNO = ParagraphStyle(
    "Aluno", parent=estilos["Normal"], fontName="Helvetica-Bold",
    fontSize=11, leading=15, textColor=CINZA_TEXTO, alignment=1, spaceAfter=16,
)
ESTILO_SECAO = ParagraphStyle(
    "Secao", parent=estilos["Heading2"], fontName="Helvetica-Bold",
    fontSize=13, leading=16, textColor=AZUL, spaceBefore=14, spaceAfter=6,
)
ESTILO_TEXTO = ParagraphStyle(
    "Texto", parent=estilos["Normal"], fontName="Helvetica", fontSize=10.5,
    leading=15, textColor=CINZA_TEXTO, alignment=TA_JUSTIFY, spaceAfter=6,
)
ESTILO_LEGENDA = ParagraphStyle(
    "Legenda", parent=estilos["Normal"], fontName="Helvetica-Bold",
    fontSize=9, leading=12, textColor=AZUL, spaceBefore=4, spaceAfter=3,
)
ESTILO_CODIGO = ParagraphStyle(
    "Codigo", parent=estilos["Code"], fontName="Courier", fontSize=8.2,
    leading=10.4, textColor=colors.HexColor("#1A1A1A"),
    leftIndent=0, rightIndent=0, spaceBefore=0, spaceAfter=0,
)
ESTILO_SAIDA = ParagraphStyle(
    "Saida", parent=ESTILO_CODIGO, textColor=colors.HexColor("#1A1A1A"),
)


def _bloco(texto, estilo, fundo, borda, largura):
    """Envolve texto pré-formatado em uma caixa com fundo e borda."""
    tabela = Table([[Preformatted(texto, estilo)]], colWidths=[largura])
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), fundo),
                ("BOX", (0, 0), (-1, -1), 0.6, borda),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return tabela


def codigo(nome_arquivo, largura, apenas=None):
    """Bloco de código lido de src/<nome_arquivo>."""
    texto = (SRC / nome_arquivo).read_text(encoding="utf-8").rstrip()
    if apenas is not None:
        linhas = texto.splitlines()
        texto = "\n".join(linhas[apenas[0]:apenas[1]]).rstrip()
    return [
        KeepTogether([
            Paragraph(f"Arquivo: {nome_arquivo}", ESTILO_LEGENDA),
            _bloco(texto, ESTILO_CODIGO, FUNDO_CODIGO, BORDA_CODIGO, largura),
        ]),
        Spacer(1, 4),
    ]


def codigo_em_partes(nome_arquivo, largura, linha_corte):
    """Bloco de código longo dividido em duas partes, para não estourar a página."""
    linhas = (SRC / nome_arquivo).read_text(encoding="utf-8").rstrip().splitlines()
    partes = ["\n".join(linhas[:linha_corte]).rstrip(), "\n".join(linhas[linha_corte:]).rstrip()]
    elementos = []
    for indice, texto in enumerate(partes, start=1):
        elementos.append(
            KeepTogether([
                Paragraph(
                    f"Arquivo: {nome_arquivo} (parte {indice} de {len(partes)})", ESTILO_LEGENDA
                ),
                _bloco(texto, ESTILO_CODIGO, FUNDO_CODIGO, BORDA_CODIGO, largura),
            ])
        )
        elementos.append(Spacer(1, 4))
    return elementos


def trecho(texto, largura, legenda=None):
    partes = []
    if legenda:
        partes.append(Paragraph(legenda, ESTILO_LEGENDA))
    partes.append(_bloco(texto.strip(), ESTILO_CODIGO, FUNDO_CODIGO, BORDA_CODIGO, largura))
    return [KeepTogether(partes), Spacer(1, 4)]


def saida_texto(texto, largura, legenda="Saída correspondente no console:"):
    """Bloco de saída de console a partir de um texto já conhecido."""
    return [
        KeepTogether([
            Paragraph(legenda, ESTILO_LEGENDA),
            _bloco(texto.strip(), ESTILO_SAIDA, FUNDO_SAIDA, BORDA_SAIDA, largura),
        ]),
        Spacer(1, 4),
    ]


def saida(nome_classe, largura):
    texto = (SAIDAS / f"{nome_classe}.txt").read_text(encoding="utf-8").rstrip()
    return [
        KeepTogether([
            Paragraph(f"Saída no console (java {nome_classe}):", ESTILO_LEGENDA),
            _bloco(texto, ESTILO_SAIDA, FUNDO_SAIDA, BORDA_SAIDA, largura),
        ]),
        Spacer(1, 4),
    ]


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawString(2.2 * cm, 1.3 * cm, "DR1 – TP3 · Gabriel Alves Sandre da Silva")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.3 * cm, f"Página {doc.page}")
    canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
    canvas.line(2.2 * cm, 1.7 * cm, A4[0] - 2.2 * cm, 1.7 * cm)
    canvas.restoreState()


def construir():
    doc = BaseDocTemplate(
        str(DESTINO), pagesize=A4,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
        topMargin=2.0 * cm, bottomMargin=2.2 * cm,
        title="DR1 - TP3 - Programacao Orientada a Objetos em Java",
        author="Gabriel Alves Sandre da Silva",
        subject="Competencia: escrever programas em Java que utilizem classes e objetos",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="corpo")
    doc.addPageTemplates([PageTemplate(id="padrao", frames=[frame], onPage=rodape)])
    L = doc.width

    e = []
    e.append(Paragraph("DR1 – TP3", ESTILO_TITULO))
    e.append(Paragraph("Programação Orientada a Objetos em Java", ESTILO_SUBTITULO))
    e.append(Paragraph("Aluno: Gabriel Alves Sandre da Silva", ESTILO_ALUNO))
    e.append(
        Paragraph(
            "Este trabalho apresenta as soluções dos doze exercícios propostos, abordando classes, "
            "objetos, atributos, métodos, getters e setters, construtores e métodos de cálculo. "
            "Todo o código foi escrito em Java, compilado com <font face='Courier'>javac</font> e "
            "executado com <font face='Courier'>java</font>; as saídas mostradas em cada exercício "
            "são as saídas reais obtidas na execução.",
            ESTILO_TEXTO,
        )
    )

    # ---------------- Exercício 1 ----------------
    e.append(Paragraph("Exercício 1 – Conceitos de Classe, Objeto, Campos e Métodos", ESTILO_SECAO))
    e.append(Paragraph(
        "<b>Classe</b> é o molde que define quais características e comportamentos os objetos daquele "
        "tipo terão. Ela não guarda dados por si só: descreve como os objetos serão. "
        "<b>Objeto</b> é uma instância criada a partir desse molde, com valores próprios; cada objeto "
        "ocupa seu próprio espaço na memória. <b>Campos</b> (ou atributos) são as variáveis declaradas "
        "na classe, responsáveis por armazenar os dados de cada objeto. <b>Métodos</b> são os "
        "comportamentos que o objeto pode executar, podendo ler ou alterar os seus próprios atributos.",
        ESTILO_TEXTO))
    e.append(Paragraph(
        "No exemplo abaixo, <font face='Courier'>Carro</font> é a classe; "
        "<font face='Courier'>marca</font> e <font face='Courier'>modelo</font> são os campos; "
        "<font face='Courier'>ligar()</font> é o método, que utiliza os dois campos na mensagem exibida; "
        "e <font face='Courier'>meuCarro</font> é o objeto criado com "
        "<font face='Courier'>new Carro()</font>.",
        ESTILO_TEXTO))
    e += codigo("Carro.java", L)
    e += codigo("Main.java", L)
    e += saida("Main", L)

    # ---------------- Exercício 2 ----------------
    e.append(Paragraph("Exercício 2 – Criando a Classe “Produto”", ESTILO_SECAO))
    e.append(Paragraph(
        "A classe <font face='Courier'>Produto</font> representa cada item cadastrado no supermercado. "
        "O atributo <b>nome</b> (String) identifica o produto na listagem e nas buscas do sistema. "
        "O atributo <b>preco</b> (double) registra o valor de venda e é do tipo decimal porque preços "
        "raramente são números inteiros. O atributo <b>quantidadeEmEstoque</b> (int) informa quantas "
        "unidades existem, sendo inteiro porque o controle é feito por unidades e é ele que permite "
        "saber quando repor a mercadoria.",
        ESTILO_TEXTO))
    e += trecho("""public class Produto {
    String nome;
    double preco;
    int quantidadeEmEstoque;
}""", L, "Estrutura inicial da classe (versão do exercício 2)")

    # ---------------- Exercício 3 ----------------
    e.append(Paragraph("Exercício 3 – Métodos Básicos da Classe “Produto”", ESTILO_SECAO))
    e.append(Paragraph(
        "O método <font face='Courier'>alterarPreco</font> recebe um novo valor e o grava no atributo "
        "<font face='Courier'>preco</font>, sendo usado em uma remarcação. "
        "<font face='Courier'>alterarQuantidade</font> faz o mesmo com "
        "<font face='Courier'>quantidadeEmEstoque</font>, refletindo entradas e saídas de mercadoria. "
        "Já <font face='Courier'>exibirInformacoes</font> não altera nada: apenas lê os três atributos "
        "e mostra no console o estado atual do objeto, servindo como o registro pedido no contexto.",
        ESTILO_TEXTO))
    e += trecho("""void alterarPreco(double novoPreco) {
    preco = novoPreco;
}

void alterarQuantidade(int novaQuantidade) {
    quantidadeEmEstoque = novaQuantidade;
}

void exibirInformacoes() {
    System.out.println("Nome: " + nome);
    System.out.println("Preço: " + preco);
    System.out.println("Quantidade em estoque: " + quantidadeEmEstoque);
}""", L, "Métodos acrescentados à classe Produto")

    # ---------------- Exercício 4 ----------------
    e.append(Paragraph("Exercício 4 – Testando a Classe “Produto”", ESTILO_SECAO))
    e.append(Paragraph(
        "A classe <font face='Courier'>AppProduto</font> contém o método "
        "<font face='Courier'>main</font>. Nele o objeto é instanciado, recebe os valores iniciais "
        "(Arroz, 25.00 e 10 unidades), tem preço e quantidade atualizados por "
        "<font face='Courier'>alterarPreco</font> e <font face='Courier'>alterarQuantidade</font> e, "
        "por fim, exibe as informações — confirmando que as alterações foram aplicadas.",
        ESTILO_TEXTO))
    e += trecho("""Produto produto = new Produto();
produto.nome = "Arroz";
produto.preco = 25.00;
produto.quantidadeEmEstoque = 10;

produto.alterarPreco(27.50);
produto.alterarQuantidade(15);
produto.exibirInformacoes();""", L, "Trecho do main de AppProduto.java")
    e += saida_texto("""Nome: Arroz
Preço: 27.5
Quantidade em estoque: 15""", L)

    # ---------------- Exercício 5 ----------------
    e.append(Paragraph("Exercício 5 – Criando Métodos de Propriedade (Getters e Setters)", ESTILO_SECAO))
    e.append(Paragraph(
        "Os <b>getters</b> devolvem o valor de cada atributo e os <b>setters</b> recebem um novo valor "
        "e o gravam. Mesmo sem usar modificadores de visibilidade, eles são úteis porque centralizam o "
        "acesso aos dados: se um dia for preciso validar o preço (impedir valor negativo, por exemplo) "
        "ou registrar quem alterou o estoque, basta mudar o setter, e todo o restante do sistema "
        "continua funcionando sem alteração. Também padronizam o código, já que todo o programa passa "
        "a ler e escrever os atributos da mesma maneira.",
        ESTILO_TEXTO))
    e += trecho("""String getNome() {
    return nome;
}

double getPreco() {
    return preco;
}

int getQuantidadeEmEstoque() {
    return quantidadeEmEstoque;
}

void setNome(String novoNome) {
    nome = novoNome;
}

void setPreco(double novoPreco) {
    preco = novoPreco;
}

void setQuantidadeEmEstoque(int novaQuantidade) {
    quantidadeEmEstoque = novaQuantidade;
}""", L, "Getters e setters da classe Produto")
    e += trecho("""Produto outroProduto = new Produto();
outroProduto.setNome("Feijão");
outroProduto.setPreco(3.75);
outroProduto.setQuantidadeEmEstoque(20);

int quantidade = outroProduto.getQuantidadeEmEstoque();
System.out.println("Nome: " + outroProduto.getNome());
System.out.println("Preço: " + outroProduto.getPreco());
System.out.println("Quantidade em estoque: " + quantidade);""",
                L, "Exemplo de uso no main")
    e += saida_texto("""Nome: Feijão
Preço: 3.75
Quantidade em estoque: 20""", L)
    e.append(Paragraph(
        "A chamada <font face='Courier'>setPreco(3.75)</font> seguida de "
        "<font face='Courier'>getPreco()</font> confirma que o valor foi atualizado.",
        ESTILO_TEXTO))

    # ---------------- Exercício 6 ----------------
    e.append(Paragraph("Exercício 6 – Adicionando Construtores à Classe “Produto”", ESTILO_SECAO))
    e.append(Paragraph(
        "O construtor é executado no momento em que o objeto é criado com "
        "<font face='Courier'>new</font>. Ele recebe nome, preço e quantidade como parâmetros e usa "
        "<font face='Courier'>this</font> para diferenciar o atributo do parâmetro de mesmo nome, "
        "atribuindo os valores de uma só vez. Assim o objeto já nasce completo e válido, em vez de "
        "existir por um tempo com atributos vazios até que os setters sejam chamados um a um. "
        "Isso reduz a chance de esquecer algum dado e deixa o código de criação mais curto e legível.",
        ESTILO_TEXTO))
    e.append(Paragraph(
        "Foi mantido também um construtor sem parâmetros, para que as criações dos exercícios 4 e 5 "
        "(<font face='Courier'>new Produto()</font>) continuem válidas na mesma classe.",
        ESTILO_TEXTO))
    e += trecho("""Produto() {
}

Produto(String nome, double preco, int quantidadeEmEstoque) {
    this.nome = nome;
    this.preco = preco;
    this.quantidadeEmEstoque = quantidadeEmEstoque;
}""", L, "Construtores da classe Produto")
    e += trecho("""Produto leite = new Produto("Leite", 5.50, 30);
leite.exibirInformacoes();""", L, "Criação do objeto usando o construtor")
    e += saida_texto("""Nome: Leite
Preço: 5.5
Quantidade em estoque: 30""", L)
    e.append(Paragraph(
        "A classe <font face='Courier'>Produto</font> completa — reunindo os atributos do exercício 2, "
        "os métodos do exercício 3, os getters e setters do exercício 5 e os construtores do exercício "
        "6 — está no anexo, ao final deste documento, junto da classe de teste "
        "<font face='Courier'>AppProduto</font> e da saída completa da execução.",
        ESTILO_TEXTO))

    # ---------------- Exercício 7 ----------------
    e.append(Paragraph("Exercício 7 – Modelando uma Conta Bancária", ESTILO_SECAO))
    e.append(Paragraph(
        "A classe <font face='Courier'>Conta</font> segue as convenções do Java (nome no singular e "
        "iniciando com letra maiúscula) e reúne os cinco atributos pedidos: "
        "<b>titular</b> (dono da conta), <b>numero</b> (identificador da conta), <b>agencia</b> "
        "(mantida como String por poder começar com zero, como em “0001”), <b>saldo</b> (valor "
        "disponível, decimal) e <b>dataAbertura</b> (registro de quando a conta foi criada).",
        ESTILO_TEXTO))
    e += trecho("""public class Conta {
    String titular;
    int numero;
    String agencia;
    double saldo;
    String dataAbertura;
}""", L, "Estrutura inicial da classe (versão do exercício 7)")

    # ---------------- Exercício 8 ----------------
    e.append(Paragraph("Exercício 8 – Criando Métodos", ESTILO_SECAO))
    e.append(Paragraph(
        "<font face='Courier'>saca(double valor)</font> subtrai o valor informado do saldo. "
        "<font face='Courier'>deposita(double valor)</font> soma o valor ao saldo. "
        "<font face='Courier'>calculaRendimento()</font> não recebe parâmetro e apenas devolve o saldo "
        "multiplicado por 0.1, ou seja, 10% — repare que ele retorna o valor em vez de alterar o saldo, "
        "exatamente como pede o enunciado.",
        ESTILO_TEXTO))
    e += codigo("Conta.java", L)

    # ---------------- Exercício 9 ----------------
    e.append(Paragraph("Exercício 9 – Vamos testar nossa classe", ESTILO_SECAO))
    e.append(Paragraph(
        "A classe <font face='Courier'>TestaConta</font> instancia uma conta, preenche os cinco "
        "atributos e executa as três operações, exibindo o saldo antes e depois de cada uma. Partindo "
        "de 1000.00, o saque de 200.00 leva o saldo a 800.00, o depósito de 500.00 o leva a 1300.00 e "
        "o rendimento devolve 130.00, que corresponde a 10% desse saldo final — confirmando que os "
        "métodos funcionam como esperado.",
        ESTILO_TEXTO))
    e += codigo("TestaConta.java", L)
    e += saida("TestaConta", L)

    # ---------------- Exercício 10 ----------------
    e.append(Paragraph("Exercício 10 – Definindo Classes para Formas Geométricas", ESTILO_SECAO))
    e.append(Paragraph(
        "As classes <font face='Courier'>Circulo</font> e <font face='Courier'>Esfera</font> foram "
        "criadas de forma independente, sem herança ou qualquer recurso avançado. O atributo "
        "<b>raio</b> é fundamental em ambas porque é a única medida de que os cálculos dependem: a "
        "área do círculo é obtida a partir do raio ao quadrado e o volume da esfera, do raio ao cubo. "
        "Sem esse atributo, não haveria como calcular nem uma coisa nem outra. Ele é "
        "<font face='Courier'>double</font> por aceitar medidas fracionadas.",
        ESTILO_TEXTO))
    e += trecho("""public class Circulo {
    double raio;
}

public class Esfera {
    double raio;
}""", L, "Estrutura inicial das classes (versão do exercício 10)")

    # ---------------- Exercício 11 ----------------
    e.append(Paragraph("Exercício 11 – Criando Métodos de Cálculo", ESTILO_SECAO))
    e.append(Paragraph(
        "<font face='Courier'>calcularArea()</font> retorna π × raio² e "
        "<font face='Courier'>calcularVolume()</font> retorna (4/3) × π × raio³. Foi utilizado "
        "<font face='Courier'>Math.PI</font>, constante já fornecida pelo Java, que é mais precisa do "
        "que digitar o valor aproximado. A divisão foi escrita como "
        "<font face='Courier'>4.0 / 3.0</font> justamente para que o Java faça a conta com decimais: "
        "se fosse <font face='Courier'>4 / 3</font>, o resultado seria 1 e o volume sairia errado. "
        "Os dois métodos apenas devolvem o resultado, sem imprimir nada.",
        ESTILO_TEXTO))
    e += codigo("Circulo.java", L)
    e += codigo("Esfera.java", L)

    # ---------------- Exercício 12 ----------------
    e.append(Paragraph("Exercício 12 – Testando as Classes de Figuras", ESTILO_SECAO))
    e.append(Paragraph(
        "A classe <font face='Courier'>TestaFiguras</font> instancia um círculo de raio 3.0 e uma "
        "esfera de raio 5.0, chama os métodos de cálculo e exibe os resultados. Os valores obtidos "
        "conferem com o cálculo manual: π × 9 ≈ 28,27 e (4/3) × π × 125 ≈ 523,60.",
        ESTILO_TEXTO))
    e += codigo("TestaFiguras.java", L)
    e += saida("TestaFiguras", L)

    # ---------------- Anexo ----------------
    e.append(Paragraph("Anexo – Classe Produto completa (exercícios 2 a 6)", ESTILO_SECAO))
    e.append(Paragraph(
        "Como a classe <font face='Courier'>Produto</font> foi construída em etapas ao longo dos "
        "exercícios 2, 3, 5 e 6, segue abaixo o arquivo final reunindo tudo, com a classe de teste e "
        "a saída completa da execução.",
        ESTILO_TEXTO))
    e += codigo_em_partes("Produto.java", L, 35)
    e += codigo("AppProduto.java", L)
    e += saida("AppProduto", L)

    # ---------------- Como compilar ----------------
    e.append(Paragraph("Organização dos arquivos e execução", ESTILO_SECAO))
    e.append(Paragraph(
        "Cada classe pública ficou em seu próprio arquivo, com o mesmo nome da classe, como exige o "
        "Java: <font face='Courier'>Carro.java</font>, <font face='Courier'>Main.java</font>, "
        "<font face='Courier'>Produto.java</font>, <font face='Courier'>AppProduto.java</font>, "
        "<font face='Courier'>Conta.java</font>, <font face='Courier'>TestaConta.java</font>, "
        "<font face='Courier'>Circulo.java</font>, <font face='Courier'>Esfera.java</font> e "
        "<font face='Courier'>TestaFiguras.java</font>. Para compilar e executar, basta compilar os "
        "arquivos em conjunto e rodar a classe que contém o método "
        "<font face='Courier'>main</font> desejado:",
        ESTILO_TEXTO))
    e.append(KeepTogether(_bloco(
        "javac -encoding UTF-8 -d out src/*.java\n\n"
        "java -cp out Main            # Exercício 1\n"
        "java -cp out AppProduto      # Exercícios 4, 5 e 6\n"
        "java -cp out TestaConta      # Exercício 9\n"
        "java -cp out TestaFiguras    # Exercício 12",
        ESTILO_CODIGO, FUNDO_CODIGO, BORDA_CODIGO, L)))

    doc.build(e)
    print(f"PDF gerado: {DESTINO}")


if __name__ == "__main__":
    construir()
