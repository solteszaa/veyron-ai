from agency_swarm import Agent

class PropertyCollector(Agent):
    def __init__(self):
        super().__init__(
            name="PropertyCollector",
            description="Ingatlanadatok gyűjtésére és validálására specializálódott ágens.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=25000,
        ) 