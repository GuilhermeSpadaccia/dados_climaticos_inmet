import pandas as pd
import os
import re

# fonte das funções dms2dd e parse_dms: https://en.proft.me/2015/09/20/converting-latitude-and-longitude-decimal-values-p/
def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd;

def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms)
    coord = dms2dd(parts[0], parts[1], parts[2], parts[3])
    return (coord)

def getCoordinates(df):
    latitudeDMS = df.iloc[5]['Unnamed: 1']
    longitudeDMS = df.iloc[6]['Unnamed: 1']

    latitudeDD = parse_dms(latitudeDMS[:len(latitudeDMS)-1]+"0'"+latitudeDMS[len(latitudeDMS)-1:len(latitudeDMS)])
    longitudeDD = parse_dms(longitudeDMS[:len(longitudeDMS)-1]+"0'"+longitudeDMS[len(longitudeDMS)-1:len(longitudeDMS)])

    return(latitudeDD, longitudeDD)

def getInfosFromName(filename):
    filename = filename.replace('.xls','')
    filenamesplited = filename.split('_')
    filenamesplited = list(filter(None, filenamesplited))
    
    estado = filenamesplited[0]
    del filenamesplited[0]
    
    codigo = filenamesplited[0]
    del filenamesplited[0]
    
    cidade = ' '.join(filenamesplited)

    return estado, codigo, cidade

def fixDF(df):
    df = df.unstack()
    df = df.reset_index()
    df.columns = ['objeto', 'hora', 'data', 'valor']
    df = df.sort_values(by=['objeto','data','hora'])
    df = pd.pivot_table(df, index=['data','hora'], columns='objeto', values='valor')
    df = df.reset_index()
    df['hora'] = df['hora'].astype('int')/100
    df['latitude'] = lat
    df['longitude'] = lon
    df['codigo'] = codigo
    df['estado'] = estado
    df['cidade'] = cidade
    
    return df

files_list = []
for (dirpath, dirnames, filenames) in os.walk('Dados Climaticos'):
    if len(filenames) > 0:
        for file in filenames:
            if file[len(file)-5:len(file)-4] == '_':
                continue
            else:
                files_list.append(dirpath + '/' + file)

        
for file in files_list:
    
    estado, codigo, cidade = getInfosFromName(file.split('/')[-1])

    df = pd.read_excel(file, nrows=9, usecols='A:B')
    lat, lon = getCoordinates(df)

    print(estado)
    print(codigo)
    print(cidade)
    print(lat, lon)
    print('-----------------')

    # Como os dados estão divididos em duas planilhas faço a leitura das duas e por fim as concateno
    df1 = pd.read_excel(file, skiprows=9, header=[0,1], usecols='A:HI')
    df1 = fixDF(df1)
    df1.columns = ['data', 'hora','temp_media','temp_ponto_orvalho_media', 'temp_maxima',
       'temp_minima','temp_ponto_orvalho_maxima','temp_ponto_orvalho_minima','umidade_relativa',
       'umidade_relativa_maxima','umidade_relativa_minima','latitude','longitude','codigo','estado', 'cidade']

    file = file.replace('.xls','_.xls')

    df2 = pd.read_excel(file, skiprows=9, header=[0,1], usecols='A:GA')
    df2 = fixDF(df2)
    df2 = df2.drop(['latitude', 'longitude', 'codigo', 'estado','cidade', 'data', 'hora'], axis=1)
    df2.columns = ['precipitacao', 'pressao_atm_med','pressao_atm_max', 'pressao_atm_min',
                   'radiacao', 'velocidade_vento','direcao_vento', 'vento_rajada_maxima']

    final_df = pd.concat([df1, df2], axis=1)

    print(final_df)
