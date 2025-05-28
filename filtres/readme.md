# Audio Filter Toolkit

This repository, located in the filtre directory, contains Python scripts designed for applying custom audio filters. It uses the Fast Fourier Transform (FFT) and Inverse Fast Fourier Transform (IFFT) to convert mathematical functions (representing desired frequency responses) into Finite Impulse Response (FIR) filter coefficients. These FIR filters are then applied to audio signals through convolution.
How It Works: The FIR Filter Design Process

Our approach leverages the power of digital signal processing to create and apply unique audio filters. Here's a breakdown of the key steps:
## 1. Defining the Filter's Frequency Response

We start by defining a mathematical function in Python that describes the desired frequency response of our filter. This function dictates how different frequencies in the audio signal will be affected (e.g., boosted, cut, or passed through unchanged). For instance, a "bell" function, like the one discussed, defines a specific gain curve across a range of frequencies.
## 2. From Frequency Response to Impulse Response (IFFT)

To apply this frequency-domain design to an audio signal, we need to convert it into a time-domain representation known as an Impulse Response. This is achieved using the Inverse Fast Fourier Transform (IFFT). The IFFT takes our desired frequency response and computes a set of coefficients, which are essentially the "fingerprint" of our filter in the time domain.

For practical application with FIR filters, we typically aim for a linear phase response. This means all frequencies are delayed by the same amount, which helps preserve the signal's waveform and avoids unwanted phase distortion. Our IFFT process is configured to yield a symmetric impulse response, which naturally leads to linear phase.
## 3. Truncating and Windowing the Impulse Response

The impulse response obtained from the IFFT is theoretically infinite. To create a Finite Impulse Response (FIR) filter, we must truncate this infinite response to a finite length (known as the filter's "order").

Simply cutting off the impulse response can introduce undesirable artifacts in the filter's actual frequency response (known as "ripple"). To mitigate this, we apply a window function (e.g., Blackman, Hann) to the truncated impulse response. This smooths the transition at the filter's ends, resulting in a cleaner and more predictable frequency response. The resulting coefficients are the FIR filter coefficients.
## 4. Applying the Filter via Convolution

Finally, to apply the designed FIR filter to an audio signal, we perform a mathematical operation called convolution. Convolution combines the audio signal with the FIR filter coefficients. Conceptually, it's like sliding the filter's impulse response across the audio signal, multiplying and summing at each point. This process efficiently transforms the audio signal according to the filter's characteristics.
Usage

Each Python script in this filtre directory will implement a specific filter design.

### To use a filter:

    Run the Python script for the desired filter.
    The script will typically:
        Generate test audio (e.g., white noise).
        Design the FIR filter based on its internal mathematical function.
        Apply the filter to the test audio using convolution.
        Save both the original and filtered audio files (e.g., as .wav files).
        Optionally, display plots of the filter's frequency response and the audio spectrum.

You can then listen to the output audio files to hear the effect of the applied filter. Feel free to modify the filter parameters within each script to experiment with different sound characteristics.

# Desmos functions :

### bell :

\ g\cdot e^{-\frac{\left(\left(\left(\ln\left(\frac{x}{f}\right)\right)^{2}\ln\left(2\right)\right)\right)}{2\left(\sinh\left(\frac{1}{2q}\right)\right)^{2}}}

