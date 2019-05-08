# -*- coding: utf-8 -*-
from os import system
from datetime import datetime
import os.path
import sys

import modulos
parametros=modulos.config
arquivo=open("./log",'a')
horario=datetime.now().strftime('%d/%m/%y   %H:%M')
arquivo.write('Inicio: '+horario+'\n')
genoma= sys.argv[1]
saida=genoma.replace('.fasta','')
arquivoTab=os.path.exists('./'+saida+".tab")
opcao=0
if (arquivoTab):
	print('arquivo ' +genoma+' tabular já existe \nQuer pular a Análize do RepeatMasker? \n S ou N?')
	opcao=input()

if (opcao == 'n' or opcao ==  'N'):
	numero_proc= input("Digite o Numero de Processadores que Será Usado;\n")
	try:
		system(parametros[0]" "+ numero_proc+" -s "+genoma)
		system("awk -v OFS='\t' '$1=$1' "+genoma+".out > "+saida+".tab")
		system("awk '{ print $10, $11 }' "+saida+".tab > "+saida+"colunasDuplas.tab")
		modulos.enviar_email("Analize Finalizada")
	except:
		print("Ocorreu um ERRO Na Analize do Arquivo: "+genoma)	
		modulos.enviar_email("ERRO na Analize do Arquivo: "+genoma)
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
		modulos.enviar_email("Analize Finalizada")
	except:
		print("Ocorreu um ERRO Na Analize do Arquivo: "+genoma)	
		modulos.enviar_email("ERRO na Analize do Arquivo: "+genoma)
	
	estrutura=modulos.indexar_contar(saida+"colunasDuplas.tab")
	modulos.criar_txt(estrutura,saida)

arquivo.write('Fim: '+horario+'\n')
horario=datetime.now().strftime('%d/%m/%y   %H:%M')
arquivo.close()
