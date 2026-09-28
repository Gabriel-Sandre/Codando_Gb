# Faculdade — Instituto Infnet

Trabalhos práticos (TPs) e exercícios da graduação, organizados por matéria.

Esta pasta é **separada do portfólio**: os projetos que compõem o portfólio ficam na
raiz do repositório e estão listados no [README principal](../README.md). O que está
aqui é material acadêmico, mantido versionado por organização e histórico pessoal.

## Matérias

| Pasta | Matéria | Status |
| --- | --- | --- |
| [`java/`](./java) | Fundamentos de Desenvolvimento com Java | TP3 entregue |
| `csharp/` | Desenvolvimento com C# | a enviar |
| `python/` | Desenvolvimento com Python | a enviar |
| `sql/` | Introdução a Visualização de Dados e SQL | a enviar |

## Entregas

| Matéria | Entrega | Conteúdo | PDF |
| --- | --- | --- | --- |
| Java | [DR1 – TP3](./java/DR1_TP3) | POO: classes, objetos, atributos, métodos, getters/setters, construtores | [PDF](./java/DR1_TP3/gabriel_alves_sandre_da_silva_DR1_TP3.PDF) |

## Convenção usada nas entregas

Cada entrega fica em `faculdade/<matéria>/<DR>_<TP>/` e segue o mesmo padrão:

```
DR1_TP3/
├── src/            código-fonte que compila e roda
├── prints/         prints da compilação/execução (entram no anexo do PDF)
├── saidas/         saídas de console usadas no documento
├── assets/         logo da capa
├── executar.sh     compila e executa tudo
├── gerar_prints.py gera os prints a partir da execução real
├── gerar_pdf.py    gera o PDF de entrega (capa + exercícios + anexo de prints)
└── nome_sobrenome_DR1_TP3.PDF
```

O PDF é sempre gerado a partir do código de verdade: as saídas que aparecem no
documento são as saídas reais dos programas, não texto digitado à mão.

Nome do arquivo final segue a regra do Infnet: `nome_sobrenome_DR1_TP<N>.PDF`.
