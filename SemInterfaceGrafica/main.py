import os
import platform
import mysql.connector


#Aqui informe o endereco do banco de dados mysql local ou na nuvem
dados_conexao = {"user": "root", "password": "Hermelio@123",
                 "host": "127.0.0.1", "database": "agenda"}


def limpar_tela():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def sair():
    print("Obrigado por utilizar o sistema!")
    os._exit(0)


def mensagem_menu_principal():
    limpar_tela()
    print("**************************************************")
    print("*        BEM-VINDO AO SISTEMA DE CADASTRO        *")
    print("*------------------------------------------------*")
    print("*       ESCOLHA UMA DAS OPÇÕES DISPONÍVEIS       *")
    print("*           1 - CADASTRAR UM CONTATO             *")
    print("*           2 - ALTERAR UM CONTATO               *")
    print("*           3 - LISTAR CONTATOS                  *")
    print("*           4 - EXPORTAR CONTATOS                *")
    print("*           5 - EXCLUIR CONTATOS                 *")
    print("*           0 - SAIR DO SISTEMA                  *")
    print("**************************************************")


def mensagem_menu_alterar():
    limpar_tela()
    print("**************************************************")
    print("*         ALTERANDO UM CONTATO EXISTENTE         *")
    print("*------------------------------------------------*")
    print("*    ESCOLHA A OPÇÃO PARA LOCALIZAR O CONTATO    *")
    print("*           1 - ID                               *")
    print("*           2 - NOME                             *")
    print("*           3 - TELEFONE                         *")
    print("*           4 - CELULAR                          *")
    print("*           0 - MENU PRINCIPAL                   *")
    print("**************************************************")


def mensagem_cadastrar():
    limpar_tela()
    print("***************************************************")
    print("*           CADASTRANDO UM NOVO CONTATO           *")
    print("***************************************************")

def mensagem_excluir():
    limpar_tela()
    print("***************************************************")
    print("*           EXCLUIR CONTATO POR:                 *")
    print("*           1 - ID                               *")
    print("*           2 - NOME                             *")
    print("*           3 - TELEFONE                         *")
    print("*           4 - CELULAR                          *")
    print("*           0 - MENU PRINCIPAL                   *")
    print("***************************************************")


def menu_principal():
    try:
        mensagem_menu_principal()
        opcao = input("Informe a Opção desejada: ")
        acoes_menu_principal[opcao]()
    except:
        print("Opção inválida.")
        input("Pressione uma tecla para voltar ao menu principal...")
        menu_principal()


def cadastrar():
    mensagem_cadastrar()
    nome = input("Informe o nome do contato (Obrigatório): ")
    telefone = input("Informe o telefone do contato (Obrigatório): ")
    celular = input("Informe o celular do contato (Obrigatório): ")

    if nome and telefone and celular:
        confirma = input(f"Confirma cadastro do contato: {nome}? (S/N): ")
        if confirma.upper() == "S":
            try:
                contato = []
                contato.append(nome)
                contato.append(telefone)
                contato.append(celular)
                conexao = mysql.connector.connect(**dados_conexao)
                cursor = conexao.cursor()
                comando_sql = "insert into contatos (nome, telefone, celular) " \
                              "values (%s, %s, %s) "
                cursor.execute(comando_sql, contato)
                conexao.commit()
                cursor.close()
                conexao.close()
                input("Contato cadastrado com sucesso!\nPressione uma tecla para voltar ao menu principal...")
            except:
                input("Ocorreu um erro no cadastro.\nPressione uma tecla para voltar ao menu principal...")
        else:
            input("Cadastro cancelado.\nPressione uma tecla para voltar ao menu principal...")
    else:
        input("Todos os campos são  .\nPressione uma tecla para voltar ao menu principal...")

    menu_principal()


def alterar():
    mensagem_menu_alterar()
    opcao = input("Informe a opção desejada: ")
    try:
        acoes_menu_alterar[opcao]()
    except:
        input("Opção Inválida.\nPressione uma tecla para voltar...")
        alterar()



def excluir():
    mensagem_excluir()
    opcao = input("Informe a opção desejada: ")
    try:
        acoes_menu_excluir[opcao]()
    except:
        input("Opção Inválida!\nPressione uma tecla para voltar...")
        excluir()


def excluir_por_id(id = ""):

    try:
        if id == "":
            id = input("Informe o id do contato: ")
        comando_sql1 = f"select * from agenda.contatos where id = {id}"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql1)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {'id': id, 'nome': nome, 'telefone': telefone, 'celular': celular}

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']},"
                  f" telefone: {contato['telefone']}, celular: {contato['celular']}")
        cursor = conexao.cursor()
        cursor.execute(comando_sql1)
        validar = input("Deseja exlcuir o contato a cima ? [S/N]: ")
        if validar.upper() == 'S':
            comando_sql = f"delete from agenda.contatos where id = {id}"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql)
            conexao.commit()
            cursor.close()
            conexao.close()
        else:
            input("Operação Cancelada\nPressione qualquer tecla para voltar...")
            excluir()

        input("Contato excluído com sucesso !\nPressione qualquer tecla para voltar...")
        excluir()
    except Exception as erro:
        print("Ocorreu um erro ao exlcuir: ", erro)
        input("Pressione qualquer tecla para voltar...")
        excluir()



def excluir_por_nome():
    try:
        nome = input("Informe o nome do contato: ")
        comando_sql = f"select * from agenda.contatos where nome like '%{nome}%' limit 1"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']},"
                  f" telefone: {contato['telefone']}, celular: {contato['celular']}")
        conexao.commit()
        cursor.close()
        conexao.close()

        valida = input("Deseja exlcuir o contato a cima ? [S/N]: ")

        if valida.upper() == "S":
            comando_sql2 = f"SET SQL_SAFE_UPDATES=0"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql2)
            conexao.commit()
            cursor.close()
            conexao.close()

            comando_sql3 = f"delete from agenda.contatos where nome like '%{nome}%'"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql3)
            conexao.commit()
            cursor.close()
            conexao.close()

            comando_sql4 = f"SET SQL_SAFE_UPDATES=1"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql4)
            conexao.commit()
            cursor.close()
            conexao.close()
            input("Contato excluído com sucesso !\nPressione qualquer tecla para voltar...")
            excluir()
    except Exception as erro:
        print("Ocorreu um erro ao tentar excluir o contato ", erro)
        input("Pressione uma tecla para voltar...")
        excluir()



def excluir_por_telefone():
    try:
        tel = input("Informe o número de telefone: ")
        comando_sql = f"select * from agenda.contatos where telefone like '%{tel}%' limit 1"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']},"
                  f" telefone: {contato['telefone']}, celular: {contato['celular']}")
        conexao.commit()
        cursor.close()
        conexao.close()

        valida = input("Deseja exlcuir o contato a cima ? [S/N]: ")

        if valida.upper() == "S":
            comando_sql2 = f"SET SQL_SAFE_UPDATES=0"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql2)
            conexao.commit()
            cursor.close()
            conexao.close()

            comando_sql3 = f"delete from agenda.contatos where telefone like '%{tel}%'"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql3)
            conexao.commit()
            cursor.close()
            conexao.close()

            comando_sql4 = f"SET SQL_SAFE_UPDATES=1"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql4)
            conexao.commit()
            cursor.close()
            conexao.close()
            input("Contato excluído com sucesso !\nPressione qualquer tecla para voltar...")
            excluir()
    except Exception as erro:
        print("Ocorreu um erro ao tentar excluir o contato ", erro)
        input("Pressione uma tecla para voltar...")
        excluir()

def excluir_por_celular():
    try:
        tel = input("Informe o número de Celular: ")
        comando_sql = f"select * from agenda.contatos where celular like '%{tel}%' limit 1"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']},"
                  f" telefone: {contato['telefone']}, celular: {contato['celular']}")
        conexao.commit()
        cursor.close()
        conexao.close()

        valida = input("Deseja exlcuir o contato a cima ? [S/N]: ")

        if valida.upper() == "S":
            comando_sql2 = f"SET SQL_SAFE_UPDATES=0"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql2)
            conexao.commit()
            cursor.close()
            conexao.close()

            comando_sql3 = f"delete from agenda.contatos where celular like '%{tel}%'"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql3)
            conexao.commit()
            cursor.close()
            conexao.close()

            comando_sql4 = f"SET SQL_SAFE_UPDATES=1"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql4)
            conexao.commit()
            cursor.close()
            conexao.close()
            input("Contato excluído com sucesso !\nPressione qualquer tecla para voltar...")
            excluir()
    except Exception as erro:
        print("Ocorreu um erro ao tentar excluir o contato ", erro)
        input("Pressione uma tecla para voltar...")
        excluir()


def pesquisar_id(id = ""):
    try:
        if not id:
            id = input("Informe o id do contato: ")
        comando_sql = f"select id, nome, telefone, celular from contatos where id = {id}"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}
        cursor.close()
        conexao.close()

        alterar_contato(contato)
    except Exception as err:
        print("Ocorreu erro na busca por id! ", err)
        input("Pressione uma tecla para voltar...")
        alterar()


def pesquisar_nome():
    try:
        nome = input("Informe o nome do contato: ")
        comando_sql = f"select id, nome, telefone, celular from contatos where nome like '%{nome}%'"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}
        cursor.close()
        conexao.close()

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']},"
                  f"telefone: {contato['telefone']}, celular: {contato['celular']}")
            pesquisar_id(contato['id'])
    except Exception as err:
        print("Ocorreu erro na busca por nome! ", err)
        input("Pressione uma tecla para voltar...")
        alterar()


def pesquisar_telefone():
    try:
        telefone = input("Informe o telefone do contato: ")
        comando_sql = f"select id, nome, telefone, celular from contatos where telefone = '{telefone}'"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}
        cursor.close()
        conexao.close()

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']}, "
                  f"telefone: {contato['telefone']}, celular: {contato['celular']}")
            pesquisar_id(contato['id'])
    except Exception as err:
        print("Ocorreu erro na busca por telefone! ", err)
        input("Pressione uma tecla para voltar...")
        alterar()


def pesquisar_celular():
    try:
        celular = input("Informe o celular do contato: ")
        comando_sql = f"select id, nome, telefone, celular from contatos where celular = '{celular}'"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando_sql)
        contato = []
        for id, nome, telefone, celular in cursor:
            contato = {"id": id, "nome": nome, "telefone": telefone, "celular": celular}
        cursor.close()
        conexao.close()

        if contato:
            print(f"Contato localizado: id: {contato['id']}, nome: {contato['nome']},"
                  f"telefone: {contato['telefone']}, celular: {contato['celular']}")
            pesquisar_id(contato['id'])
    except Exception as err:
        print("Ocorreu erro na busca por celular! ", err)
        input("Pressione uma tecla para voltar...")
        alterar()


def alterar_contato(contato):
    nome = input(f"Informe o nome do contato ({contato['nome']}): ") or contato['nome']
    telefone = input(f"Informe o telefone do contato ({contato['telefone']}): ") or contato['telefone']
    celular = input(f"Informe o celular do contato ({contato['celular']}): ") or contato['celular']

    confirma = input(f"Confirma alteração do contato: {nome}? (S/N): ")
    if confirma.upper() == "S":
        try:
            comando_sql = f"update contatos set nome = '{nome}', telefone = '{telefone}'," \
                          f"celular = '{celular}' where id = {contato['id']}"
            conexao = mysql.connector.connect(**dados_conexao)
            cursor = conexao.cursor()
            cursor.execute(comando_sql)
            conexao.commit()
            cursor.close()
            conexao.close()
            input("Contato alterado com sucesso!\nPressione uma tecla para voltar...")
        except:
            input("Ocorreu um erro na alteraÃ§Ã£o.\nPressione uma tecla para voltar...")
    else:
        input("AlteraÃ§Ã£o cancelada.\nPressione uma tecla para voltar...")
    alterar()


def listar():
    try:
        comando = "select id, nome, telefone, celular from contatos order by id desc"
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()
        cursor.execute(comando)
        print("**************************************************")
        for id, nome, telefone, celular in cursor:
            print(f"Id: {id}")
            print(f"Nome: {nome}")
            print(f"Telefone: {telefone}")
            print(f"Celular: {celular}")
            print("**************************************************")

        cursor.close()
        conexao.close()
        input("Pressione uma tecla para voltar ao menu principal...")
    except:
        print("Ocorreu erro no listar.")
    menu_principal()


def exportar():
    try:
        nome_arquivo = input("Informe o nome do arquivo: ")

        comando = "select id, nome, telefone, celular from contatos order by id desc"
        contatos = []
        conexao = mysql.connector.connect(**dados_conexao)
        cursor = conexao.cursor()

        cursor.execute(comando)
        for id, nome, telefone, celular in cursor:
            contatos.append({"id": id, "nome": nome, "telefone": telefone, "celular": celular})

        cursor.close()
        conexao.close()

        arquivo = open(nome_arquivo, "w", encoding="utf-8")

        for contato in contatos:
            registro = []
            registro.append(f"{contato['id']};{contato['nome']};{contato['telefone']};{contato['celular']}\n")
            arquivo.writelines(registro)

        arquivo.close()
        print("ExportaÃ§Ã£o realizada.")
        input("Pressione uma tecla para voltar ao menu principal...")
        menu_principal()
    except Exception as err:
        print("Correu erro na funÃ§Ã£o exportar! ", err)
        input("Pressione uma tecla para voltar ao menu principal...")

acoes_menu_principal = {
    '1': cadastrar,
    '2': alterar,
    '3': listar,
    '4': exportar,
    '5': excluir,
    '0': sair
}

acoes_menu_alterar = {
    '1': pesquisar_id,
    '2': pesquisar_nome,
    '3': pesquisar_telefone,
    '4': pesquisar_celular,
    '0': menu_principal
}
acoes_menu_excluir = {
    '1': excluir_por_id,
    '2': excluir_por_nome,
    '3': excluir_por_telefone,
    '4': excluir_por_celular,
    '0': menu_principal
}

if __name__ == "__main__":
    menu_principal()
