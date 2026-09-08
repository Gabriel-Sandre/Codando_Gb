// Exercícios 7 e 8 - Classe Conta do sistema bancário.
public class Conta {

    // Exercício 7 - Atributos.
    String titular;
    int numero;
    String agencia;
    double saldo;
    String dataAbertura;

    // Exercício 8 - Métodos de saque, depósito e rendimento.
    void saca(double valor) {
        saldo = saldo - valor;
    }

    void deposita(double valor) {
        saldo = saldo + valor;
    }

    double calculaRendimento() {
        return saldo * 0.1;
    }
}
