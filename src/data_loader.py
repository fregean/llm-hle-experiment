import os
from pathlib import Path
from datasets import load_dataset, Dataset

def load_hle_dataset(dataset_name: str, split: str = "test") -> Dataset:
    """
    HLEデータセットをHugging Face Hubから読み込む。
    失敗した場合は、ローカルのParquetファイルからの読み込みを試みる。

    Args:
        dataset_name (str): Hugging Face Hub上のデータセット名。
        split (str): 読み込むデータセットの分割。

    Returns:
        Dataset: テキストのみのサンプルが含まれるHugging Face Datasetオブジェクト。
    """
    try:
        # --- 1. Hugging Face Hubからのダウンロードを試みる ---
        print(f"Attempting to load dataset from Hugging Face Hub: {dataset_name} (split: {split})")
        hf_token = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN")
        if not hf_token:
            print("Warning: HUGGINGFACE_API_KEY not found. Access to gated datasets may fail.")

        dataset = load_dataset(dataset_name, split=split, token=hf_token)
        print("✅ Successfully loaded from Hugging Face Hub.")

    except Exception as e:
        # --- 2. 失敗した場合、ローカルファイルからの読み込みに切り替える ---
        print(f"❌ Failed to load from Hugging Face Hub: {e}")
        print("Switching to loading from local Parquet file...")
        
        # プロジェクトルートからの相対パスを指定
        local_file_path = Path("data/test-00000-of-00001.parquet")
        
        if not local_file_path.exists():
            print(f"Error: Local file not found at {local_file_path}")
            print("Please download 'test-00000-of-00001.parquet' into the 'data' directory.")
            return None # または raise FileNotFoundError(f"...")

        dataset = load_dataset('parquet', data_files={'test': str(local_file_path)}, split=split)
        print(f"✅ Successfully loaded from local file: {local_file_path}")

    # --- 3. 共通のフィルタリング処理 ---
    # 画像を含まないテキストのみのデータセットをフィルタリング
    original_size = len(dataset)
    text_only_dataset = dataset.filter(lambda x: x.get('image') == '' or x.get('image') is None)
    filtered_size = len(text_only_dataset)
    
    print(f"Original dataset size: {original_size}")
    print(f"Filtered to text-only dataset size: {filtered_size}")
    
    return text_only_dataset
