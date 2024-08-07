

import os
import librosa
import soundfile as sf  # 讀寫音訊檔案的庫
from pathlib import Path
def load_audio(filepath, target_sr):
    # 載入音訊檔案
    y, sr = librosa.load(filepath, sr=target_sr)
    return y, sr

# 儲存音訊檔案
def save_audio(filepath, audio, sr):
    sf.write(filepath, audio, sr)


dir = os.getcwd()
target_sr = 16000

wav_path="0.2.1/ImTong"
for file in os.listdir(wav_path):
    if file.endswith(".wav"):
        audio, sr = load_audio(os.path.join(wav_path, file), target_sr)
        save_audio(os.path.join(wav_path, file), audio, sr)


