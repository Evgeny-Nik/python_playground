import os


def parse_log_file(file_path, parsed_data):
    """parse a log file for INFO, ERROR, and WARNING logs, 
    and track unique users logging in and out."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                if "INFO" in line:
                    parsed_data["info_count"] += 1
                    if "logged" in line:
                        try:
                            username = line.split("User '")[1].split("'")[0]
                        # skip for malformed lines
                        except IndexError:
                            continue
                        if "in" in line:
                            parsed_data["unique_login"].add(username)
                        elif "out" in line:
                            parsed_data["unique_logout"].add(username)
                if "ERROR" in line:
                    parsed_data["error_count"] += 1
                if "WARNING" in line:
                    parsed_data["warning_count"] += 1

        return parsed_data


def parse_path(file_path):
    """parse all log files in the given directory."""
    if not os.path.isdir(file_path):
        print(f"Error: '{file_path}' is not a valid directory.")
        return
    
    try:
        os.listdir(file_path)  # Try accessing the directory to check permissions
    except PermissionError:
        print(f"Permission denied: You do not have access to '{file_path}'.")
        return
    
    parsed_data = {
        "info_count": 0,
        "error_count": 0, 
        "warning_count": 0, 
        "unique_login": set(),
        "unique_logout": set()
        }
    
    for (root, dirs, files) in os.walk(file_path):
        for file in files:
            if file.endswith('.log'):
                full_path = os.path.join(root, file)
                try:
                    print(f"Parsing log file: {full_path}")
                    parse_log_file(full_path, parsed_data)
                except (PermissionError, IOError) as e:
                    print(f"Skipping file {full_path} due to error: {e}")

    print_parsed_data(parsed_data)


def print_parsed_data(parsed_data):
    print(f"Total INFO logs: {parsed_data['info_count']}")
    print(f"Total ERROR logs: {parsed_data['error_count']}")
    print(f"Total WARNING logs: {parsed_data['warning_count']}")
    print(f"Unique users logged in: {len(parsed_data['unique_login'])}")
    print(f"Unique users logged out: {len(parsed_data['unique_logout'])}")
    print("Unique users who logged in:", ", ".join(parsed_data['unique_login']))
    print("Unique users who logged out:", ", ".join(parsed_data['unique_logout']))

if __name__ == "__main__":
    file_path = input("Enter the path to the log directory: ").strip()
    parse_path(file_path)

