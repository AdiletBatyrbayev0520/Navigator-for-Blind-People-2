import base64
# import time
# from pydub import AudioSegment
# from pydub.playback import play

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument("--headless")  # Headless mode

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    driver.get('https://issai.nu.edu.kz/kk/tts2-kaz/')
    
    # Wait until the button is clickable
    voice_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btn4")))
    
    # Scroll the button into view and click it
    driver.execute_script("arguments[0].scrollIntoView(true);", voice_btn)
    driver.execute_script("arguments[0].click();", voice_btn)
    
    # Wait for the text area to be present
    textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "text_tts")))
    textarea.clear()
    textarea.send_keys(input("Напишите текст: "))  # Correct method name
    
    # Wait for and click the upload button
    upload_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "upload_text_btn")))
    driver.execute_script("arguments[0].scrollIntoView(true);", upload_btn)
    driver.execute_script("arguments[0].click();", upload_btn)
    
    # Wait for and click the agreement checkbox
    agree_chbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agreement-checkbox")))
    driver.execute_script("arguments[0].click();", agree_chbox)
    
    # Wait for and click the agreement accept button
    agree_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "agreement-accept")))
    driver.execute_script("arguments[0].click();", agree_btn)
    
    # Wait for the audio element to be visible
    audio_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "listenme")))
    
    # Get the source URL from the nested <source> element
    source_element = WebDriverWait(audio_element, 10).until(EC.presence_of_element_located((By.TAG_NAME, "source")))
    src_url = source_element.get_attribute('src')

    if src_url:
        # Decode base64 audio data
        try:
            base64_audio = src_url.split(",")[1]
            audio_data = base64.b64decode(base64_audio)
            
            # Save audio to a file
            with open("audio.mp3", "wb") as f:
                f.write(audio_data)

            print("Audio file saved successfully.")
        except Exception as e:
            print(f"Error decoding and saving audio: {e}")
    else:
        print("The source element does not have a 'src' attribute or it is empty.")
finally:
    driver.quit()

# Play the saved audio file
# try:
    # play(AudioSegment.from_file("audio.mp3"))
    # print("Audio played successfully.")
# except Exception as e:
    # print(f"Error playing audio: {e}")
