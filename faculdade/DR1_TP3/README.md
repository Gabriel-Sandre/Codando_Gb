# DR1 – TP3 · Programação Orientada a Objetos em Java

Trabalho prático da competência **"Escrever programas em Java que utilizem classes e objetos"**.
Aluno: Gabriel Alves Sandre da Silva.

Os doze exercícios foram resolvidos em Java, compilados e executados — as saídas que aparecem
no PDF de entrega são as saídas reais dos programas.

## Entrega

📄 [`gabriel_alves_sandre_da_silva_DR1_TP3.PDF`](./gabriel_alves_sandre_da_silva_DR1_TP3.PDF)

## Estrutura

| Caminho | Conteúdo |
| --- | --- |
| `src/` | Código-fonte Java, uma classe pública por arquivo |
| `saidas/` | Saídas de console de cada execução, usadas no PDF |
| `prints/` | Prints da compilação e da execução (viram o anexo final do PDF) |
| `assets/` | Logo do Instituto Infnet usado na capa |
| `gerar_prints.py` | Executa o código e transforma a saída real do terminal em imagem |
| `executar.sh` | Compila tudo, executa as classes com `main` e regrava `saidas/` |
| `gerar_pdf.py` | Gera o PDF de entrega a partir de `src/` e `saidas/` (ReportLab) |

## Exercícios e arquivos

| Exercício | Assunto | Arquivos |
| --- | --- | --- |
| 1 | Classe, objeto, campos e métodos | `Carro.java`, `Main.java` |
| 2 | Classe `Produto` e seus atributos | `Produto.java` |
| 3 | `alterarPreco`, `alterarQuantidade`, `exibirInformacoes` | `Produto.java` |
| 4 | Teste da classe `Produto` | `AppProduto.java` |
| 5 | Getters e setters | `Produto.java`, `AppProduto.java` |
| 6 | Construtores | `Produto.java`, `AppProduto.java` |
| 7 | Classe `Conta` e seus atributos | `Conta.java` |
| 8 | `saca`, `deposita`, `calculaRendimento` | `Conta.java` |
| 9 | Teste da classe `Conta` | `TestaConta.java` |
| 10 | Classes `Circulo` e `Esfera` | `Circulo.java`, `Esfera.java` |
| 11 | `calcularArea` e `calcularVolume` | `Circulo.java`, `Esfera.java` |
| 12 | Teste das figuras geométricas | `TestaFiguras.java` |

## Como compilar e executar

```bash
./executar.sh
```

Ou manualmente:

```bash
javac -encoding UTF-8 -d out src/*.java

java -cp out Main            # Exercício 1
java -cp out AppProduto      # Exercícios 4, 5 e 6
java -cp out TestaConta      # Exercício 9
java -cp out TestaFiguras    # Exercício 12
```

Requisitos: JDK 17 ou superior (testado com OpenJDK 21).

## Como regerar o PDF

```bash
pip install reportlab pillow
./executar.sh          # atualiza as saídas do console
python3 gerar_prints.py # regera os prints do terminal (opcional)
python3 gerar_pdf.py    # regera o PDF de entrega, já com capa e anexo de prints
```

A capa (título, aluno, data e identificação do TP) fica nas constantes do topo de
`gerar_pdf.py`. Qualquer imagem colocada em `prints/` entra automaticamente no
anexo final do PDF, em ordem alfabética — basta nomear com prefixo numérico.
