import re, time, os
from collections import defaultdict
from colorama import Fore, init

init(autoreset=True)

LOG_FILE = "auth.log"
LIMITE_FALHAS = 5
JANELA_SEGUNDOS = 60

falhas_por_ip = defaultdict(list)

def analisar_linha(linha):
    if "Failed password" in linha:
        ip = re.search(r'from (\S+)', linha)

        if ip:
            ip = ip.group(1)
            agora = time.time()

            falhas_por_ip[ip].append(agora)

            falhas_por_ip[ip] = [
                t for t in falhas_por_ip[ip]
                if agora - t < JANELA_SEGUNDOS
            ]

            n = len(falhas_por_ip[ip])

            if n >= LIMITE_FALHAS:
                print(
                    Fore.RED +
                    f"[ALERTA] {n} falhas do IP {ip} nos últimos {JANELA_SEGUNDOS}s!"
                )
            else:
                print(
                    Fore.YELLOW +
                    f"[AVISO] Falha do IP {ip} ({n}/{LIMITE_FALHAS})"
                )

def monitorar(arquivo):
    print(Fore.GREEN + f"[INFO] Monitorando: {arquivo}")

    pos = os.path.getsize(arquivo)

    try:
        while True:
            with open(arquivo, "r", errors="ignore") as f:
                f.seek(pos)

                linhas = f.readlines()
                pos = f.tell()

            for linha in linhas:
                analisar_linha(linha.strip())

            time.sleep(0.5)

    except KeyboardInterrupt:
        print(
            Fore.CYAN +
            "\n[INFO] Encerrando monitoramento de forma segura..."
        )

    finally:
        print(Fore.GREEN + "[INFO] Programa finalizado.")

monitorar(LOG_FILE)