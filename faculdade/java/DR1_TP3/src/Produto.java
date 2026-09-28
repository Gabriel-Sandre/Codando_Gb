// Exercícios 2, 3, 5 e 6 - Classe Produto do sistema do supermercado.
public class Produto {

    // Exercício 2 - Atributos.
    String nome;
    double preco;
    int quantidadeEmEstoque;

    // Exercício 6 - Construtor sem parâmetros (permite criar o objeto e
    // preencher os atributos depois, como nos exercícios 4 e 5).
    Produto() {
    }

    // Exercício 6 - Construtor que já inicializa os três atributos.
    Produto(String nome, double preco, int quantidadeEmEstoque) {
        this.nome = nome;
        this.preco = preco;
        this.quantidadeEmEstoque = quantidadeEmEstoque;
    }

    // Exercício 3 - Métodos básicos de atualização e exibição.
    void alterarPreco(double novoPreco) {
        preco = novoPreco;
    }

    void alterarQuantidade(int novaQuantidade) {
        quantidadeEmEstoque = novaQuantidade;
    }

    void exibirInformacoes() {
        System.out.println("Nome: " + nome);
        System.out.println("Preço: " + preco);
        System.out.println("Quantidade em estoque: " + quantidadeEmEstoque);
    }

    // Exercício 5 - Getters.
    String getNome() {
        return nome;
    }

    double getPreco() {
        return preco;
    }

    int getQuantidadeEmEstoque() {
        return quantidadeEmEstoque;
    }

    // Exercício 5 - Setters.
    void setNome(String novoNome) {
        nome = novoNome;
    }

    void setPreco(double novoPreco) {
        preco = novoPreco;
    }

    void setQuantidadeEmEstoque(int novaQuantidade) {
        quantidadeEmEstoque = novaQuantidade;
    }
}
