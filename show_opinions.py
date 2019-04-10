import os

raiz = 'reviews/'

for pasta in os.listdir(raiz):
        print(pasta + ': ' + str(len(os.listdir(raiz+pasta))))
