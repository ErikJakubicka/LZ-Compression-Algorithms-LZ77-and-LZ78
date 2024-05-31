# LZ78 Compression Code
import argparse
from collections import defaultdict
from PIL import Image
import numpy as np


def lz78_compress(input_sequence):
    dictionary = {"" : 0}  # Initialize the dictionary with an empty string
    compressed_data = []
    current_match = ""

    for char in input_sequence:
        current_match += char

        if current_match not in dictionary:
            if len(char) > 1:
                # If the current match is a hexadecimal value
                dictionary[current_match] = len(dictionary)
                compressed_data.append((dictionary[current_match[:-2]], current_match[-2:]))  # Append the last two characters as a hexadecimal value
                current_match = ""
            else:
                # If the current match is not a hexadecimal value
                dictionary[current_match] = len(dictionary)
                compressed_data.append((dictionary[current_match[:-1]], char))  # Append the last character of the current match
                current_match = ""

    if current_match:
        if is_valid_hexadecimal(current_match):
            # If the remaining match is a hexadecimal value
            compressed_data.append((dictionary[current_match[:-2]], current_match[-2:]))  # Append the last two characters as a hexadecimal value

    # Iterate over each item in the compressed data to find the maximum prefix length
    max_prefix_length = max(item[0].bit_length() for item in compressed_data)

    return compressed_data, max_prefix_length

def print_lz78_step(input_string):
    dictionary = defaultdict(int)  # Initialize the dictionary with an empty string
    compressed_data = []
    current_match = ""
    highlighted_string = ""

    for char_index, char in enumerate(input_string):
        current_match += char
        if current_match not in dictionary:
            dictionary[current_match] = len(dictionary)
            match_start_index = char_index - len(current_match) + 1
            remaining_string_before = input_string[:match_start_index]
            compressed_data.append((remaining_string_before, current_match[:-1], char, input_string[char_index + 1:], (dictionary[current_match[:-1]], char)))
            current_match = ""

    # Check if there's any remaining match
    if current_match:
        match_start_index = len(input_string) - len(current_match)
        remaining_string_before = input_string[:match_start_index]
        compressed_data.append((remaining_string_before, current_match, "", "", (dictionary[current_match], '')))

    for before, match, char, after, compress in compressed_data:
        # Format the match and char within brackets
        formatted_match = f"[{match}]" if match else ""
        formatted_char = f"[{char}]" if char else ""
        highlighted_string += (
            f"{before}\033[92m{formatted_match}\033[0m \033[93m{formatted_char}\033[0m {after} {compress}\n"
        )

    return highlighted_string


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

def write_compressed_data(encoded_data, output_file, max_prefix_length):
    binary_buffer = bytearray()  # Buffer to accumulate binary data
    bits_written = 0  # Number of bits written so far

    for item in encoded_data:
        search_buffer = item[0]
        next_char = ord(item[1]) if len(item[1]) == 1 else int(item[1], 16)

        # Convert parameters to binary strings with dynamically determined lengths
        search_buffer_bin = format(search_buffer, f'0{max_prefix_length}b')
        next_char_bin = format(next_char, '08b')  # Assuming 8 bits for next character

        # Add the binary data to the buffer
        binary_buffer.extend(search_buffer_bin.encode())
        binary_buffer.extend(next_char_bin.encode())

        # Update the number of bits written
        bits_written += len(search_buffer_bin) + 8

        # If the buffer contains at least 8 bits (1 byte), write it to the output file
        while bits_written >= 8:
            byte = binary_buffer[:8]  # Get the first byte
            output_file.write(bytes([int(byte, 2)]))  # Write the byte to the file
            binary_buffer = binary_buffer[8:]  # Remove the written byte from the buffer
            bits_written -= 8  # Update the number of bits written

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
    parser = argparse.ArgumentParser(description='LZ78 Compression')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    args = parser.parse_args()

    input_file_path = args.input_file

    # Check if the file is an image
    if is_image(input_file_path):
        # Read and compress the image
        input_hex_string = read_hex_image(input_file_path)
        input_sequence = select_bytes_for_compression(input_hex_string)
        compressed_data, max_prefix_length = lz78_compress(input_sequence)
        print("Entered vectors image is:", input_hex_string)

        print("Selected bytes for compression:", input_sequence)
        print("Entered matched letters bits size is:", max_prefix_length)
        output_file_path = args.output_file
    else:
        # Read and compress the text file
        input_hex_string = read_hex_file(input_file_path)
        input_sequence = select_bytes_for_compression(input_hex_string)
        compressed_data, max_prefix_length = lz78_compress(input_sequence)
        print("Entered hexadecimal string is:", input_hex_string)

        print("Selected bytes for compression:", input_sequence)
        print("Entered matched letters bits size is:", max_prefix_length)

        print(compressed_data)
        output_file_path = args.output_file

    print("Encoded string:\n ")

    with open(output_file_path, "wb") as output_file:
        # Write the identifier for the compression algorithm (e.g., "LZ78")
        output_file.write(b"LZ78")

        # Write max_prefix_length to the beginning of the file
        output_file.write(max_prefix_length.to_bytes(4, 'big'))

        # Write the compressed data to the file
        write_compressed_data(compressed_data, output_file, max_prefix_length)

    print(f"Compressed file generated as {output_file_path}")
    