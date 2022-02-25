from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_for_one_user(self):
        # John ouviu falar de uma nova aplicação online interessante
        # para lista de tarefas. Ele decide verificar sua homepage
        self.browser.get(self.live_server_url)

        # Ele percebe que o titulo da pagina e o cabeçalho mencionam listas de 
        # tarefas (to-do)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # Ele é convidado a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # Ele digita "Buy peacock feathers" em uma caixa de texto
        inputbox.send_keys('Buy peacock feathers')
        # Quando ele tecla enter, a apgina é atualizada, e agora a pagina lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Ainda continua havendo uma caixa de texti convidando-o a acressentar outro
        # item. Ele insere "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # A pagina é atualizada novamente e agora mostra os dois itens em sua lista
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # John se pergunta se o site lembrará de sua lista. Então nota
        # que o site gerou um URL único para ele -- há um pequeno
        # texto explicativo para isso.

        # Ele acessa esse URL - sua lista continua lá.

        # Satisfeito, ele volta a dormir

    def test_multiple_users_can_start_lists_at_different_urls(self):
        #John inicia uma lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Ele percebe que a sua lista possui um URL unico
        john_list_url = self.browser.current_url
        self.assertRegex(john_list_url, '/list/.+')

        # Agora um novo usuario, Francis, chega ao site
        ## Nos utilizamos uma nova sessão do navegador para garantir
        ## nenhuma informção de John esta vindo de cookies e etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visita a pagina inicial, Não nenhum sinal da lista de John
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis inicia uma nova lista inserindo um novo item
        # menos interessante que John
        inputbox = self.browser.find_element(By.ID, 'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #Francis obtem sua URL unica
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, john_list_url)

        # Novamente nenhum sinal da lista de John
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #Satisfeitos, ambos voltam a dormir
