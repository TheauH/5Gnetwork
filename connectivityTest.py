import re

def test_connections(input_string):
    pattern = r"uesimtun[0-2]"
    if re.search(pattern, input_string):
        return "Connections set up\n"
    else:
        return "Connections not set up\n"

# Test cases
test_string_1 = "This is a sample uesimtun0 string."
test_string_2 = "Another example with uesimtun1 in it."
test_string_3 = "No match for the pattern here."

# print(test_connections(test_string_1))  # Output: True
# print(test_connections(test_string_2))  # Output: True
# print(test_connections(test_string_3))  # Output: False
