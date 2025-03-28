import struct

CHUNKS_TO_REMOVE = {b'tEXt', b'iTXt', b'zTXt', b'eXIf'}

def anonymize_png(input_path, output_path):
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        # Przepisujemy sygnaturę PNG
        signature = infile.read(8)
        outfile.write(signature)

        while True:
            header = infile.read(8)
            if len(header) < 8:
                break

            length, chunk_type = struct.unpack('>I4s', header)
            data = infile.read(length)
            crc = infile.read(4)

            if chunk_type in CHUNKS_TO_REMOVE:
                print(f"🚫 Removing chunk: {chunk_type.decode('ascii')}")
                continue  # pomijamy

            # Inne chunk’i — zapisujemy normalnie
            outfile.write(struct.pack('>I4s', length, chunk_type))
            outfile.write(data)
            outfile.write(crc)

            if chunk_type == b'IEND':
                break

    print(f"✅ Anonymized PNG saved to: {output_path}")
