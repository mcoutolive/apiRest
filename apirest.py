import requests
from requests.auth import HTTPBaiscAuth
from datetime import date, timedelta, datetime
import pandas as pd
import xlswriter
from getpass import getpass
import re
import pdb

#projeto voltado para manipulacao de dados de portal de acompanhamento de mudancas e incidentes e coonstrucao de um dataframe para analise e manipulacao de dados
def metodoGet1(url, user, senha):
    response = requests.request('GET',url,verify=False,auth=HTTPBasicAuth(user,senha))
    conteudoMember = response.json()['member']
    tipomud = ['MUD-CORRETIVA','MUD-OFENSORA']
    mudancas = []
    for inc in conteudoMember:
        if inc.get('relatedrecord'):
            listmud = inc.get('relatedrecord')
            for mud in listmud:
                for j in tipomud:
                    if j == str(mud.get('itau_tipomud')):
                        conteudo = {'ID':inc.get('ticketid'),'Mudanca Relacionada':mud.get('relatedrecwonum'),
                        'Tipo de Mudanca':mud.get('itau_tipomud'),'Titulo':inc.get('description'),
                        'Prioridade Interna':inc.get('internalpriority')}
                        mudancas.append(conteudo)
    df = pd.DataFrame(mudancas)
    return df

def metodoGet2(url, user, senha):
    response = requests.request('GET', url, verify=False, auth=HTTPBasicAuth(user, senha))
    conteudoMember = response.json()['member']
    return conteudoMember

def dfInc(conteudoMember):
    df = pd.DataFrame(conteudoMember)
    return df

def dfMud(conteudoMember):
    df = pd.DataFrame(conteudoMember)
    df = pd.concat([df['wonum'],df['schedstart'],df['schedfinish'],df['itau_celulagovernanca'],df['description'],df['status_description']],axis=1)
    df = df.reindex(columns=['wonum','schedstart','schedfinish','itau_celulagovernanca','description','status_description'])
    df.columns = ['ID','Inicio Programado','Termino Programado','Celula','Titulo','Status']
    
#recomenda-se sempre a insercao de senahs criptografadas
user = ''
senha = ''

today = str(date.today())
yesterday = str(date.today() - timedelta(days=1))
t1 = str(date.today() - timedelta(days=3))
t2 = str(date.today() - timedelta(days=3))
now = datetime.now()
time = (now.strftime("%Hh%M"))
nameExcel = 'Incidentes e Mudancas Relacionadas ' + today + '' + time + '.xlsx'

url = 'insira aqui a sua url de teste'
