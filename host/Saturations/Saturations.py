import numpy as np

def add_tanh_harmonics(signal, amount=1.0, bias=0.0):
    """
    Applies tanh saturation with an adjustable bias to control even harmonics.

    Args:
        signal (np.ndarray): The input audio signal.
        amount (float): The drive amount for the saturation. Controls the overall
                        intensity of the distortion.
        bias (float): A DC offset applied before saturation to introduce
                      asymmetry and control even harmonics. 
                      Positive values saturate the top half of the wave more,
                      negative values saturate the bottom half more.
                      Recommended range: -1.0 to 1.0.

    Returns:
        np.ndarray: The saturated audio signal.
    """
    # Apply the bias to introduce asymmetry
    biased_signal = signal + bias
    
    # Apply the tanh saturation
    saturated_signal = np.tanh(amount * biased_signal)
    
    # IMPORTANT: Remove the new DC offset created by the asymmetric clipping.
    # If we don't do this, the waveform will not be centered on 0, which can
    # cause issues with other processors and create clicks.
    output_signal = saturated_signal - np.mean(saturated_signal)
    
    return output_signal
def add_cubic_harmonics(audio, amount=1.0):
    """Add cubic nonlinearity for odd harmonics."""
    return audio - amount * (audio ** 3) / 3

def add_fullrect_harmonics(audio, amount=1.0):
    """Full-wave rectification for even harmonics."""
    return amount * np.abs(audio) + (1 - amount) * audio

def add_asym_clip(audio, amount=1.0):
    """Asymmetric clipping for both even and odd harmonics."""
    return np.clip(audio + amount * (audio ** 2), -1, 1)
