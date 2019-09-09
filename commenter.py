from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random
import time
import re

class Commentor:


    def __init__(self, usuario, contrasena):
        self.usuario    = usuario
        self.contrasena = contrasena
        self.driver     = webdriver.Firefox()

    def close_browser(self):
        self.driver.close( )
    

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        botonLogin = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        botonLogin.click()
        time.sleep(2)
        loginUsuario = driver.find_element_by_xpath("//input[@name = 'username']")
        loginUsuario.clear()
        loginUsuario.send_keys(self.usuario)
        loginContrasena = driver.find_element_by_xpath("//input[@name = 'password']")
        loginContrasena.clear()
        loginContrasena.send_keys(self.contrasena)
        loginContrasena.send_keys(Keys.RETURN)
        time.sleep(5)


    def obtener_fotos(self, hashtag, scrolls=int):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(5)

        for i in range(1,scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        hrefs = self.driver.find_elements_by_tag_name('a')
        hrefsFotos = [elem.get_attribute('href') for elem in hrefs]
        return(hrefsFotos)


    def escribir_comentario(self, comment_text):
        print("entro al comentario")
        try:
            comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().click()
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))

            return comment_box_elem

        except NoSuchElementException and StaleElementReferenceException as e:
            print(e)
            return False
        
    def post_comment(self, comment_text):
        time.sleep(random.randint(1, 5))
        comment_box_elem = self.escribir_comentario(comment_text)
        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
        time.sleep(random.randint(4, 7))
        self.driver.refresh()

        if comment_text in self.driver.page_source:
            return True
        return False

com = Commentor(usuario="testofthetest01",contrasena="hola123456_")
com.login()
com.driver.get("https://www.instagram.com/p/B19Ws73ByNj/")
com.post_comment(comment_text="hola como estamos!")
