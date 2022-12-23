import os
import sys
import subprocess
import whisper
from whisper.utils import write_vtt
model = whisper.load_model("base")

def video2mp3(video_file, output_ext="mp3"):
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"

def transcribe(input_video,nn):
    audio_file = video2mp3(input_video)
    options = dict(language=nn,beam_size=5, best_of=5,fp16=False)
    transcribe_options = dict(task="transcribe", **options)
    result = model.transcribe(audio_file,**transcribe_options)
    output_dir = ''
    audio_path = audio_file.split(".")[0]
    with open(os.path.join(output_dir, audio_path + ".vtt"), "w",encoding='utf-8') as vtt:
      write_vtt(result["segments"], file=vtt)
    subtitle = audio_path + ".vtt"
    output_video = audio_path + "_subtitled.mp4"
    subprocess.call(["ffmpeg", "-i", input_video , "-vf", f"subtitles={subtitle}:force_style='FontName=Arial,FontSize=24'", 
                f"{output_video}"], 
                stdout=subprocess.DEVNULL,
                 stderr=subprocess.STDOUT)
    return output_video

def translate(input_video):
    audio_file = video2mp3(input_video)
    options = dict(beam_size=5, best_of=5,fp16=False)
    #transcribe_options = dict(task="transcribe", **options)
    translate_options = dict(task="translate", **options)
    result = model.transcribe(audio_file,**translate_options)
    output_dir = ''
    audio_path = audio_file.split(".")[0]

    with open(os.path.join(output_dir, audio_path + ".vtt"), "w",encoding='utf-8') as vtt:
      write_vtt(result["segments"], file=vtt)
    subtitle = audio_path + ".vtt"
    output_video = audio_path + "_subtitled.mp4"
    #os.system(f"ffmpeg -i {input_video} -vf subtitles={subtitle} {output_video}")
    subprocess.call(["ffmpeg", "-i", input_video , "-vf", f"subtitles={subtitle}:force_style='FontName=Arial,FontSize=24'", f"{output_video}"], 
                stdout=subprocess.DEVNULL,
                 stderr=subprocess.STDOUT)
    os.remove(subtitle)
    os.remove(audio_file)
    return output_video


import streamlit as st
import time
from PIL import Image
st.set_page_config(
    page_title="My App_Subtitle Video!",
    page_icon="😎",
    layout="wide"
)

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://thuthuatnhanh.com/wp-content/uploads/2019/04/hinh-nen-thien-ha-milky-way.jpg");
background-size: cover;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Wellcom to subtitle app by Cam Tu</h1>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html=True)
url = st.text_input("Nhập đường dẫn tới file video của bạn:")
convert = st.button ('Subtitle video')
with st.sidebar:
    st.header('Menu')
    language = st.selectbox("Chọn ngôn ngữ của video input",('Afrikaans',
    'Arabic',
    'Azerbaijani',
    'Belarusian',
    'Bulgarian',
    'Bengali',
    'Bosnian',
    'Catalan',
    'Cebuano',
    'Czech',
    'Welsh',
    'Danish',
    'German',
    'Greek',
    'English',
    'Esperanto',
    'Spanish',
    'Estonian',
    'Basque',
    'Persian',
    'Finnish',
    'French',
    'Irish',
    'Galician',
    'Gujarati',
    'Hausa',
    'Hindi',
    'Hmong',
    'Croatian',
    'Haitian Creole',
    'Hungarian',
    'Armenian',
    'Indonesian',
    'Igbo',
    'Icelandic',
    'Italian',
    'Hebrew',
    'Japanese',
    'Javanese',
    'Georgian',
    'Kazakh',
    'Khmer',
    'Kannada',
    'Korean',
    'Latin',
    'Lao',
    'Lithuanian',
    'Latvian',
    'Malagasy',
    'Maori',
    'Macedonian',
    'Malayalam',
    'Mongolian',
    'Marathi',
    'Malay',
    'Maltese',
    'Myanmar (Burmese)',
    'Nepali',
    'Dutch',
    'Norwegian',
    'Chichewa',
    'Punjabi',
    'Polish',
    'Portuguese',
    'Romanian',
    'Russian',
    'Sinhala',
    'Slovak',
    'Slovenian',
    'Somali',
    'Albanian',
    'Serbian',
    'Sesotho',
    'Sudanese',
    'Swedish',
    'Swahili',
    'Tamil',
    'Telugu',
    'Tajik',
    'Thai',
    'Filipino',
    'Turkish',
    'Ukrainian',
    'Urdu',
    'Uzbek',
    'Vietnamese',
    'Yiddish',
    'Yoruba',
    'Chinese (Simplified)',
    'Chinese (Traditional)',
    'Zulu'))
    choice = st.radio('Bạn có muốn dịch sang tiếng anh không?', ('Có','Không'))
col1, col2 = st.columns(2)
with col1:
    st.header('Input')
    st.write(language)
    if url == '':
        image = Image.open('icon.jpg')
        st.image(image, caption='Video chưa được tải lên')
    else:
        video_file = open(url, 'rb')
        video_input = video_file.read()
        st.video(video_input)
with col2:
    st.header('Output')
    if choice == 'Có':
        st.write('English')
    else:
        st.write(language)
    if convert:
        with st.spinner('Đang chạy'):
            time.sleep(10)
        if choice == 'Có':
            output = translate(url)
        else:
            output = transcribe(url,language.lower())
        video_file = open(output, 'rb')
        video_input = video_file.read()
        st.video(video_input)