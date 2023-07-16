import time

def configurationTest(file_path, word, num_lines=10):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the last 'num_lines' lines from the file

        lines = file.readlines()[-num_lines:]

    # Search for the word in the last lines
    time.sleep(5)
    for line in lines:
        if word in line:
            return True
    return False

# Example usage:
# file_path = "path/to/your/file.txt"
# word_to_search = "target_word"
# num_lines_to_read = 20

# result = configurationTest(file_path, word_to_search, num_lines_to_read)

# if result:
#     print(f"The word '{word_to_search}' was found in the last {num_lines_to_read} lines.")
# else:
#     print(f"The word '{word_to_search}' was not found in the last {num_lines_to_read} lines.")
