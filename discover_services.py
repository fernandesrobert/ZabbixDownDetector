import json

DOWNTIME_LIST = "downdetector.list"

def discover_services():
    """Carrega os serviços e retorna no formato LLD do Zabbix."""
    discovered_services = {"data": []}

    try:
        with open(DOWNTIME_LIST, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) == 3 and parts[0] == "1":  # Apenas serviços ativos
                    _, service, public_name = parts
                    discovered_services["data"].append({
                        "{#SERVICE_NAME}": service,
                        "{#PUBLIC_NAME}": public_name
                    })
    except FileNotFoundError:
        print(json.dumps({"error": f"Arquivo {DOWNTIME_LIST} não encontrado!"}, indent=4))
        return

    print(json.dumps(discovered_services, indent=4))

if __name__ == "__main__":
    discover_services()
