import textwrap

def main():
    AGENCIA = "0001"
    numDeSaqueAtual = 0
    LIMITE_SAQUES = 3
    limiteMaximoDeSaque = 500
    saldo = 0
    extrato = ""
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valorDeposito = float(input("Digite o valor de Deposito: "))
            saldo, extrato = depositar(saldo, valorDeposito, extrato)

        elif opcao == "s":
            valorSaque = float(input("Digite o valor de Saque: "))
            saldo, extrato, numDeSaqueAtual = sacar(
                saldo=saldo,
                valor=valorSaque,
                extrato=extrato,
                limite=limiteMaximoDeSaque,
                numero_saques=numDeSaqueAtual,
                limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência: \t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado!@@@")
    return None

def menu():
    menu = """\n
    ===================== Menu =====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    =>"""
    return input(textwrap.dedent(menu))

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Usuário já cadastrado! @@@")
        return

    nome = input("Informe nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("=== Usuário criado com sucesso! ===")

def exibir_extrato(saldo, /, *, extrato):
    print("============== Extrato ==============\n")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"Saldo:\t\t R${saldo:.2f}")
    print("=====================================")

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("A operação falhou, o valor informado é inválido")
    return saldo, extrato

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Erro! Você não possui saldo suficiente.")
    elif valor <= 0:
        print("Valor digitado é inválido.")
    elif valor > limite:
        print("Valor máximo permitido por saque é R$500.00.")
    elif numero_saques >= limite_saques:
        print("Você atingiu a quantidade máxima de saques diários.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque: R$ {valor:.2f}\n"
        print("Número de saque atual: ", numero_saques, "\nMáximo diário: ", limite_saques)
    return saldo, extrato, numero_saques

main()
