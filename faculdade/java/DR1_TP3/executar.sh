#!/usr/bin/env bash
# Compila as classes do TP, executa cada classe com metodo main e grava as
# saidas em saidas/ (usadas na geracao do PDF de entrega).
set -e
cd "$(dirname "$0")"

rm -rf out
mkdir -p out saidas
javac -encoding UTF-8 -d out src/*.java

for classe in Main AppProduto TestaConta TestaFiguras; do
    echo "--- $classe ---"
    java -Dstdout.encoding=UTF-8 -cp out "$classe" | tee "saidas/$classe.txt"
    echo
done
