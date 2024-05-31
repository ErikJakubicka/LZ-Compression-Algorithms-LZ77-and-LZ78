# LZ77 Compression Code
import math
import argparse
from PIL import Image
import numpy as np

def lz77_encode(input_sequence, window_size, lookahead_buffer_size):
    encoded_data = []
    window_start = 0

    # Calculate the number of bits needed for search buffer and look buffer
    search_buffer_bits = math.ceil(math.log2(window_size + 1))
    look_buffer_bits = math.ceil(math.log2(lookahead_buffer_size + 1))

    while window_start < len(input_sequence):
        match = find_longest_match(input_sequence, window_start, window_size, lookahead_buffer_size)
        if match:
            offset, length = match
            next_value = input_sequence[window_start + length]
            encoded_data.append((offset, length, next_value))
            window_start += length + 1
        else:
            next_value = input_sequence[window_start]
            encoded_data.append((0, 0, next_value))
            window_start += 1

    return encoded_data, len(encoded_data), search_buffer_bits, look_buffer_bits

def print_step(input_string, window_start, window_size, offset, length, next_char):
    window_highlight = input_string[window_start - offset:window_start - offset + length]
    lookahead_highlight = input_string[window_start:window_start + length]
    common_highlight = input_string[window_start:window_start + min(len(window_highlight), len(lookahead_highlight))]

    formatted_string = (
        f"{input_string[:max(0, window_start - window_size)]}\033[32m{input_string[max(0, window_start - window_size):window_start]}"
        f"\033[34m{window_highlight}\033[0m"
        f"\033[34m{lookahead_highlight[len(common_highlight):]}\033[0m"
        f"\033[37m{next_char}\033[0m{input_string[window_start + length + 1:]}"
    )
    return formatted_string

def find_longest_match(input_string, window_start, window_size, lookahead_buffer_size):
    best_offset = -1
    best_length = 0

    for offset in range(1, min(window_size, window_start) + 1):
        for length in range(1, lookahead_buffer_size + 1):
            if window_start + length >= len(input_string):
                break

            window_substring = input_string[window_start - offset:window_start - offset + length]
            lookahead_substring = input_string[window_start:window_start + length]

            if window_substring == lookahead_substring:
                if length > best_length:
                    best_offset = offset
                    best_length = length
            else:
                break

    if best_offset == -1:
        return None
    else:
        return (best_offset, best_length)

def read_hex_file(file_path):
    with open(file_path, "rb") as file:
        hex_data = file.read()
        hex_string = hex_data.hex()
    return hex_string

def select_bytes_for_compression(input_hex_string):
    selected_bytes = []
    for i in range(0, len(input_hex_string), 2):
        hex_digit = input_hex_string[i:i+2]
        decimal_value = int(hex_digit, 16)
        if 32 < decimal_value < 127:
            # Keep printable characters as-is
            selected_bytes.append(chr(decimal_value))
        else:
            # Convert non-printable characters to hexadecimal representation
            selected_bytes.append(hex_digit)
    return selected_bytes

def is_valid_hexadecimal(char):
    # Check if the character is a valid hexadecimal digit
    return char.isdigit() or ('a' <= char.lower() <= 'f')

def has_non_hexadecimal(string):
    # Iterate over each character in the string
    for char in string:
        # Check if the character is not a valid hexadecimal digit
        if not is_valid_hexadecimal(char):
            return True  # Return True if a non-hexadecimal character is found
    return False  # Return False if all characters are valid hexadecimal digits

def pack_values(search_buffer, look_buffer, next_char, search_bits, look_bits):
    # Pack values into a single integer
    packed_value = (search_buffer << (look_bits + 8)) | (look_buffer << 8) | next_char
    return packed_value

def write_compressed_data(encoded_data, output_file, search_buffer_bits, look_buffer_bits):
    binary_buffer = bytearray()  # Buffer to accumulate binary data
    bits_written = 0  # Number of bits written so far (for the header)
    buffer_size_bits = 8  # Buffer size in bits (128 bytes)

    # Iterate over each item in the encoded data
    for item in encoded_data:
        search_buffer = item[0]
        look_buffer = item[1]
        next_char = ord(item[2]) if len(item[2]) == 1 else int(item[2], 16)

        # Convert parameters to binary strings with dynamically determined lengths
        search_buffer_bin = format(search_buffer, f'0{search_buffer_bits}b')
        look_buffer_bin = format(look_buffer, f'0{look_buffer_bits}b')
        next_char_bin = format(next_char, '08b')  # Assuming 8 bits for next character

        # Add the binary data to the buffer
        binary_buffer.extend(search_buffer_bin.encode())
        binary_buffer.extend(look_buffer_bin.encode())
        binary_buffer.extend(next_char_bin.encode())

        # Update the number of bits written
        bits_written += search_buffer_bits + look_buffer_bits + 8

        # If the buffer contains at least 8 bits (1 byte), write it to the output file
        while bits_written >= buffer_size_bits:
            byte = binary_buffer[:buffer_size_bits]  # Get the first byte
            output_file.write(bytes([int(byte, 2)]))  # Write the byte to the file
            binary_buffer = binary_buffer[buffer_size_bits:]  # Remove the written byte from the buffer
            bits_written -= buffer_size_bits  # Update the number of bits written

        # Write any remaining bits in the buffer to the output file
    if bits_written > 0:
        last_byte = int(binary_buffer.ljust(8, b'0'), 2)  # Pad with zeros if needed
        output_file.write(bytes([last_byte]))

        # Flush the output file to ensure all data is written
    output_file.flush()

def is_image(file_path):
    try:
        Image.open(file_path)
        return True
    except:
        return False

def read_hex_image(file_path):
    image = Image.open(file_path)
    image_array = np.array(image)
    byte_sequence = image_array.tobytes()
    hex_string = byte_sequence.hex()
    return hex_string

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LZ77 Compression')
    parser.add_argument('-s', '--search', type=int, help='Search buffer size')
    parser.add_argument('-l', '--lookahead', type=int, help='Lookahead buffer size')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    args = parser.parse_args()

    if args.search is None or args.lookahead is None:
        print("Please provide both search and lookahead buffer sizes.")
        exit()

    input_file_path = args.input_file
    output_file_path = args.output_file
    search_buffer_size = args.search
    lookahead_buffer_size = args.lookahead

    # Check if the file is an image
    if is_image(input_file_path):
        # Read and compress the image
        input_hex_string = read_hex_image(input_file_path)
        print("Entered hexadecimal string is:", input_hex_string)
        input_sequence = select_bytes_for_compression(input_hex_string)
        print("Selected bytes for compression:", input_sequence)

        print("Entered search size is:", search_buffer_size)
        print("Entered lookahead buffer size is:", lookahead_buffer_size)

        encoded_data, encoded_length, search_buffer_bits, look_buffer_bits = lz77_encode(input_sequence, search_buffer_size, lookahead_buffer_size)
        print("Entered search bits size is:", search_buffer_bits)
        print("Entered lookahead buffer bits size is:", look_buffer_bits)

    else:
        # Read and compress the text file
        input_hex_string = read_hex_file(input_file_path)
        print("Entered hexadecimal string is:", input_hex_string)
        input_sequence = select_bytes_for_compression(input_hex_string)
        print("Selected bytes for compression:", input_sequence)

        print("Entered search size is:", search_buffer_size)
        print("Entered lookahead buffer size is:", lookahead_buffer_size)

        encoded_data, encoded_length, search_buffer_bits, look_buffer_bits = lz77_encode(input_sequence, search_buffer_size, lookahead_buffer_size)
        print("Entered search bits size is:", search_buffer_bits)
        print("Entered lookahead buffer bits size is:", look_buffer_bits)

    print("Encoded string:\n ")

    with open(output_file_path, "wb") as output_file:
        # Write the identifier for the compression algorithm (e.g., "LZ77")
        output_file.write(b"LZ77")

        # Write search_buffer_bits and look_buffer_bits to the beginning of the file
        output_file.write(search_buffer_size.to_bytes(4, 'big') + lookahead_buffer_size.to_bytes(4, 'big'))

        # Pass search buffer and look buffer bits to the function
        write_compressed_data(encoded_data, output_file, search_buffer_bits, look_buffer_bits)

    print(f"Compressed file generated as {output_file_path}")
