from png_parser import read_chunks
from anonymizer import anonymize_png
from fourier import show_fft_spectrum

if __name__ == "__main__":
    input_file = "assets/goat.png"
    output_file = "assets/goat_anonymized.png"

    print("=== Original file ===")
    read_chunks(input_file)

    print("\n=== Anonymizing... ===")
    anonymize_png(input_file, output_file)

    print("\n=== Anonymized file ===")
    read_chunks(output_file)

    show_fft_spectrum("assets/goat.png")
