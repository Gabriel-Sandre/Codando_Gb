// Exercício 9 - Classe de teste da Conta.
public class TestaConta {
    public static void main(String[] args) {
        Conta conta = new Conta();
        conta.titular = "Gabriel Alves Sandre da Silva";
        conta.numero = 1234;
        conta.agencia = "0001";
        conta.saldo = 1000.00;
        conta.dataAbertura = "08/09/2026";

        System.out.println("Titular: " + conta.titular);
        System.out.println("Conta: " + conta.numero + " / Agência: " + conta.agencia);
        System.out.println("Data de abertura: " + conta.dataAbertura);
        System.out.println("Saldo inicial: " + conta.saldo);

        conta.saca(200.00);
        System.out.println("Saldo após saque de 200.00: " + conta.saldo);

        conta.deposita(500.00);
        System.out.println("Saldo após depósito de 500.00: " + conta.saldo);

        double rendimento = conta.calculaRendimento();
        System.out.println("Rendimento (10% do saldo): " + rendimento);
    }
}
