# src/test.py
import sys
import torch
import pandas as pd
import yaml
from transformers import pipeline
from datasets import Dataset

def test_environment():
    """
    Docker環境が正しくセットアップされているかを確認する。
    """
    print("="*50)
    print("=== LLM Experiment Environment Test Start ===")
    print("="*50)

    # 1. PythonとPyTorchの基本的な情報をチェック
    print(f"🐍 Python version: {sys.version}")
    print(f"🔥 PyTorch version: {torch.__version__}")

    # 2. GPUが利用可能かチェック (最も重要なチェックの一つ)
    is_cuda_available = torch.cuda.is_available()
    print(f" CUDA available: {'✅ Yes' if is_cuda_available else '❌ No'}")
    if is_cuda_available:
        print(f"   - GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"   - CUDA version: {torch.version.cuda}")
    else:
        print("   - Running on CPU. This is expected on machines without an NVIDIA GPU (e.g., Mac).")

    # 3. 設定ファイル(YAML)の読み込みをテスト
    print("\n🧪 Testing YAML configuration loading...")
    try:
        test_yaml_string = "key: value"
        data = yaml.safe_load(test_yaml_string)
        if data['key'] == 'value':
            print("   - ✅ PyYAML is working correctly.")
        else:
            raise ValueError("YAML value mismatch")
    except Exception as e:
        print(f"   - ❌ PyYAML test failed: {e}")

    # 4. PandasとDatasetsの基本的な動作をテスト
    print("\n🧪 Testing data handling libraries...")
    try:
        pd.DataFrame({'col1': [1, 2]})
        Dataset.from_dict({'text': ['test']})
        print("   - ✅ Pandas and Datasets are working correctly.")
    except Exception as e:
        print(f"   - ❌ Data handling library test failed: {e}")

    # 5. Transformersのパイプラインを使った簡単な推論テスト
    # これにより、PyTorchとTransformersが連携して動作することを確認できる
    print("\n🧪 Testing Transformers pipeline (this may download a small model)...")
    try:
        # sentiment-analysisは軽量でテストに適している
        classifier = pipeline('sentiment-analysis')
        result = classifier('We are very happy to test this environment!')
        print(f"   - ✅ Transformers pipeline test successful. Result: {result}")
    except Exception as e:
        print(f"   - ❌ Transformers pipeline test failed: {e}")
        print("   - Note: This might be due to a network issue if it's trying to download a model.")

    print("\n" + "="*50)
    print("=== Test Complete ===")
    print("="*50)

if __name__ == "__main__":
    test_environment()
