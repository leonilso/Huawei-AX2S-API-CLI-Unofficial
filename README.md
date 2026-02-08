Router API CLI

Projeto para controle de roteadores Huawei AX2S via API interna utilizando autenticação SCRAM.
Estruturado para execução via CLI e preparado para containerização com Docker.

============================================================
Objetivo
============================================================

Fornecer uma interface organizada para:
- Autenticação no roteador
- Consumo de endpoints internos
- Execução de comandos via linha de comando
- Organização modular para manutenção e expansão

============================================================
Estrutura de Pastas
============================================================

app/
core/
client.py -> Cliente HTTP com sessão e login SCRAM
config.py -> Configurações via variáveis de ambiente
services/ -> Onde ficam as rotas/endpoints do roteador
firewall.py -> Endpoint relacionados ao firewall
cli/
main.py -> Interface CLI usando Typer

============================================================
Requisitos
============================================================

Python 3.10+

Bibliotecas necessárias (estão presentes no requirements.txt):
- requests==2.31.0
- beautifulsoup4==4.12.3
- typer==0.12.3
- python-dotenv==1.0.1

Instalar dependências:

pip install -r requirements.txt

============================================================
Variáveis de Ambiente
============================================================

Criar um arquivo .env na raiz do projeto, pode ser o .env.example:

ROUTER_IP=192.168.1.1
ROUTER_USER=admin
ROUTER_PASSWORD="SenhaDoRoteador"

============================================================
Executando o Projeto
============================================================

Rodar via terminal:

`python -m app.cli.main`

Listar comandos disponíveis:

`python -m app.cli.main --help`

Exemplo de comando 

Ver status do firewall:

`python -m app.cli.main firewall-status`


============================================================
Arquitetura
============================================================

core/
Responsável por autenticação, sessão HTTP e gerenciamento de CSRF.

services/
Contém lógica isolada por domínio (firewall, rede, sistema, etc).
Não depende de CLI.

main.py
Camada de interface CLI.
Define parâmetros e interage com os serviços.

============================================================
Segurança
============================================================

- Autenticação via SCRAM-SHA256.
- Sessão mantida via cookie SessionID_R3.
- CSRF atualizado a cada requisição autenticada.

============================================================
Próximos Passos
============================================================

- Implementar novos módulos (wan, wlan, system, nat).
- Adicionar logging estruturado.
- Implementar testes automatizados.

============================================================
Observação
============================================================

Este projeto utiliza endpoints internos do firmware do roteador.
Alterações incorretas podem afetar a conectividade da rede.
Use com responsabilidade.