"""
Task 2: File Hash Generator

Function for calculating SHA-256 hashes for specified files
"""
import hashlib
import sys

def generate_file_hashes(*file_paths):
    """
    Calculates SHA-256 hash for each specified file
    
    Args:
        *file_paths: list of file paths
        
    Returns:
        dict: dictionary where key is the file path, value is SHA-256 hash in hexadecimal format
    """
    # Dictionary to store the results as required by the task
    # Format: {file_path: sha256_hash, ...}
    file_hashes = {}
    
    # Process each file
    for file_path in file_paths:
        try:
            # Open the file in binary mode
            with open(file_path, 'rb') as file:
                # Create SHA-256 hash object
                hasher = hashlib.sha256()
                
                # Read file in blocks for efficient memory usage
                # Block size - 8192 bytes (8 KB)
                chunk_size = 8192
                chunk = file.read(chunk_size)
                
                while chunk:
                    # Update the hash with data from the file
                    hasher.update(chunk)
                    # Read the next block
                    chunk = file.read(chunk_size)
                
                # Get the hash in hexadecimal format
                file_hash = hasher.hexdigest()
                
                # Save the result to the dictionary
                file_hashes[file_path] = file_hash
                
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except IOError as e:
            print(f"Error reading file '{file_path}': {e}")
        except Exception as e:
            print(f"Unexpected error processing file '{file_path}': {e}")
            
    # Return the dictionary with file paths and their SHA-256 hashes
    return file_hashes


# Example usage
if __name__ == "__main__":
    # Default files to hash
    default_files = ["file1.txt", "file2.txt", "apache_logs.txt"]
    
    # Check if file paths are provided as command line arguments
    if len(sys.argv) > 1:
        # Use all command line arguments after the script name as file paths
        files = sys.argv[1:]
    else:
        files = default_files
        print(f"No files specified, using defaults: {', '.join(default_files)}")
    
    # Calculate hashes
    hashes = generate_file_hashes(*files)
    
    # Output results
    print("File hashing results:")
    for file_path, file_hash in hashes.items():
        print(f"File: {file_path}")
        print(f"SHA-256: {file_hash}")
        print("-" * 50)
