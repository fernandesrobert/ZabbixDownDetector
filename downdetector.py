import json
import time
import random
import sys
from playwright.sync_api import sync_playwright

DOWNTIME_LIST = "downdetector.list"

# Lista de User-Agents para evitar detecção
user_agent_list = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.220 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/109.0.1518.78 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/537.36",
    # Novos User-Agents adicionados
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    # Firefox
    "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
]

STATUS_MAP = {
    "Relatórios de usuários indicam que não há problemas": 0,
    "Relatórios de usuários indicam potenciais problemas": 1,
    "Relatórios de usuários indicam problemas": 2
}

def load_services():
    """Carrega a lista de serviços do arquivo e retorna um dicionário."""
    services_to_monitor = {}
    try:
        with open(DOWNTIME_LIST, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) == 3 and parts[0] == "1":  # Apenas serviços ativos
                    _, service, public_name = parts
                    services_to_monitor[service] = public_name
    except FileNotFoundError:
        print(json.dumps({"error": f"Arquivo {DOWNTIME_LIST} não encontrado!"}, indent=4))
        sys.exit(1)
    
    return services_to_monitor

def check_service_status(service):
    """Verifica o status de um serviço no Downdetector e retorna um número conforme a legenda."""
    url = f"https://downdetector.com.br/fora-do-ar/{service}/"
    print(f"\n📡 Consultando status de: {service}")

    with sync_playwright() as p:
        try:
            user_agent = random.choice(user_agent_list)

            browser = p.chromium.launch(headless=False)  # Alterar para True se quiser rodar oculto
            context = browser.new_context(
                user_agent=user_agent,
                viewport={"width": random.randint(1280, 1920), "height": random.randint(720, 1080)},
                locale="pt-BR",
                timezone_id="America/Sao_Paulo",
                extra_http_headers={
                    "Accept-Language": "pt-BR,pt;q=0.9",
                    "Referer": "https://www.google.com/",
                    "DNT": "1",
                    "Upgrade-Insecure-Requests": "1"
                }
            )

            page = context.new_page()

            # **1. Removendo detecção Playwright**
            page.add_init_script(
                """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US']
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                """
            )

            # **2. Bloqueando WebRTC**
            page.add_init_script(
                """
                Object.defineProperty(navigator, 'hardwareConcurrency', {
                    get: () => 4
                });
                Object.defineProperty(navigator, 'deviceMemory', {
                    get: () => 8
                });
                Object.defineProperty(navigator, 'maxTouchPoints', {
                    get: () => 1
                });
                """
            )

            # **3. Espera aleatória para simular comportamento humano**
            delay = random.uniform(4, 8)
            print(f"⏳ Aguardando {delay:.2f} segundos antes de acessar o site...")
            time.sleep(delay)

            print(f"🌍 Acessando {url} ...")
            page.goto(url, timeout=20000)

            # **4. Simula rolagem e interação**
            page.mouse.move(random.randint(0, 300), random.randint(0, 300), steps=10)
            page.mouse.wheel(0, random.randint(200, 600))
            page.wait_for_timeout(random.uniform(1000, 3000))  # Espera de 1 a 3s

            print("📃 Página carregada. Buscando status...")

            selectors = ["h2.entry-title", "div.status-indicator", "h2.status-message"]
            status_element = None

            for selector in selectors:
                status_element = page.query_selector(selector)
                if status_element:
                    break  

            if status_element:
                status_text = status_element.inner_text().strip()
                print(f"✅ Status encontrado: {status_text}")
                return STATUS_MAP.get(status_text, -1)
            else:
                print("⚠️ Nenhum status encontrado! Pode ser um bloqueio ou alteração no layout.")
                return -1

        except Exception as e:
            print(f"❌ Erro ao acessar o site: {e}")
            return -1
        
        finally:
            print("🛑 Fechando navegador...")
            try:
                browser.close()
            except Exception as e:
                print(f"⚠️ Erro ao fechar o navegador: {e}")

def main():
    """Processa a lista de serviços e exibe o resumo final em JSON."""
    services = load_services()
    results = {}

    for service, public_name in services.items():
        status = check_service_status(service)
        results[public_name] = status

    print(json.dumps(results, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
