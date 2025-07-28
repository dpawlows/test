import re
from typing import Dict, List, Any


def parse_input(filename: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_section = None
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                current_section = line[1:].strip().upper()
                data[current_section] = []
                continue
            if current_section is None:
                continue
            # Split off comment after the value
            value_str = re.split(r"\s+", line, 1)[0]
            try:
                # try int first then float
                if '.' in value_str:
                    value = float(value_str)
                else:
                    value = int(value_str)
            except ValueError:
                continue
            data[current_section].append(value)
    return data


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python parser.py <input_file>")
        return
    result = parse_input(sys.argv[1])
    for section, values in result.items():
        print(f"{section}: {values}")


if __name__ == "__main__":
    main()
