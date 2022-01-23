from selenium import webdriver
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
        self.fail('Finish the teste')

        # Ele é convidado a inserir um item de tarefa imediatamente

        # Ele digita "Buy peacock feathers" em uma caixa de texto

        # Quando ele tecla enter, a apgina é atualizada, e agora a pagina lista
        # "1: Buy peacock feathers" como um item em uma lista de tarefas

        # Ainda continua havendo uma caixa de texti convidando-o a acressentar outro
        # item. Ele insere "Use peacock feathers to make a fly"

        # A pagina é atualizada novamente e agora mostra os dois itens em sua lista

        # John se pergunta se o site lembrará de sua lista. Então nota
        # que o site gerou um URL único para ele -- há um pequeno
        # texto explicativo para isso.

        # Ele acessa esse URL - sua lista continua lá.

        # Satisfeito, ele volta a dormir

if __name__ == '__main__':
    unittest.main(warnings='ignore')



