# legendary-computing-machine
Projekt nr 2. Analiza krawędzi


W programie użyte są biblioteki numpy, matplotlib, PIL oraz sys.

Analiza wykonana za pomocą metody operatorów Sobela.
https://en.wikipedia.org/wiki/Sobel_operator
https://setosa.io/ev/image-kernels/
Każdy pixel ma stowarzyszony z nim gradient[Gx,Gy], którego nachylenie można obliczyć.
Uznaję, że pixel jest elementem krawędzi jeśli pierwiastek z sumy kwadratów Gx oraz Gy przekroczy wartość threshold=70.
Jeśli pixel jest elementem krawędzi, to ma wartość 255, w przeciwnym razie ma wartość 0.
Z nachylenia można otrzymać za pomocą arcustangensa kąt.
Wykres orientacji krawędzi tworzę licząc liczbę pixeli o kącie w przedziale, przy czym pixele są liczone tylko tam gdzie jest
wykryta krawędź.
