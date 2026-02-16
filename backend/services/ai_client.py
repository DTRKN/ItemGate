from fastapi import HTTPException
from pydantic import ValidationError
import httpx
from typing import Dict, Any
import yaml
from pathlib import Path
import asyncio
import json
import logging

from config import config 
from services.prompt_manager import prompt_manager
from schemas.item import ItemInfo_ai

logger = logging.getLogger(__name__)


class OpenRouterClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai"

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(connect=5.0, read=30.0, write=10.0, pool=5.0),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",   
                "HTTP-Referer": "https://www.google.com", 
                "X-Title": "Google", 
            },
            follow_redirects=True
        )

    async def get_response(self, user_data: str) -> ItemInfo_ai:
            
            system_prompt = await prompt_manager.load_system_prompt(config.prompt_system_generate_info)
            payload = {
                "model": "stepfun/step-3.5-flash:free",
                "messages": [
                    {"role": "system", "content": system_prompt['content']},
                    {"role": "user", "content": user_data},
                ],
            }
            response = await self.client.post(
                url=f"{self.base_url}/api/v1/chat/completions",
                json=payload 
            )
            response.raise_for_status()

            content = response.json()['choices'][0]['message']['content']
            
            print(content)

            data_dict = json.loads(str(content))
            try:
                result = ItemInfo_ai.model_validate(data_dict)
            except ValidationError as e:
                logger.exception("AI response validation failed: %s", e)
                raise HTTPException(status_code=502, detail="AI returned JSON with unexpected schema") from e

            return result

openRouterClient = OpenRouterClient(config.AI_KEY)