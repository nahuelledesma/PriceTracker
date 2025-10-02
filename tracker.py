import requests
from bs4 import BeautifulSoup

def get_price(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Ejemplo básico MercadoLibre
        price_span = soup.find("span", {"class": "andes-money-amount__fraction"})
        if price_span:
            price_str = price_span.text.strip().replace(".", "").replace(",", ".")
            return float(price_str)
        else:
            return None
    except Exception as e:
        print(f"❌ Error obteniendo precio: {e}")
        return None

def check_price(product):
    return get_price(product["url"])
