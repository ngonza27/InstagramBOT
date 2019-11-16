from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import random
import time
import re
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot

# Instagram bot that implements liking and commenting actions given a specific hashtag(#).
# You will need to run training.py first in order to train the chatterbot.
# Disclaimer: It takes arround 5 - 15 seconds to comment on a post. 

class InstagramBot:
    
    def __init__(self, usuario, contrasena):
        self.usuario    = usuario
        self.contrasena = contrasena
        self.driver     = webdriver.Firefox()


    def close_browser(self):
        self.driver.close( )
    

    #Login to the respective Instagram account
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


    #Obtain photos given a specific Hashtag(#)
    def obtener_fotos(self, hashtag, scrolls=int):
        self.driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(5)

        for i in range(1,scrolls):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

        hrefs = self.driver.find_elements_by_tag_name('a')
        hrefsFotos = [elem.get_attribute('href') for elem in hrefs]
        return(hrefsFotos)


    #Write the comment on the picture
    def escribir_comentario(self, comment_text):
        try:
            comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            #comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")           #English
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Añade un comentario...']")    #Spanish    
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


    def get_comments(self):
        time.sleep(3)
        try:
            comments_block = self.driver.find_element_by_class_name('EtaWk')        #English
            comments_in_block = comments_block.find_elements_by_class_name('C4VMK') #Spanish
            comments = [x.find_element_by_tag_name('span') for x in comments_in_block]
            user_comment = re.sub(r'#.\w*|\.', '', comments[0].text)
        except NoSuchElementException and StaleElementReferenceException as e:
            print(e)
            return ''
        return user_comment     
    

    def like_photo(self):
        self.driver.find_element_by_xpath('/html/body/span/section/main/div/div/article/div[2]/section[1]/span[1]/button/span[@aria-label="Me gusta"]').click() #Spanish
        time.sleep(1)

    
    def follow_user(self):
        self.driver.find_element_by_class_name('oW_lN').click() #Spanish
        time.sleep(1)
    

    def comment_on_picture(self):
        bot = ChatBot('ChatBot1')   #Obatin the trained chatterbot 
        bot.set_trainer(ListTrainer)    #Obtain the trained data
        picture_comment = self.get_comments()   #Obtain the comment on the current post
        response = bot.get_response(picture_comment).__str__()
        
        #Debug purposes only:
        #print("User's commnet:", picture_comment)
        #print("Bot response:", response)

        return self.post_comment(response)



com = InstagramBot(usuario="username",contrasena="password") #Instagram account credentials
com.login()
for pic in com.obtener_fotos(hashtag='purple', scrolls=2)[1:]:
    com.driver.get(pic)
    time.sleep(2)

    #Options:
    com.like_photo()            #Like post
    com.follow_user()           #Follow the user who made the post
    com.comment_on_picture()    #Comment post
    
    time.sleep(2)
com.close_browser()
