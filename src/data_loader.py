# src/data_loader.py

import os
from datasets import load_dataset, Dataset

def load_hle_dataset(dataset_name: str, split: str = "test") -> Dataset:
    """
    Humanity's Last Exam (HLE) データセットをHugging Face Hubから読み込み、
    テキストのみのサンプルをフィルタリングする。

    Args:
        dataset_name (str): Hugging Face Hub上のデータセット名 (例: "cais/hle")。
        split (str): 読み込むデータセットの分割（例: "test"）。

    Returns:
        Dataset: テキストのみのサンプルが含まれるHugging Face Datasetオブジェクト。
    """
    print(f"Loading dataset: {dataset_name} (split: {split})")
    
    # .envから読み込まれたHUGGINGFACE_API_KEY（またはHF_TOKEN）を使用
    hf_token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
    if not hf_token:
        print("Warning: HUGGINGFACE_API_KEY not found in .env file. Access to gated datasets may fail.")

    dataset = load_dataset(dataset_name, split=split, token=hf_token)
    
    # 画像を含まないテキストのみのデータセットをフィルタリング
    original_size = len(dataset)
    text_only_dataset = dataset.filter(lambda x: x.get('image') == '' or x.get('image') is None)
    filtered_size = len(text_only_dataset)
    
    print(f"Original dataset size: {original_size}")
    print(f"Filtered to text-only dataset size: {filtered_size}")
    
    return text_only_dataset
