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
        self.driver.set_window_size(450,500)

    def closeBrowser(self):
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
        try:
            comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().click()
            comment_box_elem().send_keys('')
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().click()
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            for letter in comment_text:
                print("AAAAAAAAAAAAAAAAAAAa")
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))

        except NoSuchElementException and StaleElementReferenceException as e:
            print(e)

com = Commentor(usuario="testofthetest01",contrasena="hola123456_")
com.login()
#pictures = com.obtener_fotos(hashtag="hola", scrolls=2)
#print(pictures)
com.driver.get("https://www.instagram.com/p/B19Ws73ByNj/")
com.escribir_comentario(comment_text="hola como estas hoy?")
