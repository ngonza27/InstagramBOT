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

    def escribir_comentario(self, coment_text):
        try:
            comment_button = self.driver.find_element_by_xpath('/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button/span[@aria-label="Comment"]')
            comment_button.click()
        except NoSuchElementException:
            pass
        
        try:
            cuadro_comentario = self.driver.find_element_by_xpath("//textarea [@aria-label='Add a comment…']")
            #uadro_comentario.clear()
            #cuadro_comentario.send_keys("hola")
            #cuadro.clear()
        except NoSuchElementException and StaleElementReferenceException as e:
            print(e)

com = Commentor(usuario="testofthetest01",contrasena="hola123456_")
com.login()
#pictures = com.obtener_fotos(hashtag="hola", scrolls=2)
#print(pictures)
com.driver.get("https://www.instagram.com/p/B1v5L2Ijal0/")
com.escribir_comentario("asd")