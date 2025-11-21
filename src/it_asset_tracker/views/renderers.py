from typing import List, Dict, Any
from tabulate import tabulate

class TableRenderer:
    def __init__(self, formatter: callable = tabulate):
        self.formatter = formatter

    def render(self, data: List[Dict[str, Any]]) -> str:
        if not data:
            return "No data availible"

        headers = list(data[0].keys())
        rows = [list(row.values()) for row in data]
        return self.formatter(rows, headers=headers, tablefmt="grid")

class MenuRenderer:
    def render(self, title: str, options: List[str]) -> str:
        output = [f"\n===== {title} ====="]
        for option in options:
            output.append(option)
        return "\n".join(output)