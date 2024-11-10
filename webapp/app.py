from pathlib import Path
import time
import PIL

import streamlit as st

import settings
import helper

st.set_page_config(
    page_title="Object Detection using YOLOv7",
    page_icon=":mortar_board:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Batyrbayev Alisher: Navigator For Blind People")

st.sidebar.header("ML Model Config")

model_type = st.sidebar.radio(
    "Select Task", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
    model_path_2 = Path(settings.DETECTION_MODEL_2)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

try:
    model = helper.load_model(model_path)
    model_2 = helper.load_model(model_path_2)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image, conf=confidence)
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                res2 = model_2.predict(res_plotted, conf=confidence)
                boxes2 = res2[0].boxes
                res_plotted2 = res2[0].plot()
                st.image(res_plotted2, caption='Detected Image', use_column_width=True)
                                     
                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            x_min, y_min, x_max, y_max, confidence, class_id = box.data.cpu().numpy()[0]
                            st.write(f"Bounding Box: ({x_min}, {y_min}) -> ({x_max}, {y_max})")
                            st.write(f"Confidence: {confidence}")
                            st.write(f"Class ID: {class_id}")
                            class_id_int = int(class_id)
                            audio_file_path = f"audios/class{class_id_int}.mp3"
                            st.audio(audio_file_path, format="audio/mp3", start_time=0, autoplay=True)
                            time.sleep(3)
                        for box in boxes2:
                            x_min, y_min, x_max, y_max, confidence, class_id = box.data.cpu().numpy()[0]
                            st.write(f"Bounding Box: ({x_min}, {y_min}) -> ({x_max}, {y_max})")
                            st.write(f"Confidence: {confidence}")
                            st.write(f"Class ID: {class_id}")
                except Exception as ex:
                    st.error("No image is uploaded yet!")
                    st.error(ex)


elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model, model_2)

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model, model_2)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model, model_2)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model, model_2)

else:
    st.error("Please select a valid source type!")
