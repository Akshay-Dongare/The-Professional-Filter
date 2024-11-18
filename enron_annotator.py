import pandas as pd
import json
from guardrails import Guard, OnFailAction
from guardrails.hub import RegexMatch
from groq import Groq

class EmailAnnotator:
    def __init__(self, dataset_path, api_keys_path):
        self.dataset_path = dataset_path
        self.api_keys = self.load_api_keys(api_keys_path)

    def load_api_keys(self, filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def load_data(self):
        return pd.read_csv(self.dataset_path, usecols=['message'])

    def my_custom_groq_api(self, api_key=None, **kwargs):
        """Custom LLM API wrapper for Groq.

        At least one of messages should be provided.

        Args:
            messages: The messages to be passed to the Groq API

        Returns:
            str: The output of the Groq API
        """
        messages = kwargs.pop("messages", [])
        groq_client = Groq(api_key=api_key)
        response = groq_client.chat.completions.create(model="llama3-70b-8192", messages=messages, max_tokens=len(messages)+1, **kwargs)
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    def guarded_groq_call(self, prompt='', api_key=None):
        """Guards the Groq API call to ensure the output is a binary classification."""
        guard = Guard().use(
            RegexMatch,
            regex=r"^[01]$",
            on_fail=OnFailAction.REASK
        )
        validated_response = guard(
            self.my_custom_groq_api,
            messages=[{"role":"system", "content":"If a message is about a social event inside the company, such as celebrating a new baby of an employee, or a career promotion, it belongs to the first category 1 (work-related). If a message is about a social event outside the company but still related to the company, such as a picnic (usually family members are invited), it belongs to the second category 0 (non-work-related). If a message is about a social event which is not related to the company such as a charity but company employees are encouraged to participate, it belongs to the second category 0 (non-work-related). If a message is too short to determine its category (or even empty), it should have the same category as the message it is responding to, or the message it is forwarding. If a message is ambiguous, try to read other messages in the thread to clarify. If a message is spam or in the rare case that the first message of a thread is very short or empty, say 1 (work-related)"},
                     {"role":"user", "content":"For the following email, please classify it as 1 (work-related) or 0 (non-work-related). Do not include any other text in your response: " + prompt}],
            api_key=api_key
        )
        return validated_response
