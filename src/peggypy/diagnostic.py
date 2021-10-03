

from typing import Any
from dataclasses import dataclass

@dataclass
class Diagnostic:
    message:str
    location:Any