from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class InstagramBot:
    def __init__(self, usuario, contrasena):
        self.usuario    = usuario
        self.contrasena = contrasena
        self.driver     = webdriver.Firefox()

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
    
    def darLike(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(5)

        for i in range(1,1):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        hrefs = driver.find_elements_by_tag_name('a')
        hrefsFotos = [elem.get_attribute('href') for elem in hrefs]
        print(hrefsFotos)
        for hrefsFotos in hrefsFotos:
            if hrefsFotos == 'https://www.instagram.com/':
                break
            driver.get(hrefsFotos)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                driver.find_element_by_xpath('/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button/span[@aria-label="Me gusta"]').click()
                time.sleep(1)
            except Exception as e:
                time.sleep(2)

ig = InstagramBot("username","password")
ig.login()

hashtags = ['mar', 'gatos']
[ig.darLike(tag) for tag in hashtags]
