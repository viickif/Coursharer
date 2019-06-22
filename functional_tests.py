import unittest
from selenium import webdriver


class TempGeneralTest(unittest.TestCase):
    def setUp(self): 
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self): 
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://127.0.0.1:5000/')

        # Browser title contains 'Coursharer'
        self.assertIn('Coursharer', self.browser.title) 
        self.fail('Finish the test!')
    
        # Clicks register button

        # Registers with *Account1*

        # Registers with *Account2*

        # Logins in with *Account1*

        # Tests edit Account criteria works

        # Creates a 10 posts from *Account1*

        # Creates a 15 posts from *Account2*

        # View *Account1* and *Account2* posts 

        # View *Account1*'s and *Account2*'s posts details

        # Edit posts details and unable to edit other user's posts

        # Delete posts

        # Logs out

        # Tries to create an account with the same credentials *Account1*

        # Deletes *Account1* and *Account2*

        # Satisfied

if __name__ == '__main__': 
    unittest.main(warnings='ignore')
 

