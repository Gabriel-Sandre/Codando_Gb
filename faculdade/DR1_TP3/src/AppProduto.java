// Exercícios 4, 5 e 6 - Testes da classe Produto.
public class AppProduto {
    public static void main(String[] args) {

        // Exercício 4 - Instanciação e uso dos métodos de atualização.
        Produto produto = new Produto();
        produto.nome = "Arroz";
        produto.preco = 25.00;
        produto.quantidadeEmEstoque = 10;

        produto.alterarPreco(27.50);
        produto.alterarQuantidade(15);
        produto.exibirInformacoes();

        // Exercício 5 - Uso dos getters e setters.
        System.out.println();
        Produto outroProduto = new Produto();
        outroProduto.setNome("Feijão");
        outroProduto.setPreco(3.75);
        outroProduto.setQuantidadeEmEstoque(20);

        int quantidade = outroProduto.getQuantidadeEmEstoque();
        System.out.println("Nome: " + outroProduto.getNome());
        System.out.println("Preço: " + outroProduto.getPreco());
        System.out.println("Quantidade em estoque: " + quantidade);

        // Exercício 6 - Criação do objeto usando o construtor com parâmetros.
        System.out.println();
        Produto leite = new Produto("Leite", 5.50, 30);
        leite.exibirInformacoes();
    }
}
