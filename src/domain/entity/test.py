import datetime

from dataclasses import dataclass

@dataclass
class TestMaster():
    name: str
    type: str
    file_path: str | None = None
    modified_time: datetime
