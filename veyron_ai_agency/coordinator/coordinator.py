from agency_swarm import Agent

class Coordinator(Agent):
    def __init__(self):
        super().__init__(
            name="Coordinator",
            description="Fő kommunikációs pont a felhasználóval, kezeli a teljes folyamatot és delegálja a feladatokat.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=25000,
        ) 