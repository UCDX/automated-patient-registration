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
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys

class Patient: 
    def __init__(self): 
        self.firstname = None
        self.lastname = None
        self.rfc = None
        self.date_of_birth = None
        self.weight = None
        self.height = None
        self.bp_systolic = None
        self.bp_diastolic = None
        self.pulse = None
        self.temperature = None
        self.bmi = None

def format_patient_info(patient):
    p = Patient()
    p.firstname = patient['Nombre']
    p.lastname = patient['Apellidos']
    p.rfc = patient['RFC']
    year_of_birth = p.rfc[4:6] # El RFC solo cuenta con los últimos 2 digitos del año de nacimiento.
    year_of_birth = '20'+year_of_birth if int(year_of_birth) <= (date.today().year%100) else '19'+year_of_birth
    p.date_of_birth = f'{year_of_birth}-{p.rfc[6:8]}-{p.rfc[8:10]}'
    p.sex = 'Male' if patient['Sexo'] == 'hombre' else 'Female'
    p.weight = patient['Peso[kg]']
    p.height = patient['Estatura[cm]']
    p.bp_systolic = int(patient['Presion[mmHg]'].split('/')[0])
    p.bp_diastolic = int(patient['Presion[mmHg]'].split('/')[1])
    p.pulse = patient['Pulso[bpm]']
    p.temperature = patient['Temperatura[C]']
    p.bmi = round(p.weight / (p.height/100)**2)

    return p

def register_patient_openemr(driver, patient):
    time.sleep(3)

    # Click en Patient.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainMenu']/div/div[6]/div"))).click()
    time.sleep(3)
    # Click en New/Search.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mainMenu']/div/div[6]/div/ul/li[1]/div"))).click()    
    time.sleep(3) 

    # Entramos al Iframe de la pestaña: Search or Add patient.
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='framesDisplay']/div[3]/iframe")))
    time.sleep(3) 
    # Se escriben los datos del paciente.
    register_patient_box = driver.find_element(By.ID, 'form_fname')
    register_patient_box.send_keys(patient.firstname)
    time.sleep(2)
    register_patient_box = driver.find_element(By.ID, 'form_lname')
    register_patient_box.send_keys(patient.lastname)
    time.sleep(2)
    register_patient_box = driver.find_element(By.ID, 'form_pubpid')
    register_patient_box.send_keys(patient.rfc)
    time.sleep(2)
    register_patient_box = driver.find_element(By.ID, 'form_DOB')
    register_patient_box.send_keys(patient.date_of_birth)
    time.sleep(2)
    select_sex = Select(driver.find_element(By.ID, 'form_sex'))
    select_sex.select_by_value(patient.sex)
    time.sleep(3) 
    # Click al boton Create New Patient.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "create"))).click()
    # Regresamos al html raiz.
    driver.switch_to.default_content()

    # Entramos al iframe de la ventana modal que se abre cuando se da click en crear a paciente.
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "modalframe")))
    time.sleep(3) 
    # Click al boton Confirm Create New Patient.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='searchResultsHeader']/center/input"))).click()
    # Se cierra la alerta desplegada despues que el medico registra al paciente.
    WebDriverWait(driver, 30).until(EC.alert_is_present(), 'Timed out waiting alert after create patient')
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass
    # Regresamos al html raiz.
    driver.switch_to.default_content()
    time.sleep(3)
    
def register_vitals_patient(driver, patient):
    # ------------------------- Registro de nuevo encuentro ------------------------
    time.sleep(3)

    # Click en el boton + para crear un nuevo encuentro con el paciente.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='attendantData']/div/div[2]/div/a[2]"))).click()
    time.sleep(3)

    # Entramos al Iframe de la cuarta pestaña actualizada: Patient Encounter.
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='framesDisplay']/div[4]/iframe")))
    time.sleep(3) 

    # Seleccionamos el tipo de visita (campo requerido).
    select_vis_category = Select(driver.find_element(By.ID, 'pc_catid'))
    select_vis_category.select_by_value('9') # Value '9' = Paciente regular.
    time.sleep(3) 

    # Click al boton Save.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='new-encounter-form']/div/div/div/button[1]"))).click()
    time.sleep(3)

    # ------------------------- Fin del registro de nuevo encuentro ------------------------

    # Entramos al iframe subpestaña Summary (profundidad 3)
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='enctabs-1']/iframe")))
    time.sleep(3) 

    # Click a la opción Clinical (menú).
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "category_Clinical"))).click()
    time.sleep(3)

    # Click a la opción Vitals para registrar los signos vitales.
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='navbarSupportedContent']/ul[1]/li[2]/div/a[11]"))).click()
    time.sleep(3)

    # Regresamos al html raiz.
    driver.switch_to.default_content()

    # -------------- Registro de signos vitales del paciente. -----------------------

    # Entramos al Iframe de la cuarta pestaña: Encounter.
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='framesDisplay']/div[4]/iframe")))
    time.sleep(3) 

    # Entramos al iframe subpestaña Vitals (profundidad 3).
    WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='enctabs-1001']/iframe")))
    time.sleep(3) 

    # Se registran los signos vitales del paciente.
    register_vitals_box = driver.find_element(By.ID, 'weight_input_metric')
    register_vitals_box.send_keys(str(patient.weight))
    time.sleep(2)
    register_vitals_box = driver.find_element(By.ID, 'height_input_metric')
    register_vitals_box.send_keys(str(patient.height))
    time.sleep(2)
    register_vitals_box = driver.find_element(By.ID, 'bps_input')
    register_vitals_box.send_keys(str(patient.bp_systolic))
    time.sleep(2)
    register_vitals_box = driver.find_element(By.ID, 'bpd_input')
    register_vitals_box.send_keys(str(patient.bp_diastolic))
    time.sleep(2)
    register_vitals_box = driver.find_element(By.ID, 'pulse_input')
    register_vitals_box.send_keys(str(patient.pulse))
    time.sleep(2)
    register_vitals_box = driver.find_element(By.ID, 'temperature_input_metric')
    register_vitals_box.send_keys(str(patient.temperature))
    time.sleep(2)
    # register_vitals_box = driver.find_element(By.ID, 'BMI_input')
    # register_vitals_box.send_keys(str(patient.bmi))
    # time.sleep(3) 
    register_vitals_box.submit()

    # -------------- Fin de registro de signos vitales del paciente. -----------------------

    # Regresamos al html raiz.
    driver.switch_to.default_content()
    time.sleep(3)

def main():
    # Nota: Se usa la demo b, para evitar que algunos XPATH no se encuentren en caso de que en 
    # la demo original el admin configure apartados del sistema.
    url='https://demo.openemr.io/b/openemr/interface/login/login.php?site=default'
    patients_to_register = 3
    user = 'physician'
    password_user = 'physician'
    path_to_chromedriver = '' # Dejar en '' si está en el path. # 'D:\\Programs\\chromedriver_win32\\chromedriver.exe'
    patients = pd.read_csv('random_patients.csv', encoding='latin-1')

    try:
        s = None
        if path_to_chromedriver != '' and path_to_chromedriver is not None:
            s=Service(path_to_chromedriver)
        else:
            s=Service()
        
        driver = webdriver.Chrome(service=s)
        driver.maximize_window()
        driver.get(url)

        time.sleep(3) 

        # Se inicia sesión con la cuenta del recepcionista.
        login_box = driver.find_element(By.ID, 'authUser')
        login_box.send_keys(user)
        time.sleep(2) 
        login_box = driver.find_element(By.ID, 'clearPass')
        login_box.send_keys(password_user)
        time.sleep(2) 
        select_language = Select(driver.find_element(By.CSS_SELECTOR, 'select[name=languageChoice]'))
        select_language.select_by_value('1') # Value '1' = English (Standard)
        time.sleep(2) 
        login_box.submit()

        for index in random.sample(range(1, len(patients)), patients_to_register):
            print(index + 2)
            patient = format_patient_info(patients.loc[index])
            register_patient_openemr(driver, patient)
            register_vitals_patient(driver, patient)

        time.sleep(10) 
    finally:
        driver.quit()

if __name__ == "__main__":
    main()