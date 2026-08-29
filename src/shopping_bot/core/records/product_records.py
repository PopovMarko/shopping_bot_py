from dataclasses import dataclass


@dataclass
class ResponseProductRecord:
    id: int
    name: str
    unit: str
    description: str | None = None
