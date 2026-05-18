# SSH Log Monitor — SIEM Básico

Monitor de logs de autenticação SSH em tempo real com detecção de ataques de força bruta.

Desenvolvido como projeto de estudo em segurança defensiva.

## O que o projeto faz

- Lê o arquivo de log em tempo real (sem releitura desnecessária)
- Detecta tentativas repetidas de login com senha errada
- Agrupa falhas por IP com janela deslizante de 60 segundos
- Exibe alertas coloridos no terminal ao atingir o limite configurado

## Como funciona

Cada linha nova no `auth.log` é analisada em busca do padrão `Failed password`.
Quando o mesmo IP ultrapassa 5 falhas em 60 segundos, um alerta vermelho é disparado.
Esse comportamento é semelhante ao do Fail2Ban em ambientes Linux de produção.

## Como usar

### Requisitos
- Python 3.10+
- colorama

### Instalação
pip install colorama

### Executar
python monitor.py

### Simular um ataque (Windows)
Add-Content auth.log 'May 18 03:14:55 myserver sshd[9999]: Failed password for root from 45.33.32.156 port 41200 ssh2'

Execute esse comando 5 vezes no terminal para ver o alerta vermelho.

## Exemplo de output

[INFO] Monitorando: auth.log
[AVISO] Falha do IP 45.33.32.156 (1/5)
[AVISO] Falha do IP 45.33.32.156 (4/5)
[ALERTA] 5 falhas do IP 45.33.32.156 nos últimos 60s!

## Conceitos aplicados

- Parsing de logs no formato auth.log do Linux
- Expressões regulares para extração de IP
- Janela deslizante de tempo para evitar falsos positivos
- Estrutura de dados defaultdict para agrupamento por IP
- Monitoramento em tempo real com leitura incremental de arquivo

## Próximas melhorias planejadas

- [ ] Envio de alerta por e-mail
- [ ] Exportação de alertas em JSON
- [ ] Dashboard web para visualização
- [ ] Bloqueio automático de IP via firewall

## Aprendizado

Projeto desenvolvido com auxílio de IA como ferramenta de estudo.
O foco foi compreender cada decisão técnica: por que o `defaultdict`,
por que o `f.seek`, como funciona a janela de tempo — não apenas fazer funcionar.