import os
import time

# sobe de sistema_adm/ para a pasta do enigma
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# opcional: ignorar arquivos internos do sistema
IGNORAR = {
    os.path.join(BASE_DIR, "sistema_adm", "verificacao.txt"),
    os.path.join(BASE_DIR, "sistema_adm", "monitor.lock"),
}

INTERVALO = 1


def snapshot(pasta):
    estado = {}

    for raiz, dirs, arquivos in os.walk(pasta):

        # detectar pastas
        for nome in dirs:
            caminho = os.path.join(raiz, nome)

            if caminho in IGNORAR:
                continue

            try:
                estado[caminho] = (
                    "DIR",
                    os.path.getmtime(caminho)
                )
            except:
                pass

        # detectar arquivos
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)

            if caminho in IGNORAR:
                continue

            try:
                estado[caminho] = (
                    "FILE",
                    os.path.getmtime(caminho)
                )
            except:
                pass

    return estado


def diff(anterior, atual):
    eventos = []

    # criados
    for k in atual:
        if k not in anterior:
            eventos.append(("CRIADO", k))

    # removidos
    for k in anterior:
        if k not in atual:
            eventos.append(("REMOVIDO", k))

    # modificados
    for k in atual:
        if k in anterior and atual[k] != anterior[k]:
            eventos.append(("MODIFICADO", k))

    return eventos


def mostrar_evento(tipo, caminho):
    nome = os.path.basename(caminho)
    pasta = os.path.dirname(caminho)

    print("\n====================")
    print(f"EVENTO: {tipo}")
    print(f"ITEM: {nome}")
    print(f"LOCAL: {pasta}")
    print("====================")
    print(flush=True)


def main():
    print("Monitor Archeio iniciado.")
    print(f"Monitorando: {BASE_DIR}")
    print()

    estado_anterior = snapshot(BASE_DIR)

    while True:
        try:
            atual = snapshot(BASE_DIR)

            eventos = diff(
                estado_anterior,
                atual
            )

            for tipo, caminho in eventos:
                mostrar_evento(
                    tipo,
                    caminho
                )

            estado_anterior = atual

            time.sleep(INTERVALO)

        except KeyboardInterrupt:
            break

        except Exception as e:
            print(f"Erro monitor: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
