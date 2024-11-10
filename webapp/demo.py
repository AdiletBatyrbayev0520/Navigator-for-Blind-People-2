# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

import streamlit as st
from st_audiorec import st_audiorec

# DESIGN implement changes to the standard streamlit UI/UX
# --> optional, not relevant for the functionality of the component!
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode


def audiorec_demo_app():

    # TITLE and Creator information
    st.title('streamlit audio recorder')
    st.markdown('Implemented by '
        '[Stefan Rummer](https://www.linkedin.com/in/stefanrmmr/) - '
        'view project source code on '
                
        '[GitHub](https://github.com/stefanrmmr/streamlit-audio-recorder)')
    st.write('\n\n')

    # TUTORIAL: How to use STREAMLIT AUDIO RECORDER?
    # by calling this function an instance of the audio recorder is created
    # once a recording is completed, audio data will be saved to wav_audio_data

    wav_audio_data = st_audiorec() # tadaaaa! yes, that's it! :D

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.50, 0.50])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        st.write('The .wav audio data, as received in the backend Python code,'
                 ' will be displayed below this message as soon as it has'
                 ' been processed. [This informative message is not part of'
                 ' the audio recorder and can be removed easily] 🎈')

    if wav_audio_data is not None:
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            st.audio(wav_audio_data, format='audio/wav')
    return wav_audio_data

def stt(audio):
    options = Options()
    options.add_argument("--headless")  # Режим без графического интерфейса

    # Настройка драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://issai.nu.edu.kz/soyle-project/')
        
        # Найдите элемент input для загрузки файла и загрузите файл
        file_input = driver.find_element(By.NAME, "file")
        file_input.send_keys(audio)
        
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


if __name__ == '__main__':
    # call main function
    audio = audiorec_demo_app()
    while(audio is not None):
        time.sleep(5)
    stt(audio)

