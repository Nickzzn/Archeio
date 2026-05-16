import os
import time
import threading
import importlib.util
import hashlib
import subprocess

BASE_DIR = os.getcwd()
ADM_DIR = os.path.join(BASE_DIR, "sistema_adm")
REGRAS_PATH = os.path.join(ADM_DIR, "regras.py")
VERIFICACAO_PATH = os.path.join(ADM_DIR, "verificacao.txt")
MONITOR_EXE = os.path.join(ADM_DIR, "monitor.exe")
MONITOR_PY = os.path.join(ADM_DIR, "monitor.py")

modo_adm = False
pausado = False
regras_modulo = None
player_name = "Jogador"
acao_sistema_ativa = False


def nero(msg, delay=0.01):
    for c in msg:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()


def iniciar_interface():
    global player_name

    nero("Sistema Archeio iniciando...")
    time.sleep(1)

    nero("Carregando N.E.R.O...")
    time.sleep(1)

    player_name = input("Digite seu nome: ").strip()

    if not player_name:
        player_name = "Jogador"

    nero(f"Bem-vindo, {player_name}.")
    nero("Archeio agradece por usar nosso produto.")
    nero("Interface N.E.R.O ativa.")

def iniciar_monitor():
    monitor_exe = os.path.join(ADM_DIR, "monitor.exe")

    if not os.path.exists(monitor_exe):
        nero(f"Monitor não encontrado: {monitor_exe}")
        return

    try:
        subprocess.Popen(
            [monitor_exe],
            cwd=ADM_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        nero("Monitor iniciado.")

    except Exception as e:
        nero(f"Erro ao abrir monitor: {e}")
def gerar_hash():
    if not os.path.exists(REGRAS_PATH):
        return None
    with open(REGRAS_PATH, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def sistema_travado():
    return os.path.exists(VERIFICACAO_PATH)


def verificar_integridade():
    if not sistema_travado():
        return True
    with open(VERIFICACAO_PATH) as f:
        salvo = f.read().strip()
    atual = gerar_hash()
    if atual != salvo:
        nero("Integridade comprometida. Execução bloqueada.")
        return False
    return True


def travar():
    h = gerar_hash()
    if not h:
        nero("regras.py não encontrado.")
        return
    with open(VERIFICACAO_PATH, "w") as f:
        f.write(h)
    nero("Sistema travado.")


def carregar_regras():
    global regras_modulo
    if not os.path.exists(REGRAS_PATH):
        return
    try:
        spec = importlib.util.spec_from_file_location("regras", REGRAS_PATH)
        regras_modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(regras_modulo)
    except Exception as e:
        nero(f"Erro regras: {e}")


def auto_reload():
    ultima = 0
    while True:
        try:
            if os.path.exists(REGRAS_PATH):
                mod = os.path.getmtime(REGRAS_PATH)
                if mod != ultima:
                    if sistema_travado() and gerar_hash() != open(VERIFICACAO_PATH).read().strip():
                        nero("Alteração bloqueada.")
                        ultima = mod
                        time.sleep(2)
                        continue
                    carregar_regras()
                    nero("Regras atualizadas.")
                    ultima = mod
        except:
            pass
        time.sleep(2)


def revelar(p):
    os.system(f'attrib -h -s "{p}"')


def esconder(p):
    os.system(f'attrib +h +s "{p}"')


def adm(cmd):
    global modo_adm, pausado, acao_sistema_ativa
    cmd = cmd.lower().strip()

    if cmd == "travar":
        acao_sistema_ativa = True
        travar()
        acao_sistema_ativa = False

    elif cmd == "pausar":
        pausado = True
        nero("Sistema pausado.")

    elif cmd == "retomar":
        pausado = False
        nero("Sistema retomado.")

    elif cmd == "recarregar":
        carregar_regras()

    elif cmd == "revelar":
        revelar("material_oculto")

    elif cmd == "esconder":
        esconder("material_oculto")

    elif cmd == "revelar sys":
        revelar("sistema_adm")

    elif cmd == "esconder sys":
        esconder("sistema_adm")

    elif cmd == "estrutura":
        for r,_,_ in os.walk(BASE_DIR):
            print(r)

    elif cmd == "limpar":
        os.system("cls")

    elif cmd == "resetar":
        carregar_regras()

    elif cmd == "exit":
        modo_adm = False
        nero("Saindo do ADM.")

    else:
        nero("Comando desconhecido.")


def main():
    global modo_adm
    iniciar_interface()

    if not verificar_integridade():
        return

    carregar_regras()
    iniciar_monitor()

    threading.Thread(target=auto_reload, daemon=True).start()

    while True:
        try:
            c = input("> ").strip()
            if not modo_adm:
                if c == "ADM.key":
                    modo_adm = True
                    nero("ADM ativado.")
                continue
            adm(c)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
