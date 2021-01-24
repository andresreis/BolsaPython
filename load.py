import pychart as pc
import os
import sys
from PyQt5.QtWidgets import  QApplication
from auxiliar import *
from IG import *

#Nomes de todos os ativos no diretório
dir = 'C:/Users/dreba/Desktop/Livros/Projeto de férias/Bolsa - Python/Data'
ativos_dir = os.listdir(dir)

#Lista com objetos da classe pychart
ativos = []
total = len(ativos_dir)

print("Carregando dados...")
operando = np.load('Operando.npy', allow_pickle = True)
print(operando)
print("Corregando ativos ...")
for at in ativos_dir:
    ativos.append(pc.ativo(at, os.path.basename(dir)))
    if os.path.isfile('Tracos/' + ativos[-1].nome + '.npy'):
        t = np.load('Tracos/' + ativos[-1].nome + '.npy', allow_pickle = True)
        ativos[-1].append_risco(t[0], t[1], t[2], t[3])
    result = np.where(operando[0,:] == ativos[-1].nome)
    if(len(result[0]) > 0):
        if(operando[1,result[0][0]] == '1'):
            ativos[-1].operando = True
    print('(', len(ativos), '/', total, ')',ativos[-1].nome, " carregado!")
print("Iniciando ...")

#Interface gráfica
root = QApplication([])
root.setStyle('Fusion')

app = Window(ativos)
app.show()

sys.exit(root.exec_())
