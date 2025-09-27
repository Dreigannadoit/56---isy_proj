import os
import json
from typing import Dict, Any, Tuple
from langchain.chat_models import init_chat_model

CHAT_MODEL = "qwen3:4b"

class Word_Assesment:
    """Handles scoring for words based on various criteria"""

    def __init__(self, llm):
        self.llm
