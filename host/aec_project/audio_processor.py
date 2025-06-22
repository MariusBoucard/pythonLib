# aec_project/audio_processor.py
from pedalboard import load_plugin, Pedalboard
import numpy as np
import os

# Assuming Saturations.py is in a reachable path
from Saturations.Saturations import add_tanh_harmonics, add_cubic_harmonics, add_fullrect_harmonics, add_asym_clip

class VSTProcessor:
    """A processor for applying VST plugins using pedalboard."""
    def __init__(self, plugin_path: str):
        if not os.path.exists(plugin_path):
            raise FileNotFoundError(f"Plugin not found at path: {plugin_path}")
        self.effect = load_plugin(plugin_path)
        self.board = Pedalboard([self.effect])

    def set_parameters(self, params: dict):
        """Sets multiple parameters on the loaded VST plugin."""
        for param_name, value in params.items():
            if hasattr(self.effect, param_name):
                self.effect.parameters.param_name= value
              #  setattr(self.effect, param_name, value)

    def process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Processes an audio signal through the VST plugin."""
        return self.board(audio, sample_rate)

class HarmonicProcessor:
    """A processor for adding custom harmonic distortion."""
    def __init__(self, tanh_amount=1.0,tanh_bias=0.0, cubic_amount=1.0, fullrect_amount=0.0, asym_clip_amount=0.07):
        self.params = {
            'tanh': tanh_amount,
            'tanh_bias': tanh_bias,
            'cubic': cubic_amount,
            'fullrect': fullrect_amount,
            'asym': asym_clip_amount
        }

    def process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Applies a series of harmonic distortions.
        Assumes input is stereo and applies distortion to each channel.
        """
        processed_channels = []
        # Process each channel independently
        for i in range(audio.shape[1]):
            channel = audio[:, i]
            channel = add_asym_clip(channel, amount=self.params['asym'])
            channel = add_tanh_harmonics(channel, amount=self.params['tanh'], bias=self.params['tanh_bias'])
            channel = add_cubic_harmonics(channel, amount=self.params['cubic'])
            channel = add_fullrect_harmonics(channel, amount=self.params['fullrect'])
            processed_channels.append(channel)
        
        return np.stack(processed_channels, axis=-1)

def get_channev_neutral_params() -> dict:
    """Returns a dictionary of neutral parameters for the CHANNEV.vst3 plugin."""
    return {
        'bypass': 0, 'mic_pre_db': 0.0, 'pre_low_db': 0.0, 'pre_high_db': 0.0,
        'pre_hipass_hz': 20.0, 'pre_lowpass_khz': 20.0, 'de_esser_threshold_db': 0.0,
        'de_esser_release_ms': 100.0, 'de_esser_mix': 0.0, 'line_amp_db': 0.0,
        'low_gain_db': 0.0, 'low_freq_hz': 100.0, 'low_mid_gain_db': 0.0,
        'low_mid_freq_hz': 500.0, 'high_mid_gain_db': 0.0, 'high_mid_freq_khz': 3.0,
        'high_gain_db': 0.0, 'high_freq_khz': 10.0, 'eq_hipass_hz': 20.0,
        'eq_lowpass_khz': 20.0, 'compressor_threshold_db': 0.0, 'compressor_ratio': 1.0,
        'compressor_release_ms': 100.0, 'compressor_gain_db': 0.0, 'compressor_mix': 0.0,
        'limiter_threshold_db': 0.0, 'limiter_release_ms': 100.0, 'limiter_gain_db': 0.0,
        'limiter_mix': 0.0, 'tape_drive_db': 0.0, 'output_db': 0.0, 'trim_db': 0.0,
        'pre_phase': 0, 'pre_pad': 0, 'pre_in': 1, 'de_esser_peak': 0,
        'de_esser_in': 0, 'de_esser_soft': 0, 'low_peak': 0, 'low_mid_q': 1.0,
        'high_mid_q': 1.0, 'high_peak': 0, 'equalizer_in': 1, 'compressor_in': 0,
        'compressor_sidechain': 0, 'limiter_in': 0, 'limiter_sidechain': 0,
    }