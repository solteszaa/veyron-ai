import os
import sys
from agency_swarm.agents.agent import Agent

# Eredeti _read_instructions metódus mentése
original_read_instructions = Agent._read_instructions

# Új _read_instructions metódus létrehozása, amely UTF-8 kódolással olvassa be a fájlokat
def patched_read_instructions(self):
    """
    UTF-8 kódolással olvassa be az instrukciós fájlt.
    """
    if isinstance(self.instructions, str) and os.path.exists(self.instructions):
        with open(self.instructions, 'r', encoding='utf-8') as f:
            self.instructions = f.read()

# Az eredeti metódus felülírása a patchelt verzióval
Agent._read_instructions = patched_read_instructions

print("Az Agent osztály _read_instructions metódusa sikeresen patchelve lett UTF-8 kódolás támogatással.") 