import csv
import numpy as np
import mplfinance as mpf

import pandas as pd
from auxiliar import *

class ativo:
    def __init__(self, nome_do_ativo, pasta):
        with open(pasta + '/' + nome_do_ativo, newline='') as csvfile:
            raw_data = csv.reader(csvfile, delimiter=';', quotechar='|')

            self.list = np.flipud(np.char.replace(np.array(list(raw_data)), ',', '.'))
            self.nome = self.list[0][0]

            #0-data 1-hora 2-abertura 3-maxima 4-minima 5-fechamento 6-volume_f 7-volume_q
            self.dados_60 = [self.list[:,1],
                             self.list[:,2],
                             self.list[:,3].astype(np.float),
                             self.list[:,4].astype(np.float),
                             self.list[:,5].astype(np.float),
                             self.list[:,6].astype(np.float),
                             self.list[:,7].astype(np.float),
                             self.list[:,8].astype(np.float)]
            self.tf_60 = topos_fundos(self.dados_60[3].T, self.dados_60[4].T, ultimo = True)
            self.tf_60_list = topos_fundos_list(self.tf_60)
            self.tf_60_rel = checar_topos_fundos_60(self.tf_60)
            self.tf_60_iso = topos_fundos(self.dados_60[3].T, self.dados_60[4].T, lista = True, ultimo = True)

            self.dados_d = dados_diarios(self.dados_60)
            self.media_d_17 = media_movel(self.dados_d[5], 17)
            self.media_d_72 = media_movel(self.dados_d[5], 72)
            self.pos_medias_d = pos_medias(self.media_d_17, self.media_d_72, self.dados_d[5][-1])
            self.tf_d = topos_fundos(self.dados_d[3].T, self.dados_d[4].T)
            self.tf_d_list = topos_fundos_list(self.tf_d)
            self.tf_d_rel = checar_topos_fundos(self.tf_d)

            self.dados_s = dados_semanais(self.dados_d)
            self.media_s_72 = media_movel(self.dados_s[5], 72)
            self.pos_media_s = pos_media(self.media_s_72, self.dados_d[5][-1])

            self.linhas = []

            self.operando = False

    def candle_60(self, dias=150):
        #dias = len(self.dados_60[2])
        data = np.stack((self.dados_60[2].T[-dias:],
                         self.dados_60[3].T[-dias:],
                         self.dados_60[4].T[-dias:],
                         self.dados_60[5].T[-dias:],
                         self.dados_60[6].T[-dias:]),
                        axis=1)
        tempo = pd.to_datetime(np.core.defchararray.add(np.char.add(self.dados_60[0][-dias:],' '), self.dados_60[1][-dias:]).T, dayfirst=True)
        ohlc = pd.DataFrame(data=data, index = tempo, columns=['Open', 'High', 'Low', 'Close','Volume'])
        ohlc.index.name = 'Date'

        #Topos e fundos
        #apdict = mpf.make_addplot(self.tf_60[-dias:],type='scatter')
        adp = [mpf.make_addplot(self.tf_60_list[-dias:],type='line', color='blue')]#,
               #mpf.make_addplot(self.media_60_17[-dias:],type='line', color='pink')]

        x = mpf.plot(ohlc, returnfig = True, block=True, type='candle', style='yahoo', addplot = adp, title= '\n' + self.nome + ': 60 min')

        return x

    def candle_d(self, dias=150):

        data = np.stack((self.dados_d[2].T[-dias:],
                         self.dados_d[3].T[-dias:],
                         self.dados_d[4].T[-dias:],
                         self.dados_d[5].T[-dias:],
                         self.dados_d[6].T[-dias:]),
                        axis=1)
        tempo = pd.to_datetime(self.dados_d[0][-dias:].T, dayfirst=True)

        ohlc = pd.DataFrame(data=data, index = tempo, columns=['Open', 'High', 'Low', 'Close','Volume'])
        ohlc.index.name = 'Date'

        adp = [mpf.make_addplot(self.tf_d_list[-dias:],type='line', color='black'),
               mpf.make_addplot(self.media_d_17[-dias:],type='line', color='orange'),
               mpf.make_addplot(self.media_d_72[-dias:],type='line', color='blue')]

        for i in range(len(self.linhas)):
            adp.append(mpf.make_addplot(self.linhas[i][-dias:],type='line', color='red'))

        x = mpf.plot(ohlc, returnfig = True, block=True, type='candle', style='yahoo', addplot = adp, title= '\n' + self.nome + ': diário')
        return x

    def candle_s(self, dias=30):
        if(len(self.dados_s)<dias):
            dias = len(self.media_s_72)
        data = np.stack((self.dados_s[2].T[-dias:],
                         self.dados_s[3].T[-dias:],
                         self.dados_s[4].T[-dias:],
                         self.dados_s[5].T[-dias:],
                         self.dados_s[6].T[-dias:]),
                        axis=1)
        tempo = pd.to_datetime(self.dados_s[0][-dias:].T, dayfirst=True)

        ohlc = pd.DataFrame(data=data, index = tempo, columns=['Open', 'High', 'Low', 'Close','Volume'])
        ohlc.index.name = 'Date'

        #apdict = mpf.make_addplot(self.tf_s_list[-dias:],type='line', color='black')
        adp = [#mpf.make_addplot(self.tf_d_list[-dias:],type='line', color='black')]#,
               mpf.make_addplot(self.media_s_72[-dias:],type='line', color='blue')]

        x = mpf.plot(ohlc, returnfig = True, block=True, type='candle', style='yahoo', addplot = adp, title= '\n' + self.nome + ': semanal')#, addplot = apdict)
        return x

    def append_risco(self, x1, x2, y1, y2):
        self.linhas.append(criar_risco(x1, x2, y1, y2, len(self.dados_d[0][:])))

    def relatorio(self, formatado = False):
        if formatado:
            return[self.nome, self.pos_medias_d, self.pos_media_s, self.tf_d_rel]#, self.tf_60_rel[0], str(round(self.tf_60_rel[1],2))]
                   #, self.corr_das_medias[0], self.corr_das_medias[1]]
        print("Ativo: ", self.nome)
        print("Diário (médias) :", self.pos_medias_d)
        print("Semanal (média) :", self.pos_media_s)
        print("Topos e fundos diário: ", self.tf_d_rel)
