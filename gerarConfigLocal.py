from getpass import getpass
especie=input("Digite a espécie que vai analizar\n")
opcao=input("Configurar envio de Email.\n S ou N?")
if ( opcao=='S' or opcao =='s' ):
	emailServidor=input("email do servidor\n")
	senha=getpass("Senha do servidor")
	emailPessoal=input("Seu email pessoal\n")
elif( opcao=='N' or opcao =='n'):
	print("Ignorando...")
	emailPessoal='null'

else:
	print("opção Inválida")
	print("Ignorando...")
	emailPessoal='null'
remove=input("remover arquivos residuais no fim \n S ou N?")
if remove=='S' or remove=='s':
	remover=True
else:
	remover=False

arquivo=open("./configuracao_local.conf","w")
arquivo.write("/usr/local/RepeatMasker/RepeatMasker -dir . -species {0} -e rmblast -pa\n".format(especie))
if emailPessoal =='null':
	arquivo.write("mail:{0}\n".format(emailPessoal))
else:
	arquivo.write("mail:{0}|{1}|{2}\n".format(emailPessoal,emailServidor,senha))
arquivo.write("#{0}\n".format(remover))
arquivo.close()
input("Precione ENTER para finalizar")