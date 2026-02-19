from dataclasses import dataclass, field
from typing import List

@dataclass
class AgentState:
    goal: str
    memory: List[str] = field(default_factory=list)
    observations: List[str] = field(default_factory=list)
    completed_steps: List[str] = field(default_factory=list)