from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def show_fft_spectrum(image_path):
    image = Image.open(image_path).convert('L')
    image_data = np.array(image)

    fft = np.fft.fft2(image_data)
    fft_shifted = np.fft.fftshift(fft)
    magnitude_spectrum = 20 * np.log(np.abs(fft_shifted) + 1)

    plt.figure(figsize=(8, 6))
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.title("Fourier Spectrum (Magnitude)")
    plt.axis('off')
    plt.show()
