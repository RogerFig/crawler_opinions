import os

raiz = 'reviews_filmow/'

for pasta in os.listdir(raiz):
        print(pasta + ': ' + str(len(os.listdir(raiz+pasta))))
