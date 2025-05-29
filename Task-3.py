"""
Task 3: IP Address Filtering from Files

Function for filtering IP addresses from log files and counting allowed IP address occurrences
"""
import re
import sys

def filter_ips(input_file_path, output_file_path, allowed_ips):
    """
    Analyzes IP addresses from a log file and filters them based on an allowed list
    
    Args:
        input_file_path (str): path to the input log file
        output_file_path (str): path to the output file for results
        allowed_ips (list): list of allowed IP addresses
        
    Returns:
        dict: dictionary where key is the allowed IP address, value is the number of occurrences
    """
    # Dictionary to store the results as required by the task
    # Format: {ip_address: count, ...} - initializing with all allowed IPs set to 0
    ip_counts = {ip: 0 for ip in allowed_ips}
    
    try:
        # Open the input file for reading
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            # Regular expression to find IP addresses
            # Matches IP format: xxx.xxx.xxx.xxx
            ip_pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            
            # Read each line of the file
            for line in input_file:
                # Search for IP address
                match = re.search(ip_pattern, line)
                if match:
                    # Get the IP address
                    ip = match.group(1)
                    # Check if this IP is in the allowed list
                    if ip in allowed_ips:
                        # Increment the counter for this IP in our dictionary
                        ip_counts[ip] += 1
        
        # Write the results to the output file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for ip, count in ip_counts.items():
                output_file.write(f"{ip} - {count}\n")
                
        # Return the dictionary with IP addresses and their counts
        return ip_counts
                
    except FileNotFoundError:
        print(f"Error: Input file '{input_file_path}' not found.")
        return {}
    except IOError as e:
        print(f"Error working with files: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return {}


# Example usage
if __name__ == "__main__":
    # Default file paths
    default_input_path = "apache_logs.txt"
    default_output_path = "allowed_ips_count.txt"
    
    # Default allowed IP addresses
    default_allowed_ips = [
        "192.168.1.1",
        "10.0.0.1",
        "127.0.0.1",
        "172.16.0.1",
        "83.149.9.216"
    ]
    
    # Check if file paths are provided as command line arguments
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = default_input_path
        print(f"No input file specified, using default: {default_input_path}")
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        output_path = default_output_path
        print(f"No output file specified, using default: {default_output_path}")
    
    # Using default allowed IPs (for command line arguments, you would typically
    # read these from a configuration file or pass them in a different way)
    allowed_ips = default_allowed_ips
    print(f"Using allowed IPs: {', '.join(allowed_ips)}")
    
    # Filter IP addresses
    result = filter_ips(input_path, output_path, allowed_ips)
    
    if result:
        print("IP address filtering results:")
        for ip, count in result.items():
            print(f"IP: {ip}, occurrences: {count}")
        print(f"Results saved to file: {output_path}")
