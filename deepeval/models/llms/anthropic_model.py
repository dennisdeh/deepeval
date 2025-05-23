from typing import Optional, Tuple, Union, Dict
from anthropic import Anthropic, AsyncAnthropic
from pydantic import BaseModel
import json
import os
import re

from deepeval.models import DeepEvalBaseLLM

model_pricing = {
    "claude-3-7-sonnet-latest": {"input": 3.00 / 1e6, "output": 15.00 / 1e6},
    "claude-3-5-haiku-latest": {"input": 0.80 / 1e6, "output": 4.00 / 1e6},
    "claude-3-5-sonnet-latest": {"input": 3.00 / 1e6, "output": 15.00 / 1e6},
    "claude-3-opus-latest": {"input": 15.00 / 1e6, "output": 75.00 / 1e6},
    "claude-3-sonnet-20240229": {"input": 3.00 / 1e6, "output": 15.00 / 1e6},
    "claude-3-haiku-20240307": {"input": 0.25 / 1e6, "output": 1.25 / 1e6},
    "claude-instant-1.2": {"input": 0.80 / 1e6, "output": 2.40 / 1e6},
}


class AnthropicModel(DeepEvalBaseLLM):
    def __init__(
        self,
        model: str = "claude-3-7-sonnet-latest",
        _anthropic_api_key: Optional[str] = None,
    ):
        model_name = model
        self._anthropic_api_key = _anthropic_api_key
        super().__init__(model_name)

    ###############################################
    # Generate functions
    ###############################################

    def generate(
        self, prompt: str, schema: Optional[BaseModel] = None
    ) -> Tuple[Union[str, Dict], float]:
        chat_model = self.load_model()
        message = chat_model.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        cost = self.calculate_cost(
            message.usage.input_tokens, message.usage.output_tokens
        )
        if schema == None:
            return message.content[0].text, cost
        else:
            json_output = self.trim_and_load_json(message.content[0].text)

            return schema.model_validate(json_output), cost

    async def a_generate(
        self, prompt: str, schema: Optional[BaseModel] = None
    ) -> Tuple[str, float]:
        chat_model = self.load_model()
        message = await chat_model.messages.create(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
        )
        cost = self.calculate_cost(
            message.usage.input_tokens, message.usage.output_tokens
        )
        if schema == None:
            return message.content[0].text, cost
        else:
            json_output = self.trim_and_load_json(message.content[0].text)

            return schema.model_validate(json_output), cost

    ###############################################
    # Utilities
    ###############################################

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        pricing = model_pricing.get(self.model_name, model_pricing)
        input_cost = input_tokens * pricing["input"]
        output_cost = output_tokens * pricing["output"]
        return input_cost + output_cost

    def trim_and_load_json(
        self,
        input_string: str,
    ) -> Dict:
        start = input_string.find("{")
        end = input_string.rfind("}") + 1
        if end == 0 and start != -1:
            input_string = input_string + "}"
            end = len(input_string)
        jsonStr = input_string[start:end] if start != -1 and end != 0 else ""
        jsonStr = re.sub(r",\s*([\]}])", r"\1", jsonStr)
        try:
            return json.loads(jsonStr)
        except json.JSONDecodeError:
            error_str = "Evaluation LLM outputted an invalid JSON. Please use a better evaluation model."
            raise ValueError(error_str)
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    ###############################################
    # Model
    ###############################################

    def load_model(self, async_mode: bool = False):
        if not async_mode:
            return Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY")
                or self._anthropic_api_key
            )
        else:
            return AsyncAnthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY")
                or self._anthropic_api_key
            )

    def get_model_name(self):
        return f"{self.model_name}"
