import os
import shutil
import time


# =====================================
# INGREDIENTES ESPERADOS
# =====================================

ingredientes = [
    "farinha",
    "açúcar",
    "cacau",
    "fermento",
    "manteiga",
    "ovos",
    "leite",
    "corante"
]


# =====================================
# VERIFICAR RECEITA
# =====================================

def verificar_receita(texto):

    texto = texto.lower()

    for ingrediente in ingredientes:
        if ingrediente not in texto:
            return False

    return True


# =====================================
# REGRA PRINCIPAL
# =====================================

def executar(evento, nome, eh_pasta, sistema):

    if evento == "criado" and eh_pasta and nome == "forno":

        pasta_forno = os.path.join(os.getcwd(), "forno")

        if not os.path.exists(pasta_forno):
            return

        print("[SISTEMA] O forno foi preparado...")
        time.sleep(2)

        arquivos = os.listdir(pasta_forno)

        for arquivo in arquivos:

            if arquivo.endswith(".txt"):

                caminho = os.path.join(pasta_forno, arquivo)

                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read()

                print("[SISTEMA] Analisando ingredientes...")
                time.sleep(2)

                if verificar_receita(conteudo):

                    print("[SISTEMA] A mistura parece correta...")
                    time.sleep(3)

                    destino = os.path.join("material_oculto", "forno")

                    shutil.move("forno", destino)

                    print("[SISTEMA] O bolo está assando...")
                    time.sleep(4)

                    senha = """
O bolo está pronto.

Senha do arquivo:

red_velvet
"""

                    with open("bolo.txt", "w", encoding="utf-8") as f:
                        f.write(senha)

                    print("[SISTEMA] Algo apareceu na mesa.")
                    return

        print("[SISTEMA] Algo na receita parece errado...")
