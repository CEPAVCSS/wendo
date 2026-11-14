import json
from urllib.request import Request, urlopen


class CurrencyModel:
    base_url = "https://ve.dolarapi.com/v1"

    def get_rates(self):
        rates = {}
        try:
            for item in self._fetch("/cotizaciones"):
                self._add_rate(rates, item)
        except Exception:
            pass

        if "PARALELO" not in rates:
            try:
                self._add_rate(rates, self._fetch("/dolares/paralelo"))
            except Exception:
                pass

        if "PARALELO_EUR" not in rates:
            try:
                self._add_rate(rates, self._fetch("/euros/paralelo"))
            except Exception:
                pass

        return rates

    def _fetch(self, path):
        request = Request(
            f"{self.base_url}{path}",
            headers={"Accept": "application/json", "User-Agent": "Wendo/1.0"},
        )
        with urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))

    def _add_rate(self, rates, item):
        if not isinstance(item, dict):
            return
        promedio = item.get("promedio")
        if promedio is None:
            return
        try:
            value = float(promedio)
        except (TypeError, ValueError):
            return

        currency = str(item.get("moneda") or "").upper()
        source = str(item.get("fuente") or "").lower()

        if currency == "USD" and source == "oficial":
            rates["USD"] = value
        elif currency == "EUR" and source == "oficial":
            rates["EURO"] = value
        elif currency == "USD" and source == "paralelo":
            rates["PARALELO"] = value
        elif currency == "EUR" and source == "paralelo":
            rates["PARALELO_EUR"] = value
