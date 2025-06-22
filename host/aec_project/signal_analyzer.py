# aec_project/signal_analyzer.py
import numpy as np
from typing import Tuple

class SignalAnalyzer:
    """Provides methods for signal analysis."""
    
    @staticmethod
    def compute_fft(signal: np.ndarray, sample_rate: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Computes the real FFT of a 1D signal.

        Args:
            signal (np.ndarray): The 1D input signal.
            sample_rate (int): The sample rate of the signal.

        Returns:
            Tuple[np.ndarray, np.ndarray]: A tuple containing the frequency bins
                                           and the corresponding magnitudes.
        """
        if signal.ndim > 1:
            # If stereo, use the first channel for FFT analysis
            signal = signal[:, 0]
            
        fft_values = np.fft.rfft(signal)
        frequencies = np.fft.rfftfreq(len(signal), 1 / sample_rate)
        magnitudes = np.abs(fft_values)
        return frequencies, magnitudes