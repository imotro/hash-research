import hashlib
import itertools
import os
import time
import sys

# Configuration
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB
OUTPUT_DIR = '../output'
ALL_CHARACTERS = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"  # All typable characters

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

def hash_string(s):
    """Hashes a string using SHA-256."""
    return hashlib.sha256(s.encode()).hexdigest()

def write_to_file(file_name, data):
    """Writes data to a specified file."""
    with open(file_name, 'a') as f:
        f.write(data)

def generate_hashes(length):
    """Generates hashes for all typable strings of a given length."""
    start_time = time.time()
    part = 1
    file_name = os.path.join(OUTPUT_DIR, f"{length}.txt")
    file_size = 0

    for combo in itertools.product(ALL_CHARACTERS, repeat=length):
        string = ''.join(combo)
        hash_val = hash_string(string)
        entry = f"{hash_val}, {string}\n"

        # Check if a new file is needed
        if file_size + len(entry.encode()) > MAX_FILE_SIZE:
            part += 1
            file_name = os.path.join(OUTPUT_DIR, f"{length}-{part}.txt")
            file_size = 0

        write_to_file(file_name, entry)
        file_size += len(entry.encode())

    end_time = time.time()
    print(f"Operation completed in {end_time - start_time:.5f} seconds.")

def unhash_string(length, target_hash):
    """Attempts to find the original string for a given hash."""
    try:
        part = 1
        while True:
            file_name = os.path.join(OUTPUT_DIR, f"{length}-{part}.txt")
            if not os.path.exists(file_name):
                file_name = os.path.join(OUTPUT_DIR, f"{length}.txt")
                if not os.path.exists(file_name):
                    break
            with open(file_name, 'r') as file:
                for line in file:
                    hash_val, string = line.strip().split(', ')
                    if hash_val == target_hash:
                        return string
            part += 1
    except Exception as e:
        print(f"Error occurred during lookup: {e}")
    return None

def main():
    if len(sys.argv) > 1:
        # Command-line arguments provided
        choice = sys.argv[1]
        if choice == '1' and len(sys.argv) == 3:
            length = int(sys.argv[2])
            generate_hashes(length)
        elif choice == '2' and len(sys.argv) == 4:
            length = int(sys.argv[2])
            target_hash = sys.argv[3]
            result = unhash_string(length, target_hash)
            if result:
                print(f"Original string: {result}")
            else:
                print("Hash not found.")
        else:
            print("Invalid command-line arguments.")
    else:
        # Interactive mode
        choice = input("Enter '1' to generate hashes or '2' to unhash: ")
        if choice == '1':
            length = int(input("Enter string length to hash: "))
            generate_hashes(length)
        elif choice == '2':
            length = int(input("Enter string length to unhash: "))
            target_hash = input("Enter hash to unhash: ")
            result = unhash_string(length, target_hash)
            if result:
                print(f"Original string: {result}")
            else:
                print("Hash not found.")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
