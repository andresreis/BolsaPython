import numpy as np
import pandas as pd

def topos_fundos(high,low, lista = False, ultimo = True):

    possiveis_topos = [high[0]]       #Valor
    possiveis_fundos = [low[0]]       #Valor

    possiveis_fundos.append(np.nan)
    possiveis_topos.append(np.nan)
    i = 2
    while(i<len(high)-2):
        if ((high[i] >= high[i-1]) and (high[i] >= high[i-2]) and (high[i] >= high[i+1]) and (high[i] >= high[i+2])):
            possiveis_topos.append(high[i])
        else:
            possiveis_topos.append(np.nan)
        if ((low[i] <= low[i-1]) and (low[i] <= low[i-2]) and (low[i] <= low[i+1]) and (low[i] <= low[i+2])):
            possiveis_fundos.append(low[i])
        else:
            possiveis_fundos.append(np.nan)
        i += 1

    possiveis_fundos.append(np.nan)
    possiveis_fundos.append(np.nan)
    possiveis_topos.append(np.nan)
    possiveis_topos.append(np.nan)

    ultimo_fundo = True

    topos_analisados = [0,0]
    topos_analisados_index = [-1,-1]

    fundos_analisados = [0,0]
    fundos_analisados_index = [-1,-1]

    topos = []
    topos_index = []

    fundos = [possiveis_fundos[0]]
    fundos_index = [0]

    for i in range(len(high)):
        if (ultimo_fundo == True):
            if (np.isnan(possiveis_topos[i]) == False):
                if ((topos_analisados[0] == 0) and (fundos_index[-1] != i)):
                    topos_analisados[0] = possiveis_topos[i]
                    topos_analisados_index[0] = i
                if((fundos_analisados[0] == 0) and (possiveis_topos[i] > topos_analisados[0])):
                    topos_analisados[0] = possiveis_topos[i]
                    topos_analisados_index[0] = i
                if ((fundos_analisados[0] != 0) and (fundos_analisados_index[0] != i)):
                    if(possiveis_topos[i] <= topos_analisados[0]):
                        if (i - topos_analisados_index[0] >= 17):
                            ultimo_fundo = False
                            topos.append(topos_analisados[0])
                            topos_index.append(topos_analisados_index[0])
                            topos_analisados[0] = possiveis_topos[i]
                            topos_analisados_index[0] = i

                    else:
                        y = topos_analisados[0]
                        b = fundos_analisados[0]
                        rompimento = 0
                        if((i-fundos_analisados_index[0] != 0) and (possiveis_topos[i] - fundos_analisados[0] != 0)):
                            a = (possiveis_topos[i] - fundos_analisados[0])/(i-fundos_analisados_index[0])
                            rompimento = ((y-b)/a)+fundos_analisados_index[0]-topos_analisados_index[0]

                        if (rompimento < 17):
                        #Não tá entrando aqui
                            topos_analisados[0] = possiveis_topos[i]
                            topos_analisados_index[0] = i
                            fundos_analisados[0] = 0
                            fundos_analisados_index[0] = -1
                        else:
                            ultimo_fundo = False
                            topos.append(topos_analisados[0])
                            topos_index.append(topos_analisados_index[0])
                            topos_analisados[0] = possiveis_topos[i]
                            topos_analisados_index[0] = i

            if (np.isnan(possiveis_fundos[i]) == False):
                if ((topos_analisados[0] != 0)  and (topos_analisados_index[0] != i)):
                    if (fundos_analisados[0] == 0):
                    #and (possiveis_fundos[i] < fundos_analisados[0])
                        if ((possiveis_fundos[i] >= fundos[-1]) and (i - fundos_index[-1] >= 17)):
                            fundos_analisados[0] = possiveis_fundos[i]
                            fundos_analisados_index[0] = i

                        if (possiveis_fundos[i] < fundos[-1]):
                    #ax + b = y
                            y = fundos[-1]
                            b = topos_analisados[0]
                            rompimento = 0
                            if((i-topos_analisados_index[0] != 0) and (possiveis_fundos[i] - topos_analisados[0] != 0)):
                                a = (possiveis_fundos[i] - topos_analisados[0])/(i-topos_analisados_index[0])
                                rompimento = ((y-b)/a) + topos_analisados_index[0] - fundos_index[-1]

                            if(rompimento >= 17):
                                fundos_analisados[0] = possiveis_fundos[i]
                                fundos_analisados_index[0] = i
                    elif(possiveis_fundos[i] <= fundos_analisados[0]):
                        fundos_analisados[0] = possiveis_fundos[i]
                        fundos_analisados_index[0] = i

        if(ultimo_fundo == False):
            if (np.isnan(possiveis_fundos[i]) == False):
                if (fundos_analisados[0] == 0):
                    fundos_analisados[0] = possiveis_fundos[i]
                    fundos_analisados_index[0] = i
                if((topos_analisados[0] == 0) and (possiveis_fundos[i] < fundos_analisados[0])):
                    fundos_analisados[0] = possiveis_fundos[i]
                    fundos_analisados_index[0] = i
                if ((topos_analisados[0] != 0) and topos_analisados_index[0] != i):
                    if(possiveis_fundos[i] >= fundos_analisados[0]):
                        if (i - fundos_analisados_index[0] >= 17):
                            ultimo_fundo = True
                            fundos.append(fundos_analisados[0])
                            fundos_index.append(fundos_analisados_index[0])
                            fundos_analisados[0] = possiveis_fundos[i]
                            fundos_analisados_index[0] = i

                    else:
                        y = fundos_analisados[0]
                        b = topos_analisados[0]
                        rompimento = 0
                        if((i-topos_analisados_index[0] != 0) and (possiveis_fundos[i] - topos_analisados[0] != 0)):
                            a = (possiveis_fundos[i] - topos_analisados[0])/(i-topos_analisados_index[0])
                            #ax + b = y
                            rompimento = ((y-b)/a)+topos_analisados_index[0]-fundos_analisados_index[0]

                        if (rompimento < 17):
                        #Não tá entrando aqui
                            fundos_analisados[0] = possiveis_fundos[i]
                            fundos_analisados_index[0] = i
                            topos_analisados[0] = 0
                            topos_analisados_index[0] = -1
                        else:
                        ##print(possiveis_topos[i])
                            ultimo_fundo = True
                            fundos.append(fundos_analisados[0])
                            fundos_index.append(fundos_analisados_index[0])
                            fundos_analisados[0] = possiveis_fundos[i]
                            fundos_analisados_index[0] = i

            if (np.isnan(possiveis_topos[i]) == False):
                if ((fundos_analisados[0] != 0) and (fundos_analisados_index[0] != i)):
                    if (topos_analisados[0] == 0):

                        if ((possiveis_topos[i] <= topos[-1]) and (i - topos_index[-1] >= 17)):
                            topos_analisados[0] = possiveis_topos[i]
                            topos_analisados_index[0] = i

                        if (possiveis_topos[i] > topos[-1]):
                            #ax + b = y
                            y = topos[-1]
                            b = fundos_analisados[0]
                            rompimento = 0
                            if((i-fundos_analisados_index[0] != 0) and (possiveis_topos[i] - fundos_analisados[0] != 0)):
                                a = (possiveis_topos[i] - fundos_analisados[0])/(i-fundos_analisados_index[0])
                                rompimento = ((y-b)/a) + fundos_analisados_index[0] - topos_index[-1]

                            if(rompimento >= 17):
                                topos_analisados[0] = possiveis_topos[i]
                                topos_analisados_index[0] = i
                    elif(possiveis_topos[i] >= topos_analisados[0]):
                        topos_analisados[0] = possiveis_topos[i]
                        topos_analisados_index[0] = i

    if (ultimo == True):
        if ultimo_fundo:
            topos.append(topos_analisados[0])
            topos_index.append(topos_analisados_index[0])
        else:
            fundos.append(fundos_analisados[0])
            fundos_index.append(fundos_analisados_index[0])

    if(lista):
        return [topos, fundos]

    topos_dataframe = []
    j = 0
    fundos_dataframe = []
    k = 0

    for i in range(len(high)):
        if ((j < len(topos_index) and (topos_index[j] == i))):
            topos_dataframe.append(topos[j])
            j += 1
        else:
            topos_dataframe.append(np.nan)

        if ((k < len(fundos_index)) and (fundos_index[k] == i)):
            fundos_dataframe.append(fundos[k])
            k += 1
        else:
            fundos_dataframe.append(np.nan)

    data = {'a': topos_dataframe, 'b':fundos_dataframe}

    return pd.DataFrame(data = data)

def nan_helper(y):

    return np.isnan(y), lambda z: z.nonzero()[0]

def topos_fundos_list(df):
    a = np.array(df[:]['a'].values.tolist())
    b = np.array(df[:]['b'].values.tolist())
    c = []

    for i in range (len(a)):
        if(np.isnan(a[i]) == False):
            c.append(a[i])
        elif(np.isnan(b[i]) == False):
            c.append(b[i])
        else:
            c.append(np.nan)
    c = np.array(c)

    nans, x = nan_helper(c)
    c[nans] = np.interp(x(nans), x(~nans), c[~nans])

    i = 1
    while(np.isnan(a[-i]) and np.isnan(b[-i])):
        c[-i] = np.nan
        i+=1

    return c

def dados_diarios(lista):
    #0-data 1-hora 2-abertura 3-maxima 4-minima 5-fechamento 6-volume_f 7-volume_q
    dia = [lista[0][0]]
    maxima = [lista[3][0]]
    minima = [lista[4][0]]
    abertura = [lista[2][0]]
    fechamento = []
    volume_f = [lista[6][0]]
    volume_q = [lista[7][0]]

    for i in range(len(lista[0])-1):
        if(lista[0][i+1] == dia[-1]):
            if (lista[3][i+1]>maxima[-1]):
                maxima[-1] = lista[3][i+1]
            if (lista[4][i+1]<minima[-1]):
                minima[-1] = lista[4][i+1]
            volume_f[-1] += lista[6][i+1]
            volume_q[-1] += lista[7][i+1]
        else:
            abertura.append(lista[2][i+1])
            fechamento.append(lista[5][i])
            dia.append(lista[0][i+1])
            maxima.append(lista[3][i+1])
            minima.append(lista[4][i+1])
            volume_f.append(lista[6][i+1])
            volume_q.append(lista[7][i+1])
    fechamento.append(lista[5

                             ][-1])

    return [np.array(dia), np.zeros(len(dia)), np.array(abertura),
            np.array(maxima), np.array(minima), np.array(fechamento),
            np.array(volume_f), np.array(volume_q)]

def dados_semanais(lista):
    #0-data 1-hora 2-abertura 3-maxima 4-minima 5-fechamento 6-volume_f 7-volume_q
    semana = pd.to_datetime(lista[0][0], dayfirst=True).weekday()
    dia = [lista[0][0]]
    maxima = [lista[3][0]]
    minima = [lista[4][0]]
    abertura = [lista[2][0]]
    fechamento = []
    volume_f = [lista[6][0]]
    volume_q = [lista[7][0]]

    for i in range(len(lista[0])-1):
        if(pd.to_datetime(lista[0][i+1], dayfirst=True).weekday()>semana):
            if (lista[3][i+1]>maxima[-1]):
                maxima[-1] = lista[3][i+1]
            if (lista[4][i+1]<minima[-1]):
                minima[-1] = lista[4][i+1]
            volume_f[-1] += lista[6][i+1]
            volume_q[-1] += lista[7][i+1]

        else:
            abertura.append(lista[2][i+1])
            fechamento.append(lista[5][i])
            dia.append(lista[0][i+1])
            maxima.append(lista[3][i+1])
            minima.append(lista[4][i+1])
            volume_f.append(lista[6][i+1])
            volume_q.append(lista[7][i+1])
        semana = pd.to_datetime(lista[0][i+1], dayfirst=True).weekday()
    fechamento.append(lista[5][-1])

    return [np.array(dia), np.zeros(len(dia)), np.array(abertura),
            np.array(maxima), np.array(minima), np.array(fechamento),
            np.array(volume_f), np.array(volume_q)]

def media_movel(data_set, periods=3):
    weights = np.ones(periods) / periods
    return np.convolve(data_set, weights, mode='valid')

def pos_medias(media1, media2, fechamento):
    if (media1[-1]>media2[-1]):
        cima = media1[-1]*1.01
        baixo = media2[-1]*0.99
    else:
        cima = media2[-1]*1.01
        baixo = media1[-1]*0.99

    if (fechamento>cima):
        return 'Acima'
    elif(fechamento>=baixo):
        return 'Proximo'
    else:
        return 'Abaixo'

def pos_media(media, fechamento):
    if (media[-1]>fechamento):
        return 'Abaixo'
    else:
        return 'Acima'

def checar_topos_fundos(data):
    a = np.array(data[:]['a'].values.tolist())
    b = np.array(data[:]['b'].values.tolist())
    i = len(a)-1
    j = 0
    t = []
    f = []
    #return "Teste"
    while((j<4) and (i > 0)):
        if(np.isnan(a[i]) == False):
            t.append(a[i])
            j+=1
        elif(np.isnan(b[i]) == False):
            f.append(b[i])
            j+=1
        i-=1

    if (j==4):
        if (t[0]<t[1] and f[0]<f[1]):
            return "Tps e fds desc"
        if (t[0]>t[1] and f[0]>f[1]):
            return "Tps e fds asc"
        if (t[0]<t[1] and f[0]>f[1]):
            return "Fechando"
        if (t[0]>t[1] and f[0]<f[1]):
            return "Abrindo"
    else:
        return "Insuficiente"

def checar_topos_fundos_60(data):
    a = np.array(data[:]['a'].values.tolist())
    b = np.array(data[:]['b'].values.tolist())
    i = len(a)-1
    j = 0
    t = []
    f = []

    while(j<3):
        if(np.isnan(a[i]) == False):
            t.append(a[i])
            j+=1
        elif(np.isnan(b[i]) == False):
            f.append(b[i])
            j+=1
        i-=1

    if((len(f)==2) and (f[0]>f[1])):
        por = (t[0]-f[0])/t[0]
        por *= 100
        return ['Fds asc', por]
    elif((len(t)==2) and (t[0]<t[1])):
        por = (t[0]-f[0])/f[0]
        por *= 100
        return ['Tps desc', por]
    else:
        return['Esperar', 0]

def gerar_relatorio(ativos):
    rel = []
    for at in ativos:
        rel.append(at.relatorio(formatado = True))
    rel = np.array(rel)
    #self.nome, self.pos_medias_d, self.pos_media_s, self.tf_d_rel, self.tf_60_rel[0], self.tf_60_rel[1]
    rel = pd.DataFrame(data=rel, columns=['Ativo', 'Médias D', 'Média S', 'Tps e Fds D'])

def criar_risco(x1, x2, y1, y2, tam):
    if (x1 > x2):
        temp = x1
        x1 = x2
        x2 = temp
        temp = y1
        y1 = y2
        y2 = temp
    lista = np.full(tam, np.nan)
    a = (y2-y1)/(x2-x1)
    b = y1
    i = int(x1)
    while(i < x2):
        lista[i] = a*(i-x1) + b
        i += 1
    return lista
#Inativo
def checar_corr_das_meias(obj):

    if (obj.pos_medias_d == 'Proximo' and
        obj.pos_media_s == 'Acima' and
        obj.tf_d_rel == 'Tps e fds asc' and
        obj.tf_60_rel[0] == 'Fds asc' and
        obj.tf_60_rel[1] <= 8):
        return ['Comprar', [obj.tf_60_iso[0][-1], obj.tf_60_iso[1][-1]]]
    elif(obj.pos_medias_d == 'Proximo' and
        obj.pos_media_s == 'Abaixo' and
        obj.tf_d_rel == 'Tps e fds desc' and
        obj.tf_60_rel[0] == 'Tps desc' and
        obj.tf_60_rel[1] <= 8):
        return ['Vender', 'Calcular Pontos']
    else:
        return ['Esperar', ' ']
