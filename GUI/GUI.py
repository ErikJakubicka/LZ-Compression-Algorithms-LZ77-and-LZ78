# GUI code
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import math
import os

class MyGUI(QMainWindow):

    def __init__(self):
        super(MyGUI, self).__init__()
        self.highlighting_enabled = False
        self.user_input_2 = None  # Initialize user_input_2
        self.user_input_3 = None  # Initialize user_input_3
        self.load_welcome_ui()

    def load_welcome_ui(self):
        uic.loadUi("welcome.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ77/78")
        self.setFixedSize(QSize(740, 380))
        self.show()

        self.pushButtonLZ77.clicked.connect(self.lz77)
        self.pushButtonLZ78.clicked.connect(self.lz78)

    def lz77(self):
        uic.loadUi("welcome_LZ77.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ77")
        self.setFixedSize(QSize(740, 380))
        self.show()

        self.pushButtonN77.clicked.connect(self.next77)
        self.pushButtonBW.clicked.connect(self.load_welcome_ui)

    def lz78(self):
        uic.loadUi("welcome_LZ78.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ78")
        self.setFixedSize(QSize(740, 380))
        self.show()

        self.pushButtonN78.clicked.connect(self.next78)
        self.pushButtonBW.clicked.connect(self.load_welcome_ui)

    def toggle_back_lz77(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.lz77()

    def toggle_start77(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.start77()

    def next77(self):
        uic.loadUi("mygui_LZ77.ui", self)
        self.setWindowTitle("LZ77")
        self.setFixedSize(QSize(1280, 470))
        self.show()

        self.pushButtonS77.clicked.connect(self.toggle_start77)
        self.pushButtonBW77.clicked.connect(self.toggle_back_lz77)
        self.commandLinkButtonInfo.clicked.connect(self.lz77Info)

    def lz77Info(self):
        uic.loadUi("InfoLZ77.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ77- info")
        self.setFixedSize(QSize(700, 560))
        self.show()

        self.pushButtonToggleB.clicked.connect(self.next77)

    def toggle_back_lz78(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.lz78()

    def toggle_start78(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.start78()
    def next78(self):
        uic.loadUi("mygui_LZ78.ui", self)
        self.setWindowTitle("LZ78")
        self.setFixedSize(QSize(1280, 470))
        self.show()

        self.pushButtonS78.clicked.connect(self.toggle_start78)
        self.pushButtonBW78.clicked.connect(self.toggle_back_lz78)
        self.commandLinkButtonInfo.clicked.connect(self.lz78Info)

    def lz78Info(self):
        uic.loadUi("InfoLZ78.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ78- info")
        self.setFixedSize(QSize(700, 560))
        self.show()

        self.pushButtonToggleB.clicked.connect(self.next78)

    # LZ77 code
    def lz77_encode(self, input_sequence, window_size, lookahead_buffer_size):
        encoded_data = []
        window_start = 0

        # Calculate the number of bits needed for search buffer and look buffer
        search_buffer_bits = math.ceil(math.log2(window_size + 1))
        look_buffer_bits = math.ceil(math.log2(lookahead_buffer_size + 1))

        while window_start < len(input_sequence):
            match = self.find_longest_match(input_sequence, window_start, window_size, lookahead_buffer_size)
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

    def print_step(self, input_string, window_start, window_size, offset, length, next_char):
        window_highlight = input_string[window_start - offset:window_start - offset + length]
        lookahead_highlight = input_string[window_start:window_start + length]
        common_highlight = input_string[window_start:window_start + min(len(window_highlight), len(lookahead_highlight))]
        remaining_string_before = input_string[:max(0, window_start - window_size)]
        remaining_string_before_with_space = ' '.join(remaining_string_before)
        remaining_string_after = input_string[window_start + length + 1:]
        remaining_string_after_with_space = ' '.join(remaining_string_after)


        formatted_string = (
            f"{remaining_string_before_with_space + ' '}"
            f"<font style='background-color: lightgreen; display: inline-block; padding: 5px;'>{' '.join(input_string[max(0, window_start - window_size):window_start] + ' ')}</font>"
            f"<font style='background-color: lightblue; display: inline-block; padding: 5px;'>{' '.join(window_highlight + ' ')}</font>"
            f"<font style='background-color: lightblue; display: inline-block; padding: 5px;'>{' '.join(lookahead_highlight[len(common_highlight):] + ' ')}</font>"
            f"<font style='background-color: lightgrey; display: inline-block; padding: 5px;'>{' '.join(next_char + ' ')}</font>"
            f"{remaining_string_after_with_space + ' '}"
        )
        return formatted_string

    def print_step_original(self, input_string, window_start, window_size, offset, length, next_char):
        window_highlight = input_string[window_start - offset:window_start - offset + length]
        lookahead_highlight = input_string[window_start:window_start + length]
        common_highlight = input_string[
                           window_start:window_start + min(len(window_highlight), len(lookahead_highlight))]
        remaining_string_before = input_string[:max(0, window_start - window_size)]
        remaining_string_before_with_space = ' '.join(remaining_string_before)
        remaining_string_after = input_string[window_start + length + 1:]
        remaining_string_after_with_space = ' '.join(remaining_string_after)

        formatted_string = (
            f"{remaining_string_before_with_space + ' '}"
            f"<font style='display: inline-block; padding: 5px;'>{' '.join(input_string[max(0, window_start - window_size):window_start] + ' ')}</font>"
            f"<font style='display: inline-block; padding: 5px;'>{' '.join(window_highlight + ' ')}</font>"
            f"<font style='display: inline-block; padding: 5px;'>{' '.join(lookahead_highlight[len(common_highlight):] + ' ')}</font>"
            f"<font style='display: inline-block; padding: 5px;'>{' '.join(next_char + ' ')}</font>"
            f"{remaining_string_after_with_space + ' '}"
        )
        return formatted_string

    def find_longest_match(self, input_string, window_start, window_size, lookahead_buffer_size):
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

    def write_compressed_data(self, encoded_data, output_file, search_buffer_bits, look_buffer_bits):
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

    def read_compressed_data77(self, file_path):
        with open(file_path, "rb") as file:
            # Read the first two bytes to get the search buffer and look buffer parameters
            buffer_bytes = file.read(2)
            if len(buffer_bytes) < 2:
                raise ValueError("File is too short to contain search buffer and look buffer parameters")

            # Extract search buffer and look buffer parameters
            search_buffer = buffer_bytes[0]
            look_buffer = buffer_bytes[1]

            # Calculate the number of bits needed for search buffer and look buffer
            search_buffer_bits = math.ceil(math.log2(search_buffer + 1))
            look_buffer_bits = math.ceil(math.log2(look_buffer + 1))

            # Initialize variables
            compressed_data = []
            binary_string = ""

            # Read the rest of the file
            byte = file.read(1)
            while byte:
                # Convert the byte to binary string
                binary_byte = bin(int.from_bytes(byte, byteorder='big'))[2:].zfill(8)
                binary_string += binary_byte
                byte = file.read(1)

            # Iterate over the binary string
            while len(binary_string) >= search_buffer_bits + look_buffer_bits + 8:
                # Extract search buffer, look buffer, and next character
                search_buffer_bin = binary_string[:search_buffer_bits]
                look_buffer_bin = binary_string[search_buffer_bits:search_buffer_bits + look_buffer_bits]
                next_char_bin = binary_string[
                                search_buffer_bits + look_buffer_bits:search_buffer_bits + look_buffer_bits + 8]

                # Convert binary strings to integers
                search_buffer = int(search_buffer_bin, 2)
                look_buffer = int(look_buffer_bin, 2)
                next_char = int(next_char_bin, 2)

                # Append the decompressed data to the list
                compressed_data.append((search_buffer, look_buffer, chr(next_char)))

                # Remove the processed bits from the binary string
                binary_string = binary_string[search_buffer_bits + look_buffer_bits + 8:]

        return compressed_data, search_buffer_bits, look_buffer_bits

    def lz77_decompress(self, encoded_data):
        decompressed_string = ""
        for symbol in encoded_data:
            offset, length, char = symbol
            if offset == 0:
                decompressed_string += char
            else:
                start = len(decompressed_string) - offset
                for i in range(length):
                    decompressed_string += decompressed_string[start + i]
                decompressed_string += char
        return decompressed_string

    def count_characters_in_compressed_file(self, file_path):
        character_count = {}
        with open(file_path, "rb") as file:
            # Read the entire file as bytes
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
    def get_file_size(self, file_path):
        return os.path.getsize(file_path)


    def start77(self):
        if hasattr(self, 'file_input'):  # Check if file_input attribute exists
            user_input = self.file_input  # If it exists, use the file_input
            del self.file_input  # Delete the attribute to avoid reusing it inappropriately

        else:
            user_input = self.lineEdit.text()  # Otherwise, use the line edit input
        user_input_2 = self.lineEdit_2.text()
        user_input_3 = self.lineEdit_3.text()
        self.user_input = user_input
        self.user_input_2 = int(user_input_2) if user_input_2.isdigit() else None
        self.user_input_3 = int(user_input_3) if user_input_3.isdigit() else None

        if ((user_input == '') | (user_input_2 == '') | (user_input_3 == '')):
            uic.loadUi("war.ui", self)
            self.setWindowTitle("LZ77- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next77)
            return

        if not user_input.isascii():  # Check if user_input contains only ASCII characters
            uic.loadUi("war5.ui", self)  # Load a specific warning UI for non-ASCII input
            self.setWindowTitle("LZ77- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next77)
            return

        if not user_input_2.lstrip('-').isdigit() or not user_input_3.lstrip('-').isdigit():  # Check if inputs are not numeric
            uic.loadUi("war2.ui", self)
            self.setWindowTitle("LZ77- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next77)
            return

        elif int(user_input_2) < 0 or int(user_input_3) < 0:  # Check if inputs are negative
            uic.loadUi("war3.ui", self)
            self.setWindowTitle("LZ77- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next77)
            return

        elif int(user_input_2) > 100 or int(user_input_3) > 100:  # Check if inputs are greater than 100
            uic.loadUi("war4.ui", self)
            self.setWindowTitle("LZ77- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next77)
            return

        else:
            super(MyGUI, self).__init__()
            self.compress77()

    def toggle_highlighting(self):
        self.highlighting_enabled = not self.highlighting_enabled
        self.pushButtonToggle.setText(
            "Highlighting (Enabled)" if self.highlighting_enabled else "Highlighting (Disabled)")

        # Clear the previous highlighted text lines
        self.highlighted_text_lines = []
        self.current_line_index = 0

        # Regenerate the highlighted text lines based on the new highlighting state
        for i, item in enumerate(self.encoded_data):
            window_start = sum(entry[1] + 1 for entry in self.encoded_data[:i])
            if self.highlighting_enabled:
                line = f"{self.print_step(self.user_input, window_start, int(self.user_input_2), *item)}{item}"
            else:
                line = f"{self.print_step_original(self.user_input, window_start, int(self.user_input_2), *item)}{item}"
            self.highlighted_text_lines.extend(line.split("<br>"))

        # Update the display
        self.update_label2()

    def toggle_decompress77(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.next77D()

    def toggle_back77(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.next77()

    def compress77(self):
        # Remove all current widgets
        for widget in self.findChildren(QWidget):
            widget.deleteLater()
        uic.loadUi("compression_LZ77.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ77")
        self.setFixedSize(QSize(1280, 730))

        user_input = self.user_input
        user_input_2 = self.user_input_2
        user_input_3 = self.user_input_3
        self.current_line_index = 0

        self.label = QLabel(self)  # Create a QLabel widget
        self.label.setGeometry(10, 40, 600, 100)  # Adjust the geometry as needed
        self.label3 = QLabel(self)  # Create a QLabel widget
        self.label3.setGeometry(40, 70, 600, 100)  # Adjust the geometry as needed
        self.label4 = QLabel(self)  # Create a QLabel widget
        self.label4.setGeometry(40, 100, 600, 100)  # Adjust the geometry as needed
        self.label5 = QLabel(self)  # Create a QLabel widget
        self.label5.setGeometry(40, 130, 600, 100)  # Adjust the geometry as needed

        self.image_label = QPixmap("Green.png")  # Replace "image.jpg" with your image file path
        self.label6 = QLabel(self)  # Create a QLabel widget
        self.label6.setPixmap(self.image_label)
        self.label6.resize(3, 3)
        self.label6.setGeometry(10, 70, 600, 100)

        self.image_label2 = QPixmap("Blue.png")  # Replace "image.jpg" with your image file path
        self.label7 = QLabel(self)  # Create a QLabel widget
        self.label7.setPixmap(self.image_label2)
        self.label7.resize(3, 3)
        self.label7.setGeometry(10, 100, 600, 100)

        self.image_label3 = QPixmap("Grey.png")  # Replace "image.jpg" with your image file path
        self.label8 = QLabel(self)  # Create a QLabel widget
        self.label8.setPixmap(self.image_label3)
        self.label8.resize(3, 3)
        self.label8.setGeometry(10, 130, 600, 100)

        font = QFont("Segoe UI", 20)  # Example: Arial font with a size of 12 points
        font.setBold(True)
        font2 = QFont("Segoe UI", 18)  # Example: Arial font with a size of 12 points

        self.label.setFont(font)
        self.label3.setFont(font2)
        self.label4.setFont(font2)
        self.label5.setFont(font2)

        self.encoded_data, encoded_length, search_buffer_bits, look_buffer_bits = self.lz77_encode(user_input, user_input_2, user_input_3)
        self.label.setText("Encoded data:")
        self.label3.setText(f"Dictionary Size: {user_input_2}")
        self.label4.setText(f"Longest Match Size: {user_input_3}")
        self.label5.setText("Next Character")

        # Access the scroll area
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")

        # Create a widget to serve as the content for the scroll area
        scroll_content_widget = QWidget()

        # Create a layout for the content widget
        scroll_content_layout = QVBoxLayout(scroll_content_widget)

        # Create a horizontal layout for label2 with indentation
        label2_layout = QHBoxLayout()
        spacer = QSpacerItem(380, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        label2_layout.addItem(spacer)
        self.label2 = QLabel(self)  # Create label2 here
        label2_layout.addWidget(self.label2)
        scroll_content_layout.addLayout(label2_layout)
        self.label2.setFont(font)

        # Set the content widget for the scroll area
        self.scrollArea.setWidget(scroll_content_widget)

        # Adjust the size policy of label2
        self.label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Reset the highlighted text lines
        self.highlighted_text_lines = []

        for i, item in enumerate(self.encoded_data):
            window_start = sum(entry[1] + 1 for entry in self.encoded_data[:i])
            if self.highlighting_enabled:
                line = f"{self.print_step(user_input, window_start, int(user_input_2), *item)}{item}"
            else:
                line = f"{self.print_step_original(user_input, window_start, int(user_input_2), *item)}{item}"

            self.highlighted_text_lines.extend(line.split("<br>"))

        # Update the display
        self.update_label2()

        with open("compressed_LZ77.txt", "wb") as output_file:
            # Write search_buffer_bits and look_buffer_bits to the beginning of the file
            output_file.write(bytes([user_input_2, user_input_3]))

            # Pass search buffer and look buffer bits to the function
            self.write_compressed_data(self.encoded_data, output_file, search_buffer_bits, look_buffer_bits)

        self.show()
        self.pushButtonToggleB.clicked.connect(self.toggle_back77)
        self.pushButtonN77D.clicked.connect(self.toggle_decompress77)
        self.pushButtonN77N.clicked.connect(self.update_label2)
        self.pushButtonToggle.clicked.connect(self.toggle_highlighting)

    def update_label2(self):
        # Update label2 with the next line if available
        if self.current_line_index < len(self.highlighted_text_lines):
            if self.current_line_index == 0:
                self.label2.setText(self.highlighted_text_lines[self.current_line_index])
            else:
                current_text = self.label2.text()
                next_line = self.highlighted_text_lines[self.current_line_index]
                self.label2.setText(current_text + "<br>" + next_line)
            self.current_line_index += 1

    # LZ78
    def lz78_compress(self, input_string):
        dictionary = {"": 0}  # Initialize the dictionary with an empty string
        compressed_data = []
        current_match = ""

        for char in input_string:
            current_match += char

            if current_match not in dictionary:
                dictionary[current_match] = len(dictionary)
                compressed_data.append((dictionary[current_match[:-1]], char))
                current_match = ""

        if current_match:
            compressed_data.append((dictionary[current_match], " "))

        return compressed_data

    def print_lz78_step(self, input_string):
        dictionary = {"": 0}  # Initialize the dictionary with an empty string
        compressed_data = []
        current_match = ""

        highlighted_string = ""

        for char_index, char in enumerate(input_string):
            current_match += char
            if current_match not in dictionary:
                dictionary[current_match] = len(dictionary)
                # Get the index where the current match starts
                match_start_index = char_index - len(current_match) + 1
                # Get the remaining string before and after the current match
                remaining_string_before = input_string[:match_start_index]
                remaining_string_before_with_spaces = ' '.join(remaining_string_before)
                remaining_string_after = input_string[char_index + 1:]
                remaining_string_after_with_spaces = ' '.join(remaining_string_after)
                current_match_without_spaces = ' '.join(current_match)
                # Append the compressed data with color formatting and remaining strings
                if char != ' ' or dictionary[current_match[:-1]] != 0:
                    compressed_data.append(
                        (
                            remaining_string_before_with_spaces, f"<font style='background-color: lightgreen;'>{current_match_without_spaces[:-1]}</font>",
                            f"<font style='background-color: lightgrey;'>{char}</font>", remaining_string_after_with_spaces,
                            (dictionary[current_match[:-1]], char)))
                current_match = ""

        if current_match:
            # Get the index where the current match starts
            match_start_index = len(input_string) - len(current_match)
            # Get the remaining string before and after the current match
            remaining_string_before = input_string[:match_start_index]
            remaining_string_after = ""
            # Append the remaining compressed data with color formatting and remaining strings
            compressed_data.append(
                (remaining_string_before, f"<font style='background-color: lightgreen;'>{current_match}</font>",
                 f"<font style='background-color: lightgrey;'> </font>", remaining_string_after,
                 (dictionary[current_match], " ")))

        for before, match, char, after, compress in compressed_data:
            highlighted_string += before + " " + match + " " + char + " " + after + " " + str(compress) + "<br>"

        return highlighted_string

    def print_lz78_step_original(self, input_string):
        dictionary = {"": 0}  # Initialize the dictionary with an empty string
        compressed_data = []
        current_match = ""

        highlighted_string = ""

        for char_index, char in enumerate(input_string):
            current_match += char
            if current_match not in dictionary:
                dictionary[current_match] = len(dictionary)
                # Get the index where the current match starts
                match_start_index = char_index - len(current_match) + 1
                # Get the remaining string before and after the current match
                remaining_string_before = input_string[:match_start_index]
                remaining_string_before_with_spaces = ' '.join(remaining_string_before)
                remaining_string_after = input_string[char_index + 1:]
                remaining_string_after_with_spaces = ' '.join(remaining_string_after)
                current_match_without_spaces = ' '.join(current_match)
                # Append the compressed data with color formatting and remaining strings
                if char != ' ' or dictionary[current_match[:-1]] != 0:
                    compressed_data.append(
                        (
                            remaining_string_before_with_spaces,
                            f"<font style=''>{current_match_without_spaces[:-1]}</font>",
                            f"<font style=''>{char}</font>",
                            remaining_string_after_with_spaces,
                            (dictionary[current_match[:-1]], char)))
                current_match = ""

        if current_match:
            # Get the index where the current match starts
            match_start_index = len(input_string) - len(current_match)
            # Get the remaining string before and after the current match
            remaining_string_before = input_string[:match_start_index]
            remaining_string_after = ""
            # Append the remaining compressed data with color formatting and remaining strings
            compressed_data.append(
                (remaining_string_before, f"<font style=''>{current_match}</font>",
                 f"<font style=''> </font>", remaining_string_after,
                 (dictionary[current_match], " ")))

        for before, match, char, after, compress in compressed_data:
            highlighted_string += before + " " + match + " " + char + " " + after + " " + str(compress) + "<br>"

        return highlighted_string

    def write_compressed_data_LZ78(self, encoded_data, output_file):
        binary_buffer = bytearray()  # Buffer to accumulate binary data
        bits_written = 0  # Number of bits written so far

        # Iterate over each item in the encoded data
        max_prefix_length = max(item[0].bit_length() for item in encoded_data)

        # Write max_prefix_length to the beginning of the file
        output_file.write(bytes([max_prefix_length]))

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

    def read_compressed_data78(self, file_path):
        with open(file_path, "rb") as file:
            # Read the first bytes to get the search buffer
            buffer_bytes = file.read(1)
            if len(buffer_bytes) < 1:
                raise ValueError("File is too short to contain search buffer and look buffer parameters")

            # Extract search buffer
            search_buffer_bits = buffer_bytes[0]

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

    def lz78_decompress(self, compressed_data):
        dictionary = {0: ""}
        decompressed_string = ""

        for index, char in compressed_data:
            word = dictionary[index]
            dictionary[len(dictionary)] = word + char
            decompressed_string += word + char

        return decompressed_string


    def start78(self):
        if hasattr(self, 'file_input'):  # Check if file_input attribute exists
            user_input = self.file_input  # If it exists, use the file_input
            del self.file_input  # Delete the attribute to avoid reusing it inappropriately

        else:
            user_input = self.lineEdit.text()  # Otherwise, use the line edit input
        self.user_input = user_input

        if (user_input == ''):
            uic.loadUi("war.ui", self)
            self.setWindowTitle("LZ78- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next78)
            return

        if not user_input.isascii():  # Check if user_input contains only ASCII characters
            uic.loadUi("war5.ui", self)  # Load a specific warning UI for non-ASCII input
            self.setWindowTitle("LZ78- warning")
            self.setFixedSize(QSize(536, 200))
            self.show()

            self.pushButton_war.clicked.connect(self.next78)
            return

        else:
            super(MyGUI, self).__init__()
            self.compress78()

    def toggle_highlighting_LZ78(self):
        self.highlighting_enabled = not self.highlighting_enabled
        if self.highlighting_enabled:
            self.pushButtonToggle78.setText("Highlighting (Enabled)")
        else:
            self.pushButtonToggle78.setText("Highlighting (Disabled)")

        # Clear the current display and reset the line index
        self.label2.setText("")
        self.current_line_index = 0

        # Repopulate highlighted_text_lines based on the new highlighting mode
        user_input = self.user_input
        self.highlighted_text_lines = []

        if self.highlighting_enabled:
            highlighted_text = self.print_lz78_step(user_input)
        else:
            highlighted_text = self.print_lz78_step_original(user_input)

        # Split the highlighted text into lines and add to highlighted_text_lines
        self.highlighted_text_lines = highlighted_text.split("<br>")  # Adjust splitting method if necessary

        # Update the display
        self.update_label78()

    def toggle_decompress78(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.next78D()

    def toggle_back78(self):
        # Close the current window
        self.close()
        # Get encoded_data and user_input from compress77
        self.next78()

    def compress78(self):
        # Remove all current widgets
        for widget in self.findChildren(QWidget):
            widget.deleteLater()
        uic.loadUi("compression_LZ78.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ78")
        self.setFixedSize(QSize(1280, 780))

        user_input = self.user_input
        self.current_line_index = 0

        self.label = QLabel(self)  # Create a QLabel widget
        self.label.setGeometry(10, 40, 600, 100)  # Adjust the geometry as needed
        self.label3 = QLabel(self)  # Create a QLabel widget
        self.label3.setGeometry(40, 70, 600, 100)  # Adjust the geometry as needed
        self.label4 = QLabel(self)  # Create a QLabel widget
        self.label4.setGeometry(40, 100, 600, 100)  # Adjust the geometry as needed

        self.image_label = QPixmap("Green.png")  # Replace "image.jpg" with your image file path
        self.label6 = QLabel(self)  # Create a QLabel widget
        self.label6.setPixmap(self.image_label)
        self.label6.resize(3, 3)
        self.label6.setGeometry(10, 70, 600, 100)

        self.image_label2 = QPixmap("Grey.png")  # Replace "image.jpg" with your image file path
        self.label7 = QLabel(self)  # Create a QLabel widget
        self.label7.setPixmap(self.image_label2)
        self.label7.resize(3, 3)
        self.label7.setGeometry(10, 100, 600, 100)

        font = QFont("Segoe UI", 20)  # Example: Arial font with a size of 12 points
        font.setBold(True)
        font2 = QFont("Segoe UI", 18)  # Example: Arial font with a size of 12 points

        self.label.setFont(font)
        self.label3.setFont(font2)
        self.label4.setFont(font2)

        self.label.setText("Encoded data:")
        self.label3.setText("Matched Letter")
        self.label4.setText("Next Character")

        compressed_data = self.lz78_compress(user_input)

        # Access the scroll area
        self.scrollArea = self.findChild(QScrollArea, "scrollArea")

        # Create a widget to serve as the content for the scroll area
        scroll_content_widget = QWidget()

        # Create a layout for the content widget
        scroll_content_layout = QVBoxLayout(scroll_content_widget)

        # Create a horizontal layout for label2 with indentation
        label2_layout = QHBoxLayout()
        spacer = QSpacerItem(380, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        label2_layout.addItem(spacer)
        self.label2 = QLabel(self)  # Create label2 here
        label2_layout.addWidget(self.label2)
        scroll_content_layout.addLayout(label2_layout)
        self.label2.setFont(font)

        # Set the content widget for the scroll area
        self.scrollArea.setWidget(scroll_content_widget)

        # Adjust the size policy of label2
        self.label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Reset the highlighted text lines
        self.highlighted_text_lines = []

        # Get the highlighted text
        if self.highlighting_enabled:
            highlighted_text = self.print_lz78_step(user_input)
        else:
            highlighted_text = self.print_lz78_step_original(user_input)

        # Split the highlighted text into lines and add to highlighted_text_lines
        self.highlighted_text_lines = highlighted_text.split("<br>")  # Adjust splitting method if necessary

        # Update the display
        self.update_label78()

        with open("compressed_LZ78.txt", "wb") as output_file:
            # Write the compressed data to the file
            self.write_compressed_data_LZ78(compressed_data, output_file)

        self.show()
        self.pushButtonToggleB.clicked.connect(self.toggle_back78)
        self.pushButtonN78D.clicked.connect(self.toggle_decompress78)
        self.pushButtonN78N.clicked.connect(self.update_label78)
        self.pushButtonToggle78.clicked.connect(self.toggle_highlighting_LZ78)

    def update_label78(self):
        # Check if the current line index is less than the length of highlighted_text_lines
        if self.current_line_index < len(self.highlighted_text_lines):
            # Get the next line from highlighted_text_lines
            next_line = self.highlighted_text_lines[self.current_line_index]
            # Append the next line to the current text of label2, separated by a line break
            current_text = self.label2.text()
            self.label2.setText(current_text + next_line + "<br>")
            # Increment the current line index
            self.current_line_index += 1

    def toggle_back_decompress77(self):
        # Close the current window
        self.close()
        # Get encoded_data ands uer_input from compress77
        self.start77()

    def next77D(self):
        # Remove all current widgets
        for widget in self.findChildren(QWidget):
            widget.deleteLater()
        uic.loadUi("decompression_LZ77.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ77")

        self.label = QLabel(self)  # Create a QLabel widget
        self.label.setGeometry(10, 40, 600, 100)  # Adjust the geometry as needed
        self.label2 = QLabel(self)  # Create a QLabel widget
        self.label2.setGeometry(10, 90, 600, 100)  # Adjust the geometry as needed
        self.label3 = QLabel(self)  # Create a QLabel widget
        self.label3.setGeometry(10, 130, 600, 100)  # Adjust the geometry as needed
        self.label4 = QLabel(self)  # Create a QLabel widget
        self.label4.setGeometry(10, 190, 600, 100)  # Adjust the geometry as needed
        self.label5 = QLabel(self)  # Create a QLabel widget
        self.label5.setGeometry(10, 220, 600, 100)  # Adjust the geometry as needed
        self.label6 = QLabel(self)  # Create a QLabel widget
        self.label6.setGeometry(10, 280, 600, 100)  # Adjust the geometry as needed

        font = QFont("Segoe UI", 20)  # Example: Arial font with a size of 12 points
        font.setBold(True)
        font2 = QFont("Segoe UI", 18)  # Example: Arial font with a size of 12 points

        self.label.setFont(font)
        self.label2.setFont(font2)
        self.label3.setFont(font2)
        self.label4.setFont(font2)
        self.label5.setFont(font2)
        self.label6.setFont(font2)


        compressed_file_path = "compressed_LZ77.txt"

        compressed_data, search_buffer_bits, look_buffer_bits = self.read_compressed_data77(compressed_file_path)  # Assuming 8 bits for search buffer and 6 bits for look buffer
        decoded_sequence = self.lz77_decompress(compressed_data)

        self.label.setText(f"Decompressed data: {decoded_sequence}")
        self.label2.setText(f"Search bits size is: {search_buffer_bits}")
        self.label3.setText(f"Lookahead buffer bits size is: {look_buffer_bits}")

        character_count = self.count_characters_in_compressed_file(compressed_file_path)

        # Calculate the sizes
        original_size = len(decoded_sequence)
        compressed_size = len(character_count)

        # Calculate the success rate
        success_rate = (1 - (compressed_size / original_size)) * 100

        # Calculate the success rate of bits
        success_rate_bits = (1 - (compressed_size / original_size)) * 100

        self.label4.setText(f"Character count in compressed file: {compressed_size}")
        self.label5.setText(f"Character count in original string: {original_size}")
        self.label6.setText(f"Compression Success Rate: {success_rate:.2f}")

        self.show()
        self.pushButtonB77C.clicked.connect(self.toggle_back_decompress77)
        return

    def toggle_back_decompress78(self):
        # Close the current window
        self.close()
        # Get encoded_data ands uer_input from compress77
        self.start78()

    def next78D(self):
        # Remove all current widgets
        for widget in self.findChildren(QWidget):
            widget.deleteLater()
        uic.loadUi("decompression_LZ78.ui", self)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("LZ78")

        self.label = QLabel(self)  # Create a QLabel widget
        self.label.setGeometry(10, 40, 600, 100)  # Adjust the geometry as needed
        self.label2 = QLabel(self)  # Create a QLabel widget
        self.label2.setGeometry(10, 90, 600, 100)  # Adjust the geometry as needed
        self.label4 = QLabel(self)  # Create a QLabel widget
        self.label4.setGeometry(10, 190, 600, 100)  # Adjust the geometry as needed
        self.label5 = QLabel(self)  # Create a QLabel widget
        self.label5.setGeometry(10, 220, 600, 100)  # Adjust the geometry as needed
        self.label6 = QLabel(self)  # Create a QLabel widget
        self.label6.setGeometry(10, 280, 600, 100)  # Adjust the geometry as needed

        font = QFont("Segoe UI", 20)  # Example: Arial font with a size of 12 points
        font.setBold(True)
        font2 = QFont("Segoe UI", 18)  # Example: Arial font with a size of 12 points

        self.label.setFont(font)
        self.label2.setFont(font2)
        self.label3.setFont(font2)
        self.label4.setFont(font2)
        self.label5.setFont(font2)
        self.label6.setFont(font2)

        compressed_file_path = "compressed_LZ78.txt"

        compressed_data, search_buffer_bits = self.read_compressed_data78(compressed_file_path)
        decoded_sequence = self.lz78_decompress(compressed_data)

        self.label.setText(f"Decompressed data: {decoded_sequence}")
        self.label2.setText(f"Matched Letter bits size is: {search_buffer_bits}")

        character_count = self.count_characters_in_compressed_file(compressed_file_path)

        # Calculate the sizes
        original_size = len(decoded_sequence)
        compressed_size = len(character_count)

        # Calculate the success rate
        success_rate = (1 - (compressed_size / original_size)) * 100

        self.label4.setText(f"Character count in compressed file: {compressed_size}")
        self.label5.setText(f"Character count in original string: {original_size}")
        self.label6.setText(f"Compression Success Rate: {success_rate:.2f}")

        self.show()
        self.pushButtonB78C.clicked.connect(self.toggle_back_decompress78)
        return 

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == '__main__':
    main()