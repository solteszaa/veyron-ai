from agency_swarm import Agent

class WebhookManager(Agent):
    def __init__(self):
        super().__init__(
            name="WebhookManager",
            description="A generált tartalom webhookra való küldésére specializálódott ágens.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.3,  # Alacsonyabb kreativitás, precízebb működés
            max_prompt_tokens=25000,
        ) 