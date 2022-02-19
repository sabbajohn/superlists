from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        # John ouviu falar de uma nova aplicação online interessante
        # para lista de tarefas. Ele decide verificar sua homepage
        self.browser.get('http://localhost:8000')

        # Ele percebe que o titulo da pagina e o cabeçalho mencionam listas de 
        # tarefas (to-do)
        
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Ele é convidado a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # Ele digita "Buy peacock feathers" em uma caixa de texto
        inputbox.send_keys('Buy peacock feathers')
        # Quando ele tecla enter, a apgina é atualizada, e agora a pagina lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue( 
                any(row.text == '1: Buy peacock feathers' for row in rows),
            f"New to-do item did not appear in table. Contents were:\n{table.text}"
        )

        # Ainda continua havendo uma caixa de texti convidando-o a acressentar outro
        # item. Ele insere "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # A pagina é atualizada novamente e agora mostra os dois itens em sua lista
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn (
            '2: Use peacock to make a fly',
            [row.text for  row in rows]
        )
        # John se pergunta se o site lembrará de sua lista. Então nota
        # que o site gerou um URL único para ele -- há um pequeno
        # texto explicativo para isso.
        self.fail('Finish the test')

        # Ele acessa esse URL - sua lista continua lá.

        # Satisfeito, ele volta a dormir

if __name__ == '__main__':
    unittest.main(warnings='ignore')



