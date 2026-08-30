from dataclasses import dataclass


@dataclass
class ResponseProductRecord:
    name: str
    id: int | None = None
    unit: str | None = None
    description: str | None = None
