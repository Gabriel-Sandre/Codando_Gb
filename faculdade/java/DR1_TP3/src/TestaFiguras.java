// Exercício 12 - Classe de teste das figuras geométricas.
public class TestaFiguras {
    public static void main(String[] args) {
        Circulo circulo = new Circulo();
        Esfera esfera = new Esfera();

        circulo.raio = 3.0;
        esfera.raio = 5.0;

        System.out.println("Área do círculo (raio 3.0): " + circulo.calcularArea());
        System.out.println("Volume da esfera (raio 5.0): " + esfera.calcularVolume());
    }
}
