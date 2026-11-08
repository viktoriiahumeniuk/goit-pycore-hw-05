import sys
from datetime import datetime


def parse_log_line(line: str) -> dict:
    date, time, level, message = line.strip().split(maxsplit=3)
    datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    if level not in ("INFO", "DEBUG", "ERROR", "WARNING"):
        raise ValueError(f"Unknown logging level: {level}")
    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }

def load_logs(file_path: str) -> list:
    logs = []
    with open(file_path) as file:
        for line in file:
            logs.append(parse_log_line(line))
    return logs
    

def filter_logs_by_level(logs: list, level: str) -> list:
    level = level.upper()
    return [log for log in logs if log["level"] == level]

def count_logs_by_level(logs: list) -> dict:
    counted_logs = {
        "INFO": 0,
        "DEBUG": 0, 
        "ERROR": 0, 
        "WARNING": 0
    }
    for log in logs:
        level = log["level"]
        counted_logs[level] += 1
    return counted_logs


def display_log_counts(counts: dict):
    print(f"{'Log level':<16} | Number")
    print("-----------------|----------")

    for level, count in counts.items():
        print(f"{level:<16} | {count}")

def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python main.py <file_path> [level]")
        return

    file_path = sys.argv[1]

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Couldn't find the file: {file_path}")
        return
    except (OSError, UnicodeError) as error:
        print(f"Couldn't read the file: {error}")
        return
    except ValueError as error:
        print(f"Incorrect format of logging: {error}")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)

        print(f"\nLog details for level '{level.upper()}':")

        if not filtered_logs:
            print(f"Couldn't find info on the log level '{level.upper()}':")

        for log in filtered_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()