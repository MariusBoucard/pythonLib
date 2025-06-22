# plot_results.py
import matplotlib.pyplot as plt
import numpy as np
import argparse
from aec_project.data_handler import DataHandler

def plot_fft_comparison(data: dict):
    """
    Plots the FFT data from the loaded dictionary.

    Args:
        data (dict): A dictionary containing FFT data arrays.
    """
    plt.figure(figsize=(12, 6))
    
    # Convert magnitudes to dB, adding a small epsilon to avoid log(0)
    epsilon = 1e-9
    
    plt.semilogx(data['freq_axis'], 20 * np.log10(data['original_fft'] + epsilon), label='Original')
    plt.semilogx(data['freq_axis'], 20 * np.log10(data['effected_vst_fft'] + epsilon), label='VST Processed')
    plt.semilogx(data['freq_axis'], 20 * np.log10(data['effected_harm_fft'] + epsilon), label='Harmonics Added', linestyle='--')
    
    plt.title('FFT Comparison of Audio Signals')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.legend()
    plt.grid(True)
    plt.ylim(bottom=-60) # Set a floor for better visualization
    plt.show()

def main():
    """Main function to load data and plot."""
    parser = argparse.ArgumentParser(description="Load and plot audio analysis results.")
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the .npz file containing the analysis data."
    )
    args = parser.parse_args()

    # Load the data
    handler = DataHandler()
    try:
        analysis_data = handler.load_analysis_data(args.input_file)
        print(f"Successfully loaded data from {args.input_file}")
    except FileNotFoundError:
        print(f"Error: The file {args.input_file} was not found.")
        return

    # Plot the data
    plot_fft_comparison(analysis_data)

if __name__ == "__main__":
    main()