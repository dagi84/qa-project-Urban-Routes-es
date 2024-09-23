import time

import data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from locators import ComfortMethodLocators

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
    message_to_driver = (By.CSS_SELECTOR, "#comment")
    order_blanket_tissues = (By.CSS_SELECTOR, 'div.reqs-arrow.open img[alt="Arrow"]')


    #active_switch = (By.CSS_SELECTOR, 'input.switch-input[type="checkbox"]')
    #code_sms = (By.CSS_SELECTOR, '[name="phone"]')
    #confirm_button = (By.XPATH, '//button[text()="Confirmar"]')
    #payment_method = (By.CLASS_NAME, 'pp-text')
    #card_add_button = (By.CLASS_NAME, 'pp-title')
    #add_credit_card = (By.XPATH, '//*[text()="agregar tarjeta"]')
    #add_card_number = (By.ID, 'number')
    #card_cvv = (By.XPATH, '//*[@id="code"]')
    #add_card_action_button = (By.CSS_SELECTOR, 'button[type="submit"].button.full')
    #button_close = (By.CSS_SELECTOR, 'button.close-button')

    #icecream_button = (By.XPATH, '//div[@class="r-counter-label" and text()="Helado"]')
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

    # Retorna un sms que se debe introducir
    def get_code_sms(self):
        get_phone_code = retrieve_phone_code(self.driver)
        return self.driver.find_element(*self.code_sms).send_keys(get_phone_code)

    # Click en confirmar mensaje sms
    def confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    # clic en el botón que permite seleccionar un metodo de pago
    def payment_method_button(self):
        self.driver.find_element(*self.payment_method).click()

    # clic en el botón que selecciona la opción para agregar una tarjeta
    def pick_card_button(self):
        self.driver.find_element(*self.card_add_button).click()

    # clic en el botón que permite agregar una tarjeta de crédito
    def add_card(self):
        self.driver.find_element(*self.add_credit_card).click()

    # Encuentra los campos para ingresar el número de la tarjeta y el código CVV
    def add_number(self):
        self.driver.find_element(*self.add_card_number).send_keys(data.card_number)
        self.driver.find_element(*self.card_cvv).send_keys(data.card_code)

    # clic en agregar
    def add_card_button(self):
        self.driver.find_element(*self.add_card_action_button).click()

    # clic en cerrar ventana
    def close_the_window(self):
        self.driver.find_element(*self.button_close).click()

    # Buscar campo"Mensaje para el conductor"
    def add_message_for_driver(self,message):
        self.driver.find_element(*self.message_to_driver).send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_to_driver).text




    # Pedir manta y panuelos
    def search_order_blanket_tissues(self):
        self.driver.find_element(*self.order_blanket_tissues).click()

    # validar que manta y panuelos esten seleccionados
    def blanket_tissues_selected(self):
        self.driver.find_element(*self.order_blanket_tissues).is_displayed()


    # busco para agregar helados
    def search_icecream(self):
        ice_cream = self.driver.find_element(*self.icecream_button)
        return self.driver.scroll_to_element(ice_cream)

    # agrego los helados
    def add_ice_cream(self):
        self.driver.find_element(*self.add_icecream)
        action = ActionChains(self.driver)
        action.double_click(ice_cream_element).perform()


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        time.sleep(3)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.configure_route(data.address_from, data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_comfort(self):
        request_taxi = (By.XPATH, ".//div[@class='results-text']/button[@class='button round']")

        # Esperar a que el botón sea clickeable
        WebDriverWait(self.driver, 10).until(expected_conditions.element_to_be_clickable(request_taxi))

        # Desempaquetar el localizador para find_element
        self.driver.find_element(*request_taxi).click()

        # Esperar a que el botón de Comfort sea clickeable
     #   WebDriverWait(self.driver, 10).until(
      #      expected_conditions.element_to_be_clickable(ComfortMethodLocators.COMFORT_BUTTON))

        route_page = UrbanRoutesPage(self.driver)
        route_page.click_comfort_button()

        # Validar el estado del botón
        assert route_page.is_comfort_button_selected() == True

    def test_fill_phone_number(self):
        number = (By.CLASS_NAME, "np-text")
        code = (By.ID, "code")
        confirm = (By.XPATH, ".//*[text()='Confirmar']")
        self.driver.find_element(*number).click()
        route_page = UrbanRoutesPage(self.driver)
        route_page.send_phone_number(data.phone_number)
        self.driver.find_element(*code).send_keys(retrieve_phone_code(driver=self.driver))
        self.driver.find_element(confirm).click()


    @classmethod
    def teardown_class(cls):
        time.sleep(3)
        cls.driver.quit()
