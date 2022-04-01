import time
import random
import pandas as pd
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service

class Patient: 
    def __init__(self): 
        self.firstname = None
        self.lastname = None
        self.rfc = None
        self.date_of_birth = None
        self.sex = None

def format_patient_info(patient):
    p = Patient()
    p.firstname = patient['Nombre']
    p.lastname = patient['Apellidos']
    p.rfc = patient['RFC']
    year_of_birth = p.rfc[4:6] # El RFC solo cuenta con los últimos 2 digitos del año de nacimiento.
    year_of_birth = '20'+year_of_birth if int(year_of_birth) <= (date.today().year%100) else '19'+year_of_birth
    p.date_of_birth = f'{year_of_birth}-{p.rfc[6:8]}-{p.rfc[8:10]}'
    p.sex = 'Male' if patient['Sexo'] == 'hombre' else 'Female'

    return p

def register_patient_openemr(driver, patient):
    time.sleep(2)

    # Click en Patient.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainMenu']/div/div[5]/div"))).click()
    time.sleep(1)
    # Click en New/Search.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainMenu']/div/div[5]/div/ul/li[1]/div"))).click()    
    time.sleep(3) 

    # Entramos al Iframe de la ultima pestaña abierta (3ra): Search or Add patient.
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='framesDisplay']/div[3]/iframe")))
    time.sleep(3) 
    # Se escriben los datos del paciente.
    register_patient_box = driver.find_element(By.ID, 'form_fname')
    register_patient_box.send_keys(patient.firstname)
    register_patient_box = driver.find_element(By.ID, 'form_lname')
    register_patient_box.send_keys(patient.lastname)
    register_patient_box = driver.find_element(By.ID, 'form_pubpid')
    register_patient_box.send_keys(patient.rfc)
    register_patient_box = driver.find_element(By.ID, 'form_DOB')
    register_patient_box.send_keys(patient.date_of_birth)
    select_sex = Select(driver.find_element(By.ID, 'form_sex'))
    select_sex.select_by_value(patient.sex)
    time.sleep(3) 
    # Click al boton Create New Patient.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "create"))).click()
    # Salimos del iframe: Search or Add patient.
    driver.switch_to.default_content()

    # Entramos al iframe de la ventana modal que se abre cuando se da click en crear a paciente.
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "modalframe")))
    time.sleep(3) 
    # Click al boton Confirm Create New Patient.
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='searchResultsHeader']/center/input"))).click()
    # Salimos del iframe de la ventana modal.
    driver.switch_to.default_content()
    time.sleep(3)
    

def main():
    url='https://demo.openemr.io/openemr/interface/login/login.php?site=default'
    patients_to_register = 3
    patients = pd.read_csv('random_patients.csv', encoding='latin-1')

    try:
        s=Service('D:\\Programs\\chromedriver_win32\\chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        driver.maximize_window()
        driver.get(url)

        time.sleep(2) 

        # Se inicia sesión con la cuenta del recepcionista.
        login_box = driver.find_element(By.ID, 'authUser')
        login_box.send_keys('receptionist')
        time.sleep(1) 
        login_box = driver.find_element(By.ID, 'clearPass')
        login_box.send_keys('receptionist')
        time.sleep(1) 
        select_language = Select(driver.find_element(By.CSS_SELECTOR, 'select[name=languageChoice]'))
        select_language.select_by_value('1') # Value '1' = English (Standard)
        time.sleep(1) 
        login_box.submit()

        for index in random.sample(range(1, len(patients)), patients_to_register):
            # print(index)
            patient = format_patient_info(patients.loc[index])
            register_patient_openemr(driver, patient)

        # Despues de registrar a los pacientes, se abre la lista de todos los pacientes.
        # Click en Patient.
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainMenu']/div/div[5]/div"))).click()
        time.sleep(1)
        # Click en New/Search.
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainMenu']/div/div[5]/div/ul/li[1]/div"))).click()    
        time.sleep(3) 
        # Entramos al Iframe de la ultima pestaña abierta (3ra): Search or Add patient.
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='framesDisplay']/div[3]/iframe")))
        time.sleep(3) 
        # Click al boton Search.
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "search"))).click()

        time.sleep(10) 
    finally:
        driver.quit()

if __name__ == "__main__":
    main()