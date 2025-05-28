import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import ifft, fft
from scipy.signal import windows, convolve, welch
from scipy.io.wavfile import write, read

# --- 1. Définition de la fonction de réponse en fréquence du filtre en cloche ---
def bell_filter_frequency_response(frequencies, center_freq, Q_factor, gain_dB):
    """
    Calcule la réponse en magnitude (en linéaire) d'un filtre en cloche.

    Args:
        frequencies (np.array): Tableau des fréquences en Hz.
        center_freq (float): Fréquence centrale du filtre en Hz (f dans votre formule).
        Q_factor (float): Facteur de qualité (q dans votre formule).
        gain_dB (float): Gain maximal du filtre en décibels (g dans votre formule,
                         représenté ici en dB pour être converti en linéaire).

    Returns:
        np.array: Réponse en magnitude linéaire pour chaque fréquence.
    """
    # Convertir le gain de dB en linéaire pour 'g'
    g_linear = 10**(gain_dB / 20.0)

    # Assurez-vous que les fréquences sont positives et non nulles pour ln(x/f)
    frequencies_safe = np.where(frequencies > 0, frequencies, 1e-10)

    # Calcul des termes de la formule on the array
    term1 = np.log(frequencies_safe / center_freq)**2
    term2 = np.log(2)
    term3 = (2 * (np.sinh(1 / (2 * Q_factor)))**2)

    # Éviter la division par zéro si Q_factor est trop grand ou 1/(2Q) est proche de 0
    # Dans ce cas, le dénominateur de sinh peut être très petit, gérant cela.
    # Pour Q = inf, sinh(0) = 0. Nous mettons une petite valeur pour éviter inf ou NaN.
    if np.abs(term3).any() < 1e-10:
        term3 = np.where(np.abs(term3) < 1e-10, 1e-10, term3) # Remplace les valeurs très petites par 1e-10

    exponent = -(term1 * term2) / term3

    # Calcul de la réponse en magnitude
    magnitude_response = g_linear * np.exp(exponent)
    for a in range(len(magnitude_response)):
        magnitude_response[a] = magnitude_response[a]+1
    return magnitude_response

# --- 2. Paramètres du signal et du filtre ---
sample_rate = 44100  # Fréquence d'échantillonnage en Hz
duration = 3         # Durée du signal audio en secondes
num_samples = int(sample_rate * duration)

# Paramètres de votre filtre en cloche
center_freq = 1000   # Fréquence centrale de 1 kHz
Q_factor = 10         # Facteur de qualité, plus élevé = cloche plus étroite
gain_dB = 12         # Gain de 12 dB (boost)

# Ordre du filtre FIR. Un ordre plus élevé = meilleure approximation de la réponse en fréquence
# mais un calcul plus lourd. Choisissez une puissance de 2 pour l'IFFT pour l'efficacité.
# Un ordre de 1024 ou 2048 est un bon point de départ pour une cloche.
fir_order = 2048

# --- 3. Génération de la réponse impulsionnelle du FIR ---

# Créez un tableau de fréquences pour l'IFFT
# La longueur de l'IFFT doit être au moins l'ordre du FIR
fft_length = fir_order

# Les fréquences s'étendent de 0 à sample_rate/2 (Nyquist)
# et sont symétriques pour les fréquences négatives pour l'IFFT
frequencies_for_fft = np.fft.fftfreq(fft_length, d=1/sample_rate)

# Réponse en magnitude calculée par notre fonction
magnitude_spectrum = bell_filter_frequency_response(
    np.abs(frequencies_for_fft), center_freq, Q_factor, gain_dB
)

# Pour un FIR à phase linéaire, nous prenons une phase nulle (ou un délai constant)
# La réponse en fréquence complexe est simplement la magnitude, car la phase est nulle pour un filtre idéal
# (ou linéaire, mais pour la conception d'un FIR symétrique, on part de là).
# Note: Pour des filtres FIR à phase linéaire, l'IFFT d'une réponse en magnitude réelle
# donnera une réponse impulsionnelle symétrique autour du centre.
complex_frequency_response = magnitude_spectrum

# Appliquez l'IFFT pour obtenir la réponse impulsionnelle
# Le résultat de l'IFFT peut être complexe, mais pour un filtre réel et à phase linéaire,
# la partie imaginaire devrait être négligeable.
ideal_impulse_response = np.real(ifft(complex_frequency_response))

# Centrez la réponse impulsionnelle pour une phase linéaire (décalage circulaire)
# Cela déplace le pic de la réponse impulsionnelle au milieu, ce qui correspond à un délai.
ideal_impulse_response = np.roll(ideal_impulse_response, fft_length // 2)

# Appliquez une fenêtre (par exemple, Blackman) pour réduire les artefacts de troncature
# et obtenir les coefficients FIR finaux.
window = windows.blackman(fir_order)
fir_coefficients = ideal_impulse_response[:fir_order] * window

# Normalisez les coefficients pour éviter un changement de volume global indésirable si le gain moyen n'est pas 1.
# Cette étape est optionnelle et dépend de l'effet voulu. Pour un "boost", on ne normalise pas toujours
# pour maintenir le gain_dB demandé. Cependant, si le gain moyen est trop élevé, ça peut saturer.
#fir_coefficients /= np.sum(fir_coefficients) # Décommentez si vous voulez que le gain DC soit 0dB

# --- 4. Génération d'un signal audio de test (bruit blanc) ---
# Le bruit blanc est idéal pour tester la réponse en fréquence d'un filtre.
test_audio = np.random.randn(num_samples).astype(np.float32)
# Normalisation du bruit blanc pour éviter la saturation
test_audio = 0.5 * test_audio / np.max(np.abs(test_audio))

# --- 5. Application du filtre au signal audio ---
print(f"Application du filtre FIR d'ordre {fir_order} par convolution...")
filtered_audio = convolve(test_audio, fir_coefficients, mode='same')
print("Filtrage terminé.")

# Normalisation du signal filtré pour éviter le clipping lors de la lecture/écriture
max_val = np.max(np.abs(filtered_audio))
if max_val > 1.0:
    filtered_audio = filtered_audio / max_val * 0.9 # Normalise à 90% de la plage max

# --- 6. Sauvegarde et lecture du signal audio ---
output_filename_original = "test_audio_original.wav"
output_filename_filtered = "test_audio_filtered.wav"

write(output_filename_original, sample_rate, (test_audio * 32767).astype(np.int16)) # Convertir en int16 pour WAV
write(output_filename_filtered, sample_rate, (filtered_audio * 32767).astype(np.int16))

print(f"Signal original sauvegardé sous : {output_filename_original}")
print(f"Signal filtré sauvegardé sous : {output_filename_filtered}")

# --- 7. Visualisation (Optionnel) ---
plt.figure(figsize=(15, 10))

# Spectre de la réponse impulsionnelle (pour vérifier la forme du filtre)
plt.subplot(3, 1, 1)
plt.plot(np.fft.fftfreq(fir_order, d=1/sample_rate)[:fir_order//2],
         20 * np.log10(np.abs(fft(fir_coefficients))[:fir_order//2]))
plt.title('Réponse en Fréquence du Filtre FIR (en dB)')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Gain (dB)')
plt.grid(True)
plt.axvline(center_freq, color='r', linestyle='--', label=f'Fréquence Centrale ({center_freq} Hz)')
plt.legend()
plt.xlim(20, sample_rate/2)
plt.xscale('log')


# Spectre du signal original et filtré
# Utilisation de la méthode de Welch pour une estimation plus lisse du PSD
f_orig, Pxx_orig = welch(test_audio, fs=sample_rate, nperseg=1024)
f_filt, Pxx_filt = welch(filtered_audio, fs=sample_rate, nperseg=1024)

plt.subplot(3, 1, 2)
plt.semilogx(f_orig, 10 * np.log10(Pxx_orig), label='Original')
plt.semilogx(f_filt, 10 * np.log10(Pxx_filt), label='Filtré')
plt.title('Spectre de Puissance du Signal Audio (Original vs. Filtré)')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Densité Spectrale de Puissance (dB/Hz)')
plt.grid(True)
plt.legend()
plt.xlim(20, sample_rate/2)

# Affichage des coefficients du FIR
plt.subplot(3, 1, 3)
plt.plot(fir_coefficients)
plt.title('Coefficients de la Réponse Impulsionnelle du FIR')
plt.xlabel('Échantillon')
plt.ylabel('Amplitude')
plt.grid(True)

plt.tight_layout()
plt.show()