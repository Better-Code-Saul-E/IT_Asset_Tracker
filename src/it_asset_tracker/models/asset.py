from dataclasses import dataclass
from typing import Optional

@dataclass
class Asset:
    id: Optional[int]
    device_type: str
    manufacturer: str
    model: str
    serial_number: str