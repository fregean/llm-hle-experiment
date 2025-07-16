# src/model_handler.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
import json

class ModelHandler:
    """
    大規模言語モデルの読み込み、推論、出力解析を管理するクラス。
    """
    def __init__(self, model_name: str, hf_token: str = None):
        """
        モデルとトークナイザーを初期化してロードします。

        Args:
            model_name (str): Hugging Face Hub上のモデル名。
            hf_token (str, optional): Hugging Face Hubの認証トークン。
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing ModelHandler on device: {self.device}")

        print(f"Loading tokenizer: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            print("Warning: tokenizer.pad_token is not set. Setting it to tokenizer.eos_token.")


        print(f"Loading model: {model_name}")
        # bfloat16を使用してメモリ使用量を削減
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto", # 自動的にGPU/CPUを割り当て
            trust_remote_code=True,
            token=hf_token
        )
        print("Model and tokenizer loaded successfully.")

    def generate(self, prompt: str, max_length: int, temperature: float) -> str:
        """
        与えられたプロンプトからテキストを生成します。

        Args:
            prompt (str): モデルへの入力プロンプト。
            max_length (int): 生成されるテキストの最大長。
            temperature (float): 生成のランダム性を制御する温度。

        Returns:
            str: モデルによって生成された生のテキスト。
        """
        messages = [{"role": "user", "content": prompt}]
        
        # トークナイザーはinput_idsとattention_maskを含む辞書を返す
        input_ids_tensor = self.tokenizer.apply_chat_template(
            messages,
            return_tensors="pt",
            add_generation_prompt=True
        ).to(self.device)

        outputs = self.model.generate(
            input_ids_tensor,
            max_new_tokens=max_length, 
            temperature=temperature,
            do_sample=True if temperature > 0 else False,
            pad_token_id=self.tokenizer.eos_token_id
        )
        # モデルの出力から生成されたテキストをデコード
        input_length = input_ids_tensor.shape[1]
        response_text = self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
        
        return response_text

    def parse_output(self, raw_text: str) -> dict:
        """
        モデルの生の出力から<think>ブロックとJSONブロックを抽出・解析します。

        Args:
            raw_text (str): モデルの生の出力文字列。

        Returns:
            dict: 解析されたデータを含む辞書。
        """
        parsed_data = {
            "think_process": None,
            "explanation": None,
            "answer": None,
            "confidence": None,
            "error": None
        }

        # 1. <think>ブロックを抽出
        think_match = re.search(r"<think>(.*?)</think>", raw_text, re.DOTALL)
        if think_match:
            parsed_data["think_process"] = think_match.group(1).strip()

        # 2. JSONブロックを抽出
        # ```json ... ``` の有無に関わらず、最も内側にある {...} を探す
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            try:
                # JSON文字列をクリーンアップ（末尾のカンマなど）
                json_string = re.sub(r",\s*(\}|\])", r"\1", json_string)
                json_data = json.loads(json_string)
                
                parsed_data.update(json_data) # 抽出したJSONデータをマージ

            except json.JSONDecodeError as e:
                parsed_data["error"] = f"JSON parsing failed: {e}"
                print(f"JSON parsing failed: {e}\\nRaw JSON string: {json_string}")
        else:
            parsed_data["error"] = "No JSON block found in the output."
            print("No JSON block found in the output.")
            
        return parsed_data
