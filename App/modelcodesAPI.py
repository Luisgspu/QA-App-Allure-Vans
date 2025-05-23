import requests
import logging

class ModelCodesAPI:
    def __init__(self, access_token):
        """
        Initializes the ModelCodesAPI class with an access token for making API requests.
        
        Args:
            access_token (str): The access token for the API.
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def fetch_model_codes(self, market_code):
        """
        Fetches and filters model codes for vans cars from the API.

        Args:
            market_code (str): The market code to fetch model codes for.

        Returns:
            list: A list of vans car model codes, or an empty list if an error occurs.
        """
        url = f"https://api.oneweb.mercedes-benz.com/vehicle-deeplinks-api/v1/deeplinks/{market_code}/model-series"
        try:
            # Realiza la solicitud GET
            response = requests.get(url, headers=self.headers)

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Parsear la respuesta JSON
                try:
                    data = response.json()
                    if not isinstance(data, dict):
                        logging.error("La respuesta de la API no tiene el formato esperado.")
                        return []

                    # Filtrar los modelos disponibles
                    vans_car_model_codes = []
                    for model_key, model_data in data.items():
                        # Verificar si cualquier URL en el modelo contiene "/vans/" en la página de producto
                        contains_vans = any(
                            "/vans/" in value.get("modelSeriesUrl", "")
                            for key, value in model_data.items()
                            if isinstance(value, dict)
                        )
                        
                        # Verificar si cualquier URL en el modelo contiene "/passengercars/" en la Online Shop
                        contains_passengercars_in_online_shop = any(
                            "/passengercars/" in value.get("onlineShopUrl", "")
                            for key, value in model_data.items()
                            if isinstance(value, dict)
                        )
                        
                        # Verificar si no hay URL disponible para la Online Shop
                        no_online_shop_url = all(
                            "onlineShopUrl" not in value or not value.get("onlineShopUrl")
                            for key, value in model_data.items()
                            if isinstance(value, dict)
                        )
                        
                        # Incluir el modelo si cumple con los escenarios:
                        # A) "/vans/" en Product Page y "/passengercars/" en Online Shop
                        # B) "/vans/" en Product Page y no hay URL para Online Shop
                        if contains_vans and (contains_passengercars_in_online_shop or no_online_shop_url):
                            vans_car_model_codes.append(model_key)

                    return vans_car_model_codes
                except ValueError:
                    logging.error("Error al parsear la respuesta JSON.")
                    return []
            else:
                logging.error("Error al recuperar los datos. Código de estado: %s", response.status_code)
                return []
        except requests.exceptions.RequestException as e:
            logging.error("Ocurrió un error al realizar la solicitud: %s", e)
            return []

# Uso de la clase
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Reemplaza con tu token de acceso y código de mercado
    access_token = "YOUR_ACCESS_TOKEN"  # Reemplazar con el token de acceso real
    market_code = "IT/it"

    # Crear una instancia de la clase
    api = ModelCodesAPI(access_token)

    # Llamar al método para obtener los códigos de modelos
    vans_car_model_codes = api.fetch_model_codes(market_code)

    if vans_car_model_codes:
        print("vans Car Model Codes:", vans_car_model_codes)
    else:
        print("No se encontraron códigos de modelos de autos de pasajeros o ocurrió un error.")