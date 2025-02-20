#!/bin/bash

echo -n Histogramas:
mkdir -p resultados/base
mkdir -p resultados/hist
for img in $(ls imagens)
do
    nome="${img%.*}"
    echo -n ' ' $nome
    convert imagens/$img resultados/base/$nome.png
    python3 histograma.py imagens/$img resultados/hist/$nome.pgf
done
echo; echo

function run {
    argv=($@)
    python3 limiarizacao -o resultados/$1/$3.png \
        imagens/$2.pgm $1 ${argv[@]:3}
    echo $1 $3 ${argv[@]:3} $(python3 porcentagem.py resultados/$1/$3.png)
}

mkdir -p resultados/global
run global retina retina -T 128
run global wedge wedge100 -T 100
run global wedge wedge110 -T 110
echo

mkdir -p resultados/bernsen
run bernsen baboon baboon -r 50
run bernsen peppers peppers -r 50
run bernsen wedge wedge -r 20
run bernsen sonnet sonnet -r 20
echo

mkdir -p resultados/niblack
run niblack sonnet sonnet50 -r 50 -k -0.5
run niblack sonnet sonnet20 -r 20 -k -0.5
run niblack wedge wedge -r 50 -k -0.3
run niblack fiducial fiducial -r 50 -k -0.5
echo

mkdir -p resultados/sauvola
run sauvola sonnet sonnet -k 0.08 -R 100
run sauvola retina retina -k -0.5 -R 100
run sauvola wedge wedge -k 0.08 -R 200
run sauvola monarch monarch -k 0.5 -R 300
echo

mkdir -p resultados/phansalkar
run phansalkar retina retina -r 5 -k -0.2 -q 0.5 -p 0.2 -R 4
run phansalkar monarch monarch -r 10 -k 0.9 -q 10 -p 5 -R 0.7
run phansalkar wedge wedge -r 10 -k 0.1 -p 12 -q 16 -R 0.9
echo

mkdir -p resultados/contraste
run contraste baboon baboon -r 50
run contraste sonnet sonnet -r 20
echo

mkdir -p resultados/media
run media fiducial fiducial -r 50
run media wedge wedge -r 50
run media retina retina -r 30
echo

mkdir -p resultados/mediana
run mediana wedge wedge -r 50
run mediana peppers peppers -r 60
