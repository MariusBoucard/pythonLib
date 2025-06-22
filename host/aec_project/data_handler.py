# aec_project/data_handler.py
import numpy as np

class DataHandler:
    """Handles saving and loading of analysis data."""

    @staticmethod
    def save_analysis_data(filepath: str, **data_arrays):
        """
        Saves multiple NumPy arrays to a single compressed .npz file.

        Args:
            filepath (str): The path to save the file to.
            **data_arrays: Keyword arguments where keys are the names and
                           values are the NumPy arrays to save.
        """
        np.savez(filepath, **data_arrays)
        print(f"Analysis data saved to {filepath}")

    @staticmethod
    def load_analysis_data(filepath: str) -> dict:
        """
        Loads data from a .npz file into a dictionary of arrays.

        Args:
            filepath (str): The path to the .npz file.

        Returns:
            dict: A dictionary where keys are the names of the saved arrays
                  and values are the loaded NumPy arrays.
        """
        return np.load(filepath)