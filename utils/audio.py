import os
import librosa
import pandas as pd
import numpy as np


# Features to extract (modelled off GTZAN dataset):
# 0. length of analysed segments
# 1. Chroma stft (short term fourier transform)
# 2. rms (root mean square)
# 3. spectral centroid
# 4. spectral bandwidth
# 5. rolloff
# 6. zero crossing rate
# 7. harmony
# 8. perceptr
# 9. tempo
# 10. mfccs


def extract_audio_features(filepath: str, song_name: str = None, chunk_length: float or int = None, num_chunks: int = 1,
                           n_fft: int = 2048, hop_length: int = 512) -> (pd.DataFrame, list):
    assert ((num_chunks > 1) and (chunk_length is not None)) is False, "either chunk_length or num_chunks must be used"
    assert num_chunks > 0, "num chunks cannot be negative"

    filepath = os.path.abspath(filepath)
    filename = filepath.split(os.sep)[-1]
    y, sample_rate = librosa.load(filepath)
    duration_s = np.shape(y)[0] / sample_rate

    if chunk_length:
        num_chunks = int(np.ceil(duration_s / chunk_length))
    if num_chunks > 1:
        chunk_length = duration_s / num_chunks
    else:
        chunk_length = duration_s

    final_df = None
    cols = []
    for chunk in range(num_chunks):
        name = filename if num_chunks == 1 else f"{filename}_{chunk}"
        billboard_name = song_name if num_chunks == 1 else f"{song_name}_{chunk}"
        offset = chunk_length * chunk
        audio, sr = librosa.load(filepath, offset=offset, duration=chunk_length)
        audio, _ = librosa.effects.trim(audio)
        # stft = np.abs(librosa.stft(audio, n_fft=n_fft, hop_length=hop_length))
        chroma_stft = librosa.feature.chroma_stft(audio, sr=sr, hop_length=hop_length, n_fft=n_fft)
        chroma_stft_mean = np.mean(chroma_stft)
        chroma_stft_var = np.var(chroma_stft)
        rms = librosa.feature.rms(y=audio)
        rms_mean = np.mean(rms)
        rms_var = np.var(rms)
        spectral_centroid = librosa.feature.spectral_centroid(audio, sr=sr)[0]
        spectral_centroid_mean = np.mean(spectral_centroid)
        spectral_centroid_var = np.var(spectral_centroid)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(audio)
        spectral_bandwidth_mean = np.mean(spectral_bandwidth)
        spectral_bandwidth_var = np.var(spectral_bandwidth)
        rolloff = librosa.feature.spectral_rolloff(audio)
        rolloff_mean = np.mean(rolloff)
        rolloff_var = np.mean(rolloff)
        zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)
        zero_crossing_rate_mean = np.mean(zero_crossing_rate)
        zero_crossing_rate_var = np.var(zero_crossing_rate)
        harmony, perceptr = librosa.effects.hpss(audio)
        harmony_mean = np.mean(harmony)
        harmony_var = np.var(harmony)
        perceptr_mean = np.mean(perceptr)
        perceptr_var = np.var(perceptr)
        tempo, _ = librosa.beat.beat_track(audio, sr=sr)
        mfccs = librosa.feature.mfcc(audio, sr=sr)
        mfccs_mean = [np.mean(mfcc) for mfcc in mfccs]
        mfccs_var = [np.var(mfcc) for mfcc in mfccs]
        cols = ['billboard_name', 'filename', 'length', 'chroma_stft_mean', 'chroma_stft_var', 'rms_mean', 'rms_var',
                'spectral_centroid_mean', 'spectral_centroid_var', 'spectral_bandwidth_mean', 'spectral_bandwidth_var',
                'rolloff_mean', 'rolloff_var', 'zero_crossing_rate_mean', 'zero_crossing_rate_var', 'harmony_mean',
                'harmony_var', 'perceptr_mean', 'perceptr_var', 'tempo']
        data = [billboard_name, name, chunk_length, chroma_stft_mean, chroma_stft_var, rms_mean, rms_var,
                spectral_centroid_mean, spectral_centroid_var, spectral_bandwidth_mean, spectral_bandwidth_var,
                rolloff_mean, rolloff_var, zero_crossing_rate_mean, zero_crossing_rate_var, harmony_mean, harmony_var,
                perceptr_mean, perceptr_var, tempo]
        for m in range(len(mfccs_mean)):
            cols.append(f"mfcc{m + 1}_mean")
            cols.append(f"mfcc{m + 1}_var")
            data.append(mfccs_mean[m])
            data.append(mfccs_var[m])
        df = pd.DataFrame(columns=cols, data=[data])
        final_df = df if final_df is None else pd.concat([final_df, df], axis=0)
    return final_df, cols
