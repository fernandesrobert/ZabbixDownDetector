# 🔍 Downdetector Monitor

![Downdetector Logo](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Downdetector_Logo.svg/2560px-Downdetector_Logo.svg.png)

![GitHub Repo stars](https://img.shields.io/github/stars/fernandesrobert/ZabbixDownDetector?style=social)  
![GitHub contributors](https://img.shields.io/github/contributors/fernandesrobert/ZabbixDownDetector)

Este projeto permite monitorar o status de serviços no **Downdetector** de forma automatizada utilizando o Playwright.

---

## 📌 Arquivos do projeto

### 📜 downdetector.py
Este script principal realiza a verificação do status dos serviços listados no arquivo `downdetector.list`. Ele:
- Simula um navegador real para evitar bloqueios;
- Obtém o status dos serviços;
- Exibe um relatório consolidado em JSON.

### 📜 downdetector.list
Lista os serviços a serem monitorados no formato:
```txt
1;nome_do_servico;Nome Público
```
Apenas serviços marcados com `1` serão monitorados.

### 📜 discover_services.py
Script auxiliar para descobrir serviços disponíveis no Downdetector.

---

## 🚀 Como Usar

### 📌 Requisitos
- Python 3.x
- Playwright instalado (`pip install playwright`)
- Chromium configurado (`playwright install`)

### ▶️ Execução
```bash
python downdetector.py
```

---

## 📊 Integração com Monitoramento
Este projeto pode ser integrado com sistemas de monitoramento como **Zabbix** e **Grafana**.

### 🔹 Zabbix
![Zabbix](https://cdn.worldvectorlogo.com/logos/zabbix-1.svg)

### 🔸 Grafana
![Grafana](https://cdn.freelogovectors.net/wp-content/uploads/2018/07/grafana-logo.png)

---

## 🤝 Contribuições
Contribuições são bem-vindas! Faça um fork, crie sua branch e abra um PR. 🎯

👥 **Contribuintes:**  
![GitHub contributors](https://img.shields.io/github/contributors/fernandesrobert/ZabbixDownDetector)

