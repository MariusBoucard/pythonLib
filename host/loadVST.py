
import soundfile
from pedalboard import load_plugin, Pedalboard
import numpy as np
import matplotlib.pyplot as plt
from Saturations.Saturations import add_tanh_harmonics, add_cubic_harmonics, add_fullrect_harmonics, add_asym_clip

#audio, sample_rate = soundfile.read('10 Topin.wav')

duration = 2.0  # seconds
sample_rate = 44100
frequency = 440  # Hz (A4)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
mono = 0.5 * np.sin(2 * np.pi * frequency * t).astype(np.float32)
audio = np.stack([mono, mono], axis=-1) 
effect = load_plugin("./host/CHANNEV.vst3")
#effect = load_plugin("./Inf EQ.vst3")
#print(effect.parameters.keys())
neutral_params = {
    'bypass': 0,
    'mic_pre_db': 0.0,
    'pre_low_db': 0.0,
    'pre_high_db': 0.0,
    'pre_hipass_hz': 20.0,
    'pre_lowpass_khz': 20.0,
    'de_esser_threshold_db': 0.0,
    'de_esser_release_ms': 100.0,
    'de_esser_mix': 0.0,
    'line_amp_db': 0.0,
    'low_gain_db': 0.0,
    'low_freq_hz': 100.0,
    'low_mid_gain_db': 0.0,
    'low_mid_freq_hz': 500.0,
    'high_mid_gain_db': 0.0,
    'high_mid_freq_khz': 3.0,
    'high_gain_db': 0.0,
    'high_freq_khz': 10.0,
    'eq_hipass_hz': 20.0,
    'eq_lowpass_khz': 20.0,
    'compressor_threshold_db': 0.0,
    'compressor_ratio': 1.0,
    'compressor_release_ms': 100.0,
    'compressor_gain_db': 0.0,
    'compressor_mix': 0.0,
    'limiter_threshold_db': 0.0,
    'limiter_release_ms': 100.0,
    'limiter_gain_db': 0.0,
    'limiter_mix': 0.0,
    'tape_drive_db': 0.0,
    'output_db': 0.0,
    'trim_db': 0.0,
    'pre_phase': 0,
    'pre_pad': 0,
    'pre_in': 1,
    'de_esser_peak': 0,
    'de_esser_in': 0,
    'de_esser_soft': 0,
    'low_peak': 0,
    'low_mid_q': 1.0,
    'high_mid_q': 1.0,
    'high_peak': 0,
    'equalizer_in': 1,
    'compressor_in': 0,
    'compressor_sidechain': 0,
    'limiter_in': 0,
    'limiter_sidechain': 0,
}

# Set all parameters to neutral values
for param, value in neutral_params.items():
    if param in effect.parameters:
        effect.parameters.param = value


board = Pedalboard(
[effect]
)

effected = board(audio, sample_rate)

mono_harm = add_tanh_harmonics(mono, amount=1.0)
mono_harm = add_cubic_harmonics(mono_harm, amount=1.0)
# mono_harm = add_fullrect_harmonics(mono_harm, amount=0.1)
mono_harm = add_asym_clip(mono_harm, amount=0.07)

harmoAdded = np.stack([mono_harm, mono_harm], axis=-1)

if audio.ndim > 1:
    audio_plot = audio[:, 0]
    effected_plot = effected[:, 0]
else:
    audio_plot = audio
    effected_plot = effected


def compute_fft(signal, sr):
    fft = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(len(signal), 1/sr)
    return freq, np.abs(fft)

freq, orig_fft = compute_fft(audio_plot, sample_rate)
_, effected_fft = compute_fft(effected_plot, sample_rate)
_,  harm_fft = compute_fft(mono_harm, sample_rate)


# Plot
plt.figure(figsize=(12, 6))
plt.semilogx(freq, 20 * np.log10(orig_fft + 1e-6), label='Original')
plt.semilogx(freq, 20 * np.log10(effected_fft + 1e-6), label='Processed')
plt.semilogx(freq, 20 * np.log10(harm_fft + 1e-6), label='Harmonics Added', linestyle='--')
plt.title('FFT Before and After Plugin')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.legend()
plt.grid(True)
plt.show()



