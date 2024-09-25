import time
from selenium.webdriver import ActionChains
import data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service

driver_path = r"C:\Users\dagip\Documents\QA Engeneer\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException

    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    comfort_button = (By.CLASS_NAME, 'tcard-icon')
    phone_number_field = (By.ID, 'phone')
    phone_send = (By.XPATH, '//button[text()="Siguiente"]')
    message_to_driver = (By.XPATH, "//label[@for='comment']")
    order_blanket_tissues = (By.CSS_SELECTOR, 'div.reqs-arrow.open img[alt="Arrow"]')
    payment_method = (By.CLASS_NAME, 'pp-text')
    space_message =(By.CSS_SELECTOR, "#comment")
    card_add_button = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    add_card_number = (By.CSS_SELECTOR, ".card-input")
    card_cvv = (By.XPATH, "//input[@placeholder='12']")
    button_add = (By.XPATH, "//button[text()='Agregar']")
    button_close = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")
    add_orders = (By.XPATH, "//div[text()='Requisitos del pedido']")
    req_blanket_and_tissues = (By.CLASS_NAME, "slider")
    icecream_button = (By.CSS_SELECTOR, "div.counter-plus.disabled")
    #add_icecream = (By.CSS_SELECTOR, 'div.counter-plus')

    def __init__(self, driver):
        self.driver = driver

    # Se completa el campo desde
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    # Se completa el campo hasta
    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    # Retorna el valor de campo desde
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    # Retorna el valor de campo hasta
    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def configure_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    # Click en modo Comfort
    def click_comfort_button(self):
        self.driver.find_element(*self.comfort_button).click()

    #verificar si el boton confort esta seleccionado
    def is_comfort_button_selected(self):
        return self.driver.find_element(*self.comfort_button).is_displayed()

    #poner numero de telefono
    def fill_phone_number(self,number):
        self.driver.find_element(*self.phone_number_field).send_keys(number)

    # clic en el botón que envía el número de teléfono ingresado
    def click_phone_number(self):
        self.driver.find_element(*self.phone_send).click()

    # Se muestra el campo que contiene el numero de telefono
    def read_phone_field(self):
        return self.driver.find_element(*self.phone_number_field).text


    def send_phone_number(self, number):
        self.fill_phone_number(number)
        self.click_phone_number()

    # clic en el botón que permite seleccionar un metodo de pago
    def payment_method_button(self):
        self.driver.find_element(*self.payment_method).click()

    # clic en el botón que selecciona la opción para agregar una tarjeta
    def pick_card_button(self):
        self.driver.find_element(*self.card_add_button).click()

    # clic en el botón que permite agregar una tarjeta de crédito
    def add_card(self):

        self.driver.find_element(*self.add_card_number).send_keys(data.card_number)
        self.driver.find_element(*self.card_cvv).send_keys(data.card_code)
        self.driver.find_element(By.ID, "number").click()
        self.driver.find_element(*self.button_add).click()
        self.driver.find_element(*self.button_close).click()


    # Buscar campo"Mensaje para el conductor"
    def add_message_for_driver(self):
        self.driver.find_element(*self.message_to_driver).click()

    def get_message_for_driver(self,message):
        self.driver.find_element(*self.space_message).send_keys(message)

    # Pedir manta y panuelos
    def search_order_blanket_tissues(self):
        self.driver.find_element(*self.add_orders).click()
        return self.driver.find_element(*self.req_blanket_and_tissues).click()


    # busco para agregar helados
    def search_icecream(self):
        icecream_button = self.driver.find_element(*self.icecream_button)
        actions = ActionChains(self.driver)
        actions.double_click(icecream_button).perform()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    # Test 1:para ingresar origen y destino
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.configure_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    # Test 2: para seleccionar tarifa confort
    def test_comfort(self):
        request_taxi = (By.XPATH, ".//div[@class='results-text']/button[@class='button round']")
        # Esperar a que el botón sea clickeable
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(request_taxi))
        # Desempaquetar el localizador para find_element
        self.driver.find_element(*request_taxi).click()
        route_page = UrbanRoutesPage(self.driver)
        route_page.click_comfort_button()
        # Validar el estado del botón
        assert route_page.is_comfort_button_selected() == True

    # Test 3: para rellenar numero de telefono
    def test_fill_phone_number(self):
        number = (By.CLASS_NAME, "np-text")
        code = (By.ID, "code")
        confirm = (By.XPATH, ".//*[text()='Confirmar']")
        self.driver.find_element(*number).click()
        route_page = UrbanRoutesPage(self.driver)
        route_page.send_phone_number(data.phone_number)
        self.driver.find_element(*code).send_keys(retrieve_phone_code(driver=self.driver))
        self.driver.find_element(*confirm).click()

    # Test 4: Para agregar tarjeta
    def test_add_payment_method(self):
        route_page = UrbanRoutesPage(self.driver)
        route_page.payment_method_button()
        route_page.pick_card_button()
        route_page.add_card()

    # Test 5: Mensaje para el conductor
    def test_message_to_driver(self):
        route_page = UrbanRoutesPage(self.driver)
        route_page.add_message_for_driver()
        message = data.message_for_driver
        route_page.get_message_for_driver(message)

    # Test 6: Pedir manta y panuelos
    def test_blanket_and_tissues(self):
        route_page = UrbanRoutesPage(self.driver)
        route_page.search_order_blanket_tissues()

    # Test 7: Pedir helados
    def test_add_icecream(self):
        route_page = UrbanRoutesPage(self.driver)
        route_page.search_icecream()

    # Test 8: Modal para buscar taxi

    # Test 9: Pedir manta y panuelos


    @classmethod
    def teardown_class(cls):
        time.sleep(3)
        cls.driver.quit()
