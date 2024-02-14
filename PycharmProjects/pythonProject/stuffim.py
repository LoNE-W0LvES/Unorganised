# Example of a Caesar cipher encryption in Python

# Define the original message
message = "I like you"

# Define the encryption key (shift value)
key = 3

# Initialize an empty string to store the encrypted message
encrypted_message = ""

# Iterate through each character in the message
for char in message:
    # Check if the character is an uppercase letter
    if char.isupper():
        # Apply the Caesar cipher encryption to uppercase letters
        encrypted_char = chr((ord(char) - 65 + key) % 26 + 65)
    # Check if the character is a lowercase letter
    elif char.islower():
        # Apply the Caesar cipher encryption to lowercase letters
        encrypted_char = chr((ord(char) - 97 + key) % 26 + 97)
    else:
        # Keep non-alphabetic characters unchanged
        encrypted_char = char
    # Add the encrypted character to the encrypted message
    encrypted_message += encrypted_char

# Print the encrypted message
print("Encrypted message:", encrypted_message)