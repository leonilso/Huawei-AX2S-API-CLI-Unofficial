import typer
from app.core.client import RouterClient
from app.services import firewall
from typing import Literal

app = typer.Typer()

def get_client():
    client = RouterClient()
    client.login()
    return client

@app.command()
def firewall_status():
    """Mostra o status do firewall"""
    client = get_client()
    result = firewall.get_status(client)
    print(result)

@app.command()
def firewall_set(
    level: Literal["Disable", "Low", "High"] = typer.Option(
        ...,
        help="Nível do firewall"
    )
):
    """Muda o status do Firewall"""
    client = get_client()
    result = firewall.set_level(client, level)
    print(result)

if __name__ == "__main__":
    app()
