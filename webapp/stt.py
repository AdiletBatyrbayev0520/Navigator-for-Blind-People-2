from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

options = Options()
options.add_argument("--headless")  # Режим без графического интерфейса

# Настройка драйвера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get('https://issai.nu.edu.kz/soyle-project/')
    
    # Найдите элемент input для загрузки файла и загрузите файл
    file_input = driver.find_element(By.NAME, "file")
    file_input.send_keys('/Users/adiletbatyrbaev/Downloads/speech2.mp3')
    
    # Ожидание загрузки файла и обновления JavaScript
    time.sleep(2)  # Используйте time.sleep для простоты вместо implicitly_wait

    # Проверка обновления текста
    uploaded_text = driver.find_element(By.ID, 'audio-uploader-text').text
    print('Текст после загрузки:', uploaded_text)

    time.sleep(5)
    
    element = driver.find_element(By.ID, 'audio-upload-button')
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()  # Прокрутка до элемента
    element.click()  # Клик по элементу
    
    # Увеличьте время ожидания до 30 секунд
    text_element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "audio-result")))

    # Считывание текста
    extracted_text = text_element.text
    extracted_text = extracted_text + "?"
    print("Извлеченный текст:", extracted_text)

except Exception as e:
    # Снимок экрана при возникновении ошибки
    driver.save_screenshot('error_screenshot.png')
    print(f"Exception occurred: {e}")

finally:
    driver.quit()
