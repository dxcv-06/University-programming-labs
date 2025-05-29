"""
Task 1: Log File Analyzer

Function for analyzing HTTP server log files and counting unique response codes
"""
import re
import sys

def analyze_log_file(log_file_path):
    """
    Analyzes HTTP server log file and counts the number of unique response codes

    Args:
        log_file_path (str): path to the HTTP server log file

    Returns:
        dict: dictionary where key is the response code, value is the number of occurrences
    """
    # Dictionary to store the results as required by the task
    # Format: {response_code: count, ...}
    response_codes = {}
    
    try:
        # Open the file for reading
        with open(log_file_path, 'r', encoding='utf-8') as file:
            # Regular expression to find HTTP response codes
            # Typical Apache log file format: IP - - [date] "GET /path HTTP/1.1" 200 1234
            pattern = r'\s(\d{3})\s'
            
            # Read each line of the file
            for line in file:
                # Search for HTTP response code
                match = re.search(pattern, line)
                if match:
                    # Get the response code
                    response_code = match.group(1)
                    # Increment the counter for this code
                    if response_code in response_codes:
                        response_codes[response_code] += 1
                    else:
                        response_codes[response_code] = 1
                        
        # Return the dictionary with response codes and their counts
        return response_codes
    
    except FileNotFoundError:
        print(f"Error: File '{log_file_path}' not found.")
        return {}
    except IOError as e:
        print(f"Error reading file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return {}


# Example usage
if __name__ == "__main__":
    # Default log file path
    default_log_path = "apache_logs.txt"
    
    # Check if file path is provided as command line argument
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
    else:
        log_path = default_log_path
        print(f"No log file specified, using default: {default_log_path}")
    
    result = analyze_log_file(log_path)
    
    if result:
        print("Log file analysis results:")
        for code, count in result.items():
            print(f"Response code {code}: {count} occurrences")
