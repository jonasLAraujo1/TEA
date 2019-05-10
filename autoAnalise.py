# -*- coding: utf-8 -*-
from os import system
from datetime import datetime
import os.path
import sys
#definição de cor para erro
VERMELHO   = "\033[1;31m"
NORMAL = "\033[0;0m"
#
import modulos
parametros=modulos.config
arquivo=open("./log",'a')
horario=datetime.now().strftime('%d/%m/%y   %H:%M')
arquivo.write('Inicio: '+horario+'\n')
genoma= sys.argv[1]
if genoma[-3]=="f":
	saida=genoma.replace('.fna','')
elif genoma[-3]=="s":
	saida=genoma.replace('.fasta','')
else:
	print(VERMELHO+"ERRO!\nTipo de Arquivo Inválido\n"+NORMAL)
	exit()
arquivoTab=os.path.exists('./'+saida+".tab")
opcao=0
if (arquivoTab):
	print('arquivo ' +genoma+' tabular já existe \nQuer pular a Análise do RepeatMasker? \n S ou N?')
	opcao=input()

if (opcao == 'n' or opcao ==  'N'):
	numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	try:
		system(parametros[0]" "+ numero_proc+" -s "+genoma)
		system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab")
		system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
		modulos.enviar_email("Analise Finalizada")
	except:
		print(VERMELHO+"ERRO Na Analise do Arquivo: "+genoma+NORMAL)	
		modulos.enviar_email("ERRO na Analise do Arquivo: "+genoma)
		exit()
	estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
	modulos.criar_txt(estrutura,saida)

elif(opcao == 's' or opcao ==  'S'):
	system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
	estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
	modulos.criar_txt(estrutura,saida)

else:
	numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	try:
		system(parametros[0]" "+ numero_proc+" -s "+genoma)
		system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab")
		system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
		modulos.enviar_email("Analise Finalizada")
	except:
		print(VERMELHO+"ERRO Na Analise do Arquivo: "+genoma+NORMAL)	
		modulos.enviar_email("ERRO na Analise do Arquivo: "+genoma)
		exit()
	
	estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
	modulos.criar_txt(estrutura,saida)

arquivo.write('Fim: '+horario+'\n')
horario=datetime.now().strftime('%d/%m/%y   %H:%M')
arquivo.close()
