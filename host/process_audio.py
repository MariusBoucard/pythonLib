# process_audio.py
import numpy as np
from aec_project.audio_generator import SignalGenerator
from aec_project.audio_processor import VSTProcessor, HarmonicProcessor, get_channev_neutral_params
from aec_project.signal_analyzer import SignalAnalyzer
from aec_project.data_handler import DataHandler

# --- Configuration ---
DURATION = 2.0
SAMPLE_RATE = 44100
FREQUENCY = 500  # Hz (A4)
PLUGIN_PATH = "./vst/CHANNEV.vst3"
OUTPUT_FILE = "analysis_results.npz"

def main():
    """Main processing pipeline."""
    # 1. Generate Audio
    generator = SignalGenerator(duration=DURATION, sample_rate=SAMPLE_RATE)
    original_audio = generator.generate_sine(frequency=FREQUENCY)

    # 2. Process Audio with VST
    vst_processor = VSTProcessor(plugin_path=PLUGIN_PATH)
    neutral_params = get_channev_neutral_params()
    vst_processor.set_parameters(neutral_params)
    effected_audio = vst_processor.process(original_audio, SAMPLE_RATE)
    
    # 3. Process Audio with Custom Harmonics
    harmonic_processor = HarmonicProcessor(tanh_amount=1.0, tanh_bias=-0.5,cubic_amount=0.0, fullrect_amount=0.0, asym_clip_amount=0.02)
    harmonic_audio = harmonic_processor.process(original_audio, SAMPLE_RATE)

    # 4. Analyze Signals
    analyzer = SignalAnalyzer()
    freq_axis, orig_fft = analyzer.compute_fft(original_audio, SAMPLE_RATE)
    _, effected_fft = analyzer.compute_fft(effected_audio, SAMPLE_RATE)
    _, harm_fft = analyzer.compute_fft(harmonic_audio, SAMPLE_RATE)

    # 5. Save Data for Later Use
    handler = DataHandler()
    handler.save_analysis_data(
        OUTPUT_FILE,
        freq_axis=freq_axis,
        effected_harm_fft=harm_fft,
        effected_vst_fft=effected_fft,
        original_fft=orig_fft,
    )

if __name__ == "__main__":
    main()