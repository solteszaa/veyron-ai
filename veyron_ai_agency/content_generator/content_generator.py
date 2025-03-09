from agency_swarm import Agent

class ContentGenerator(Agent):
    def __init__(self):
        super().__init__(
            name="ContentGenerator",
            description="Social media posztok és hashtag-ek generálására specializálódott ágens.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.7,  # Kicsit magasabb kreativitás
            max_prompt_tokens=25000,
        ) 