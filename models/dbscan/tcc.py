# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.cluster import DBSCAN as DensityBasedSpatialClustering

from lixeira import preProcessamento2

dfHeader = ['estado', 'cidade', 'tipo', 'objeto', 'aspectos']
filename = '../../input/dataset_100.csv'
df = pd.read_csv(filename, delimiter=';', names=dfHeader)

def DBSCAN(conjunto_de_dados, eps, minPts):
    dbscan = DensityBasedSpatialClustering(eps=eps, min_samples=minPts)
    dbscan.fit(conjunto_de_dados)

    return dbscan.labels_, dbscan.core_sample_indices_

def processarDBSCAN(subset, eps, minPts):
    visualizacao = []
    visualizacao.append(['Nó', 'Pai', 'Centróide'])
    visualizacao.append(['core', None, 0])

    dfSubconjunto = subset
    setCaracteristicas = preProcessamento2.extrairCaracteristicas(dfSubconjunto)
    listSubconjuntoTransformado = preProcessamento2.processarPonderacaoBinaria(setCaracteristicas, dfSubconjunto)
    resultado, core_points_index = DBSCAN(listSubconjuntoTransformado, eps, minPts)

    # centroides = []

    for point_index in core_points_index:
        linhaGrupo = [str(point_index), 'core', 0]
        visualizacao.append(linhaGrupo)
        sample_indexes = np.where(resultado == resultado[point_index]) #recuperar indices das amostras do grupo do core point
        df_samples = pd.DataFrame(listSubconjuntoTransformado) #transformar em DataFrame
        df_samples = df_samples.loc[sample_indexes] #recuperar amostras do grupo do core point através dos índices

        for aspecto, column in zip(list(setCaracteristicas), df_samples):
            centroide = df_samples[column].mean()
            linhaAspecto = [aspecto + ' (g' + str(point_index) + ')', str(point_index), centroide];
            visualizacao.append(linhaAspecto)

    print visualizacao

processarDBSCAN(df, 2, 2)