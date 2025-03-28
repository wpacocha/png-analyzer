import struct

PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'

def read_chunks(file_path):
    with open(file_path, 'rb') as f:
        signature = f.read(8)
        if signature != PNG_SIGNATURE:
            raise ValueError("This is not a valid PNG file.")

        print("✅ Valid PNG file detected.\n")

        while True:
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                break

            length, chunk_type = struct.unpack('>I4s', chunk_header)
            chunk_data = f.read(length)
            crc = f.read(4)

            chunk_type_str = chunk_type.decode('ascii')
            print(f"🔹 Chunk: {chunk_type_str}, Length: {length}")

            if chunk_type == b'IHDR':
                parse_IHDR(chunk_data)

            if chunk_type == b'IEND':
                print("\n🛑 End of PNG file.")
                break
            if chunk_type == b'tEXt':
                parse_tEXt(chunk_data)
            if chunk_type == b'iTXt':
                parse_iTXt(chunk_data)
            elif chunk_type == b'zTXt':
                parse_zTXt(chunk_data)
            elif chunk_type == b'eXIf':
                parse_eXIf(chunk_data)


def parse_tEXt(data):
    try:
        text = data.decode('latin1')  # PNG spec wymaga Latin-1
        key, value = text.split('\x00', 1)
        print(f"  📝 tEXt key: {key}")
        print(f"  📝 tEXt value: {value}")
    except Exception as e:
        print(f"  ⚠️ Failed to parse tEXt chunk: {e}")

def parse_IHDR(data):
    width, height, bit_depth, color_type, compression, filter_method, interlace = struct.unpack('>IIBBBBB', data)
    print(f"  📐 Width: {width}")
    print(f"  📐 Height: {height}")
    print(f"  🎨 Bit depth: {bit_depth}")
    print(f"  🎨 Color type: {color_type}")
    print(f"  📦 Compression: {compression}")
    print(f"  🧹 Filter method: {filter_method}")
    print(f"  🧶 Interlace method: {interlace}")

def parse_iTXt(data):
    try:
        parts = data.split(b'\x00', 5)
        if len(parts) < 6:
            print("  ⚠️ Malformed iTXt chunk.")
            return

        keyword = parts[0].decode('latin1')
        compression_flag = parts[1]
        compression_method = parts[2]
        language_tag = parts[3].decode('latin1')
        translated_keyword = parts[4].decode('utf-8')
        text_data = parts[5]

        if compression_flag == b'\x01':  # compressed
            import zlib
            text = zlib.decompress(text_data).decode('utf-8')
        else:
            text = text_data.decode('utf-8')

        print(f"  🌍 iTXt keyword: {keyword}")
        print(f"  🌍 Language: {language_tag}")
        print(f"  🌍 Translated keyword: {translated_keyword}")
        print(f"  🌍 Text: {text}")
    except Exception as e:
        print(f"  ⚠️ Failed to parse iTXt chunk: {e}")

def parse_zTXt(data):
    try:
        keyword, rest = data.split(b'\x00', 1)
        compression_method = rest[0]
        compressed_text = rest[1:]

        import zlib
        text = zlib.decompress(compressed_text).decode('latin1')

        print(f"  🗜️ zTXt keyword: {keyword.decode('latin1')}")
        print(f"  🗜️ Text: {text}")
    except Exception as e:
        print(f"  ⚠️ Failed to parse zTXt chunk: {e}")

def parse_eXIf(data):
    print(f"  📷 eXIf chunk detected, raw length: {len(data)} bytes")
