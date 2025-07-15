import yaml
from pathlib import Path

def load_config(config_path: str = '../configs/parameters.yml'):
    """
    YAML設定ファイルを読み込む。

    Args:
        config_path (str): YAML設定ファイルへのパス。

    Returns:
        dict: 設定情報を含む辞書。エラーが発生した場合はNone。
    """
    path = Path(config_path)
    try:
        with path.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {path}")
        return None
    except Exception as e:
        print(f"Error loading or parsing YAML file at {path}: {e}")
        return None

def load_prompt_template(prompt_name: str) -> str:
    """
    configs/prompts/ ディレクトリからプロンプトテンプレートを読み込む。

    Args:
        prompt_name (str): .yml拡張子を除いたプロンプトファイル名。
                           例: "em_system_prompt"

    Returns:
        str: プロンプトのテンプレート文字列。エラーが発生した場合は空文字列。
    """

    prompt_path = Path("../configs/prompts") / f"{prompt_name}.yml"
    
    config = load_config(str(prompt_path))

    if config and "prompt_template" in config:
        return config["prompt_template"]
    elif config:
        print(f"Error: 'prompt_template' key not found in {prompt_path}")
        return ""
    else:
        return ""

def ensure_dir(path: str):
    """
    指定されたパスのディレクトリが存在することを確認し、なければ作成します。
    
    Args:
        path (str): ファイルまたはディレクトリのパス。
    """
    # パスがファイルの場合、その親ディレクトリを取得
    p = Path(path)
    dir_path = p.parent if p.suffix else p
    dir_path.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':

    # メイン設定の読み込み
    main_config = load_config()
    if main_config:
        print("--- メイン設定読み込み完了 ---")
        print(f"モデル名: {main_config.get('MODEL_NAME')}")

    # プロンプトテンプレートの読み込み
    em_prompt = load_prompt_template("em_system_prompt")
    if em_prompt:
        print("\n--- EMプロンプトテンプレート読み込み完了 ---")
        print(em_prompt)
