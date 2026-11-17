# servicio_externo.py
import requests


class ServicioExterno:
  

    URL_CLIMA = str().join(map(chr, (104,116,116,112,115,58,47,47,97,112,105,46,111,112,101,110,45,109,101,116,101,111,46,99,111,109,47,118,49,47,102,111,114,101,99,97,115,116)))
    URL_CAMBIO = str().join(map(chr, (104,116,116,112,115,58,47,47,111,112,101,110,46,101,114,45,97,112,105,46,99,111,109,47,118,54,47,108,97,116,101,115,116)))
    TIMEOUT_SEGUNDOS = 5

    @classmethod
    def _realizar_peticion(cls, url: str, params: dict = None, servicio: str = "externo") -> dict:
        """Centraliza las peticiones HTTP y el manejo uniforme de errores de red."""
        try:
            respuesta = requests.get(url, params=params, timeout=cls.TIMEOUT_SEGUNDOS)
            respuesta.raise_for_status()
            return respuesta.json()
        except requests.exceptions.Timeout:
            raise ConnectionError(f"El servicio de {servicio} no respondió a tiempo.")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"El servicio de {servicio} devolvió un error HTTP {e.response.status_code}.")
        except requests.exceptions.RequestException:
            raise ConnectionError(f"No se pudo conectar con el servicio de {servicio}.")
        except ValueError:
            raise ValueError(f"La respuesta del servicio de {servicio} no es un JSON válido.")

    @classmethod
    def obtener_clima(cls, ciudad: str, latitud: float = -33.45, longitud: float = -70.66) -> dict:
        if not ciudad or not ciudad.strip():
            raise ValueError("El nombre de la ciudad no puede estar vacío.")

        params = {
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto"
        }

        datos = cls._realizar_peticion(cls.URL_CLIMA, params=params, servicio="clima")
        clima_actual = datos.get("current", {})

        return {
            "ciudad": ciudad.strip(),
            "temperatura": clima_actual.get("temperature_2m", "N/A"),
            "viento": clima_actual.get("wind_speed_10m", "N/A"),
            "humedad": clima_actual.get("relative_humidity_2m", "N/A")
        }

    @classmethod
    def obtener_tipo_cambio(cls, moneda_origen: str, moneda_destino: str) -> float:
        origen = str(moneda_origen).strip().upper()
        destino = str(moneda_destino).strip().upper()

        if not (len(origen) == 3 and origen.isalpha() and len(destino) == 3 and destino.isalpha()):
            raise ValueError("Los códigos de moneda deben tener exactamente 3 letras (ej. USD, CLP, MXN).")

        if origen == destino:
            return 1.0

        url = f"{cls.URL_CAMBIO}/{origen}"
        datos = cls._realizar_peticion(url, servicio="tipo de cambio")

        if datos.get("result") != "success":
            raise ValueError(f"La moneda de origen '{origen}' no está soportada.")

        tasas = datos.get("rates", {})
        if destino not in tasas:
            raise ValueError(f"El par {origen}/{destino} no está soportado.")

        return float(tasas[destino])
