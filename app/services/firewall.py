def set_level(client, level: str):
    return client.post("/api/ntwk/firewall", {
        "SetLevel": level
    })

def get_status(client):
    return client.get("/api/ntwk/firewall")
