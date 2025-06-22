# aec_project/audio_generator.py
import numpy as np

class SignalGenerator:
    """Generates various types of audio signals."""
    def __init__(self, duration: float, sample_rate: int):
        """
        Initializes the SignalGenerator.

        Args:
            duration (float): The duration of the signal in seconds.
            sample_rate (int): The sample rate of the signal in Hz.
        """
        self.duration = duration
        self.sample_rate = sample_rate
        self.num_samples = int(self.sample_rate * self.duration)

    def generate_sine(self, frequency: float, amplitude: float = 0.5) -> np.ndarray:
        """
        Generates a stereo sine wave.

        Args:
            frequency (float): The frequency of the sine wave in Hz.
            amplitude (float): The peak amplitude of the signal.

        Returns:
            np.ndarray: A stereo audio signal as a NumPy array.
        """
        t = np.linspace(0, self.duration, self.num_samples, endpoint=False)
        mono_signal = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
        # Stack the mono signal to create a stereo signal
        stereo_signal = np.stack([mono_signal, mono_signal], axis=-1)
        return stereo_signal