# -*- coding: utf-8 -*-
def enviar_email(destinatario,remetente,senha,texto):
  import smtplib
  from  time import sleep as pausa
  
  if destinatario!="null":
    #destinatario = ['jonasaraujo23137@gmail.com']
    assunto      = 'Servidor Remoto Paula'
    msg = '\r\n'.join([
    'From: %s' % remetente,
    'To: %s' % destinatario,
    'Subject: %s' % assunto,
    '',
    '%s' % texto])
    # Enviando o email
    
    while True:
      try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(remetente,senha)
        server.sendmail(remetente, destinatario, msg)
        server.quit()
        break
      except:
        pausa(10)

def organizar_contagem():
  from os import remove
  """ Organiza as contagens das colunas 10 e 11 para trabalhar de forma melhor"""
  arquivo=open('./contagem.txt','r')
  conteudo=arquivo.readlines()
  arquivo.close()
  arquivo=open('./contagemC11.txt','w')
  for linha in conteudo:
    linha=linha.replace("/"," ")
    linha=linha.split()
    if linha[1]!='begin':
      if len(linha) == 3:
          arquivo.write(linha[1]+"\t"+linha[2]+"\t"+linha[0]+"\n")
      else:
        arquivo.write(linha[1]+"\t"+linha[0]+"\n")
  arquivo.close()
  arquivo=open('./contagemC10.txt','w')
  with open("contagem2.txt") as file:
    for linha in file:
      linha=linha.split()
      arquivo.write(linha[1]+"\t"+linha[0]+"\n")
  arquivo.close()
  remove('contagem.txt')
  remove('contagem2.txt')

def indexar(arquivo):
  import pickle #modulo pickle
  classe1={}
  with open(arquivo) as file:
      for linha in file:
          nova=linha.split()
          novaLinha=nova[1].replace("/"," ")
          novaLinha=novaLinha.split()
          if len(novaLinha)==2:
              if novaLinha[0] not in classe1:
                  classe1[novaLinha[0]]={}
                  classe1[novaLinha[0]][novaLinha[1]]=[]
                  classe1[novaLinha[0]][novaLinha[1]].append(nova[0])
              elif novaLinha[1] not in classe1[novaLinha[0]]:
                      classe1[novaLinha[0]][novaLinha[1]]=[]
                      classe1[novaLinha[0]][novaLinha[1]].append(nova[0])
              else:
                  if nova[0] not in classe1[novaLinha[0]][novaLinha[1]]:
                          classe1[novaLinha[0]][novaLinha[1]].append(nova[0])
          else:
              if nova[1] not in classe1:
                  classe1[nova[1]]={}
                  classe1[nova[1]]['Sem Familia '+nova[1]]=[]
                  classe1[nova[1]]['Sem Familia '+nova[1]].append(nova[0])

              elif 'Sem Familia '+nova[1] not in classe1[nova[1]]:                  
                  classe1[nova[1]]['Sem Familia '+nova[1]]=[]
                  classe1[nova[1]]['Sem Familia '+nova[1]].append(nova[0])
              else:
                  if nova[0] not in classe1[nova[1]]['Sem Familia '+nova[1]]:
                      classe1[nova[1]]['Sem Familia '+nova[1]].append(nova[0])
      

  del classe1['position']
  del classe1['begin']
  arquivo = open('referencia.ref','wb') # o "b" significa que o arquivo é binário
  pickle.dump(classe1,arquivo) 
  arquivo.close()
  return classe1

def gerar_valores():
  """ Fazer a contagem geral dos elementos por classe Familia e Subfamilia"""
  classes={}
  duvidoso={}
  duvidosoF={}
  familias={}
  subfamilia={}
  with open("./contagemC11.txt") as file:
    for linha in file:
      linha=linha.split()
      print(linha)
      if len(linha)==3:
        # print(linha[0]+"\n\n")
        if linha[0] not in classes and '?' not in linha[0]:
          # print("Normal Primeiro adicionado")
          classes[linha[0]]=int(linha[2])
          familias[linha[1]]=int(linha[2])
        elif '?' in linha[0] and linha[0][0:-1] not in classes :
          classes[linha[0][0:-1]]=int(linha[2])
          # print("Duvidoso Primeiro adicionado como Normal")
        elif '?' in linha[0]  and linha[0][0:-1] in classes:
          # print("Duvidoso!, Normal já existe, Soma")
          classes[linha[0][0:-1]]=(classes[linha[0][0:-1]]+int(linha[2]))
        else:
          # print("Normal já existe, Soma")
          classes[linha[0]]=(classes[linha[0]]+int(linha[2]))
          familias[linha[1]]=int(linha[2])
        if '?' in linha[0] and linha[0] not in duvidoso:
          duvidoso[linha[0]]=int(linha[2])
          duvidosoF[linha[1]]=int(linha[2])
        elif '?' in linha[0]:
          duvidoso[linha[0]]=(duvidoso[linha[0]]+int(linha[2]))
          duvidosoF[linha[1]]=int(linha[2])
      else:
        if linha[0] not in classes and '?' not in linha[0]:
          # print("Normal Primeiro adicionado")
          classes[linha[0]]=int(linha[1])
        elif '?' in linha[0] and linha[0][0:-1] not in classes :
          classes[linha[0][0:-1]]=int(linha[1])
          # print("Duvidoso Primeiro adicionado como Normal")
        elif '?' in linha[0]  and linha[0][0:-1] in classes:
          # print("Duvidoso!, Normal já existe, Soma")
          classes[linha[0][0:-1]]=(classes[linha[0][0:-1]]+int(linha[1]))
        else:
          # print("Normal já existe, Soma")
          classes[linha[0]]=(classes[linha[0]]+int(linha[1]))
        if '?' in linha[0] and linha[0] not in duvidoso:
          duvidoso[linha[0]]=int(linha[1])
        elif '?' in linha[0]:
          duvidoso[linha[0]]=(duvidoso[linha[0]]+int(linha[1]))

  with open("contagemC10.txt") as file:
    for linha in file:
      linha=linha.split()
      if 'Sem Familia '+str(linha[0]) not in familias:
        familias['Sem Familia '+str(linha[0])]=int(linha[1])
      else:
        familias['Sem Familia '+str(linha[0])]=(familias['Sem Familia '+str(linha[0])]+int(linha[1]))

      subfamilia[linha[0]]=linha[1]

  familias['Sem Familia']=''
  duvidosoF['Sem Familia']=''
  valores=[classes,familias,subfamilia,duvidoso,duvidosoF]
  return valores

def ler_index():
  import pickle
  arquivo = open('referencia.ref','rb')
  dicionario = pickle.load(arquivo)
  arquivo.close()
  return dicionario


def indexar_contar(arquivo):
  import pickle #modulo pickle
  classe1={}
  with open(arquivo) as file:
      for linha in file:
          nova=linha.split()
          novaLinha=nova[1].replace("/"," ")
          novaLinha=novaLinha.split()
          if len(novaLinha)==2:
              if novaLinha[0] not in classe1:
                  classe1[novaLinha[0]]={}
                  classe1[novaLinha[0]][novaLinha[1]]={}
                  classe1[novaLinha[0]][novaLinha[1]][nova[0]]=1
              elif novaLinha[1] not in classe1[novaLinha[0]]:
                      classe1[novaLinha[0]][novaLinha[1]]={}
                      classe1[novaLinha[0]][novaLinha[1]][nova[0]]=1
              else:
                  if nova[0] not in classe1[novaLinha[0]][novaLinha[1]]:
                          classe1[novaLinha[0]][novaLinha[1]][nova[0]]=1
                  else:
                    classe1[novaLinha[0]][novaLinha[1]][nova[0]]+=1
          else:
              if nova[1] not in classe1:
                  classe1[nova[1]]={}
                  classe1[nova[1]]['Sem Familia '+nova[1]]={}
                  classe1[nova[1]]['Sem Familia '+nova[1]][nova[0]]=1

              elif 'Sem Familia '+nova[1] not in classe1[nova[1]]:                  
                  classe1[nova[1]]['Sem Familia '+nova[1]]={}
                  classe1[nova[1]]['Sem Familia '+nova[1]][nova[0]]=1
              else:
                  if nova[0] not in classe1[nova[1]]['Sem Familia '+nova[1]]:
                      classe1[nova[1]]['Sem Familia '+nova[1]][nova[0]]=1
                  else:
                    classe1[nova[1]]['Sem Familia '+nova[1]][nova[0]]+=1


  del classe1['position']
  del classe1['begin']
  for i in classe1:
    for j in classe1[i]:
      somaFamilia=0
      for k in classe1[i][j]:
        somaFamilia+=classe1[i][j][k]
      classe1[i][j]['Total']=somaFamilia
  for i in classe1:
    somaClasse=0
    for j in classe1[i]:
      somaClasse+=classe1[i][j]['Total']
    classe1[i]['Total']=somaClasse

  #arquivo = open('referencia2.ref','wb') # o "b" significa que o arquivo é binário
  #pickle.dump(classe1,arquivo) 
  #arquivo.close()
  return classe1


def criar_xml(dicionario,total,nome_arquivo='saida'):
  #cria documento
  from xml.dom import minidom
  doc = minidom.Document()
  #cria raiz e adicionar no documento
  raiz = doc.createElement('raiz')
  doc.appendChild(doc.createElement('raiz'))

  #cria itens e adiciona na raiz
  classes = doc.createElement('Classes')
  raiz.appendChild(classes)
  for dic_classe in dicionario:
    if dic_classe+'?' in dicionario :
      # print("Normal! existe Duvidoso")
      classe = doc.createElement('classe')
      classe.setAttribute('name', dic_classe)
      classes.appendChild(classe)
      classe.appendChild( doc.createTextNode(str(dic_classe)+' '+str(total[0][dic_classe])))
      # classe.appendChild( doc.createTextNode("valor"))

      duvidoso = doc.createElement('Duvidoso')
      duvidoso.setAttribute('name', dic_classe+'?')
      classe.appendChild(duvidoso)
      duvidoso.appendChild( doc.createTextNode(str(dic_classe+'?')+' '+str(total[3][dic_classe+'?'])))
      
      for dic_familia in dicionario[dic_classe+'?']:
        familia = doc.createElement('familia')
        familia.setAttribute('name', dic_familia)
        duvidoso.appendChild(familia)
        familia.appendChild( doc.createTextNode(str(dic_familia)+' '+str(total[4][dic_familia])))
        for dic_subfamilia in dicionario[dic_classe+'?'][dic_familia]:  
          subfamilia = doc.createElement('Subfamilia')
          subfamilia.setAttribute('name', dic_subfamilia)
          familia.appendChild(subfamilia)
          subfamilia.appendChild( doc.createTextNode(str(dic_subfamilia)+' '+str(total[2][dic_subfamilia])))
      for dic_familia in dicionario[dic_classe]:
        familia = doc.createElement('familia')
        familia.setAttribute('name', dic_familia)
        classe.appendChild(familia)
        familia.appendChild( doc.createTextNode(str(dic_familia)+' '+str(total[1][dic_familia])))
        for dic_subfamilia in dicionario[dic_classe][dic_familia]:  
          subfamilia = doc.createElement('Subfamilia')
          subfamilia.setAttribute('name', dic_subfamilia)
          familia.appendChild(subfamilia)
          subfamilia.appendChild( doc.createTextNode(str(dic_subfamilia)+' '+str(total[2][dic_subfamilia])))

    elif '?' not in dic_classe:
      # print("Duvidoso...\n")
      classe = doc.createElement('classe')
      classe.setAttribute('name', dic_classe)
      # classe.setAttribute('value',10)
      classes.appendChild(classe)
      classe.appendChild( doc.createTextNode(str(dic_classe)+' '+str(total[0][dic_classe])))
      # classe.appendChild( doc.createTextNode("valor"))
      for dic_familia in dicionario[dic_classe]:
        familia = doc.createElement('familia')
        familia.setAttribute('name', dic_familia)
        classe.appendChild(familia)
        familia.appendChild( doc.createTextNode(str(dic_familia)+' '+str(total[1][dic_familia])))
        for dic_subfamilia in dicionario[dic_classe][dic_familia]:  
          subfamilia = doc.createElement('Subfamilia')
          subfamilia.setAttribute('name', dic_subfamilia)
          familia.appendChild(subfamilia)
          subfamilia.appendChild( doc.createTextNode(str(dic_subfamilia)+' '+str(total[2][dic_subfamilia])))
    else:
      pass

  arquivo=open(str(nome_arquivo)+'.xml', 'w')
  arquivo.write(raiz.toprettyxml())
  arquivo.close()    


def criar_txt(dicionario,nome_arquivo='saida'):

  arquivo=open(nome_arquivo+'.txt','w')
  arquivo.writelines('Classe \tFamilia \tSubfamilia\t Valor\n')
  for dic_classe in dicionario:
    #
    if dic_classe != 'Total':
      if dic_classe+'?' in dicionario :
        arquivo.write(str("{}\t\t\t{}\n").format(dic_classe,dicionario[dic_classe]['Total']))
        arquivo.write(str("{}?\t\t\t{}\n").format(dic_classe,dicionario[dic_classe+'?']['Total']))
        #
        for dic_familia in dicionario[str(dic_classe+'?')]:
          if dic_familia!='Total' :
            arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[dic_classe+'?'][dic_familia]['Total']))
            #
            for dic_subfamilia in dicionario[dic_classe+'?'][dic_familia].keys():
              if dic_subfamilia!='Total':
                arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[dic_classe+'?'][dic_familia][dic_subfamilia]))
              #
        for dic_familia in dicionario[dic_classe]:
          if dic_familia !='Total':
            arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[dic_classe][dic_familia]['Total']))
            #
            for dic_subfamilia in dicionario[dic_classe][dic_familia]:
              if dic_subfamilia!='Total':
                arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[dic_classe][dic_familia][dic_subfamilia]))
              #

      elif '?' not in dic_classe:
        if dic_classe !='Total':  
          arquivo.write(str("{}\t\t\t{}\n").format(dic_classe,dicionario[dic_classe]['Total']))
          #
          for dic_familia in dicionario[dic_classe]:
            if dic_familia !='Total':
              arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[dic_classe][dic_familia]['Total']))
              #print(dicionario[dic_classe][dic_familia])
              #
              for dic_subfamilia in dicionario[dic_classe][dic_familia].keys():
                if dic_subfamilia !='Total':
                  arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[dic_classe][dic_familia][dic_subfamilia]))
             #
      else:
        pass
  arquivo.close()
def criar_txt2(dicionario,nome_arquivo='saida'):

	arquivo=open(nome_arquivo+'.txt','w')
	prioridade=("LINE","SINE","LTR","Retroposon","DNA","Unknown")
	arquivo.writelines('Classe \tFamilia \tSubfamilia\t Valor\n')
	for classe_p in prioridade:
		if classe_p in dicionario:
			arquivo.write(str("{}\t\t\t{}\n").format(classe_p,dicionario[classe_p]['Total']))
			for dic_familia in dicionario[classe_p]:
				if dic_familia !='Total':
					arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[classe_p][dic_familia]['Total']))
					#
					for dic_subfamilia in dicionario[classe_p][dic_familia]:
						if dic_subfamilia!='Total':
							arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[classe_p][dic_familia][dic_subfamilia]))
			if classe_p+'?' in dicionario:
				arquivo.write(str("{}\t\t\t{}\n").format(classe_p+'?',dicionario[classe_p+'?']['Total']))
				for dic_familia in dicionario[classe_p+'?']:
					if dic_familia !='Total':
						arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[classe_p+'?'][dic_familia]['Total']))
						#
						for dic_subfamilia in dicionario[classe_p+'?'][dic_familia]:
							if dic_subfamilia!='Total':
								arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[classe_p+'?'][dic_familia][dic_subfamilia]))


	for dic_classe in dicionario:
		if dic_classe != 'Total' and dic_classe not in prioridade:
			if dic_classe+'?' in dicionario:
				arquivo.write(str("{}\t\t\t{}\n").format(dic_classe,dicionario[dic_classe]['Total']))
				for dic_familia in dicionario[dic_classe]:
					if dic_familia !='Total':
						arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[dic_classe][dic_familia]['Total']))

						for dic_subfamilia in dicionario[dic_classe][dic_familia]:
							if dic_subfamilia!='Total':
								arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[dic_classe][dic_familia][dic_subfamilia]))
			  
				arquivo.write(str("{}?\t\t\t{}\n").format(dic_classe,dicionario[dic_classe+'?']['Total']))
				for dic_familia in dicionario[str(dic_classe+'?')]:
					if dic_familia!='Total' :
						arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[dic_classe+'?'][dic_familia]['Total']))
						for dic_subfamilia in dicionario[dic_classe+'?'][dic_familia].keys():
							if dic_subfamilia!='Total':
								arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[dic_classe+'?'][dic_familia][dic_subfamilia]))

			elif '?' not in dic_classe :
				if dic_classe !='Total':
					arquivo.write(str("{}\t\t\t{}\n").format(dic_classe,dicionario[dic_classe]['Total']))
					for dic_familia in dicionario[dic_classe]:
						if dic_familia !='Total':
							arquivo.write(str("\t{}\t\t{}\n").format(dic_familia,dicionario[dic_classe][dic_familia]['Total']))
							for dic_subfamilia in dicionario[dic_classe][dic_familia].keys():
								if dic_subfamilia !='Total':
									arquivo.write(str("\t\t{}\t{}\n").format(dic_subfamilia,dicionario[dic_classe][dic_familia][dic_subfamilia]))
			else:
				pass


	arquivo.close()

# ler_index()
def carregarConfig(localExecute):
  import os
  if(os.path.exists("./configuracao_local.conf")):
    localExecute="./configuracao_local.conf"
    arquivo_conf=(open(localExecute))
  
  else:
    localExecute=localExecute.replace("/main.py","/")
    arquivo_conf=(open(localExecute+"configuracao.conf"))
  configuracoes={}
  for linha in arquivo_conf.readlines():
    if "RepeatMasker" in linha:
      configuracoes["programa"]=linha.replace("\n","")
    elif "mail:" in linha:
      configuracoes['email']=[]
      for sub in linha.replace("mail:","").split("|"):
        configuracoes['email'].append(sub.replace("\n",""))
    elif "#" in linha:
      configuracoes["residuos"]=linha.replace("#","").replace("\n","")
      configuracoes["residuos"]=bool(configuracoes["residuos"])
    else:
      pass
  return configuracoes

def removeLixo(prefixo,remover):
  from os import remove
  import os
  if (remover='True'):
    listaRemover=["colunasDuplas.tab",".fna.alert",".fna.cat",".fna.masked",".fna.out"]
    for arquvivo in listaRemover:
      if (os.path.exists(prefixo+arquvivo)):
        remove(prefixo+arquvivo)
      else:
        pass
    
