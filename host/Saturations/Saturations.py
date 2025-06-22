import numpy as np

def add_tanh_harmonics(audio, amount=1.0):
    """Apply tanh waveshaping for soft clipping/harmonics."""
    return np.tanh(amount * audio)

def add_cubic_harmonics(audio, amount=1.0):
    """Add cubic nonlinearity for odd harmonics."""
    return audio - amount * (audio ** 3) / 3

def add_fullrect_harmonics(audio, amount=1.0):
    """Full-wave rectification for even harmonics."""
    return amount * np.abs(audio) + (1 - amount) * audio

def add_asym_clip(audio, amount=1.0):
    """Asymmetric clipping for both even and odd harmonics."""
    return np.clip(audio + amount * (audio ** 2), -1, 1)
