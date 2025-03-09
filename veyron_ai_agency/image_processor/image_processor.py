from agency_swarm import Agent

class ImageProcessor(Agent):
    def __init__(self):
        super().__init__(
            name="ImageProcessor",
            description="Képek feldolgozására és ImgBB-re való feltöltésére specializálódott ágens.",
            instructions="./instructions.md",
            tools_folder="./tools",
            temperature=0.5,
            max_prompt_tokens=25000,
        ) 