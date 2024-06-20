# LZ78 Decompression Code
import os
import argparse

def read_compressed_data(file_path):
    with open(file_path, "rb") as file:
        # Read the first four bytes to check for the compression algorithm identifier
        algorithm_identifier = file.read(4)
        if algorithm_identifier != b"LZ78":
            raise ValueError("Invalid compression algorithm identifier. Expected 'LZ78'.")

        # Read the first four bytes to get the search buffer and look buffer parameters
        buffer_bytes = file.read(4)
        if len(buffer_bytes) < 4:
            raise ValueError("File is too short to contain search buffer and look buffer parameters")

        # Extract search buffer
        search_buffer_bits = int.from_bytes(buffer_bytes[:4], 'big')

        # Initialize variables
        compressed_data = []
        binary_string = ""

        # Read the binary data from the file
        byte = file.read(1)
        while byte:
            # Convert the byte to binary string
            binary_byte = bin(int.from_bytes(byte, byteorder='big'))[2:].zfill(8)
            binary_string += binary_byte
            byte = file.read(1)

        # Track the number of bits read
        bits_read = 0

        # Iterate over the binary string
        while bits_read + search_buffer_bits + 8 <= len(binary_string):
            # Extract search buffer and next character
            search_buffer_bin = binary_string[bits_read:bits_read + search_buffer_bits]
            next_char_bin = binary_string[bits_read + search_buffer_bits:bits_read + search_buffer_bits + 8]

            # Convert binary strings to integers
            search_buffer = int(search_buffer_bin, 2)
            next_char = int(next_char_bin, 2)

            # Append the decompressed data to the list
            compressed_data.append((search_buffer, chr(next_char)))

            # Update the number of bits read
            bits_read += search_buffer_bits + 8

    return compressed_data, search_buffer_bits

def lz78_decompress(compressed_data):
    dictionary = {0: ""}
    decompressed_string = ""

    for index, char in compressed_data:
        word = dictionary[index]
        dictionary[len(dictionary)] = word + char
        decompressed_string += word + char

    return decompressed_string


def count_characters_in_compressed_file(file_path):
    character_count = {}
    with open(file_path, "rb") as file:
        # Skip the first 8 bytes (4 bytes for identifier + 4 bytes for buffer parameters)
        file.seek(8)
        # Read the rest of the file as bytes
        data = file.read()
        # Iterate over each byte
        for byte in data:
            # Decode the byte to a character
            char = chr(byte)
            # Increment the count for the character
            if char in character_count:
                character_count[char] += 1
            else:
                character_count[char] = 1
    return character_count

# Function to get the size of a file in bytes
def get_file_size(file_path):
    return os.path.getsize(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LZ78 Decompression')
    parser.add_argument('input_file', help='Input file path')
    args = parser.parse_args()

    input_file_path = args.input_file

    compressed_data, search_buffer_bits = read_compressed_data(input_file_path)
    decoded_sequence = lz78_decompress(compressed_data)
    print(f"Decoded sequence: {decoded_sequence}")
    print(f"Matched Letter bits size is: {search_buffer_bits}\n")

    character_count = count_characters_in_compressed_file(input_file_path)

    # Calculate the sizes
    original_size = len(decoded_sequence)
    compressed_size = len(character_count)

    # Get the sizes of the compressed and original files
    compressed_size_bits = get_file_size(input_file_path)

    # Calculate the success rate
    success_rate = (1 - (compressed_size / original_size)) * 100

    print(f"Character count in compressed file: {compressed_size}")
    print(f"Size of original file bytes: {original_size} bytes")
    print(f"Size of compressed file bytes: {compressed_size_bits} bytes")
    print(f"Compression Success Rate: {success_rate:.2f}%")


