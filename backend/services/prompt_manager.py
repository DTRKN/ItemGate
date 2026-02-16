import yaml
from pathlib import Path

class PromptManager:

    @staticmethod
    async def load_system_prompt(path: str) -> str:
        with open(Path(path), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data["system"]
    
prompt_manager = PromptManager()