import time
import glob
import os
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Envio_Informacion(object):

    def envio_Informacion_by_name(self, driver, primero, segundo):
        envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, primero )))
        envio.click()
        envio.clear()
        envio.send_keys(segundo)
        time.sleep(1)

    def envio_Informacion_by_id(self, driver, primero, segundo):
        envio = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, primero )))
        envio.click()
        envio.clear()
        envio.send_keys(segundo)
        time.sleep(2)

class Click(object):

    def click_by_id(self, driver, primero):
        click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, primero )))
        click.click()
        time.sleep(2)

    def click_by_xpath(self, driver, primero):
        click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, primero )))
        click.click()
        time.sleep(1)

    def click_by_name(self, driver, primero):
        click = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, primero )))
        click.click()
        time.sleep(2)

class Ficheros(object):

    def eliminar_elementos(self, driver, primero):
        for x in glob.glob(primero):
            print("Eliminando : ", x)
            os.remove(x)
        time.sleep(3)

    def mover_elementos(self, driver, primero, segundo):
        ficheros = glob.glob(primero)
        i = len(ficheros)
        while i == 0:
            time.sleep(2)
            i += len(glob.glob(primero))
            print("Descargando en proceso...")

        shutil.move(glob.glob(primero)[0], segundo)
        time.sleep(2)

class Buscar_Elemento(object):

    def elemento(self, driver, primero):
        print( driver.find_element_by_xpath(primero).get_attribute("value") )
