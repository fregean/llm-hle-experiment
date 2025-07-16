# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a machine learning experiment environment for evaluating large language models on the HLE (Humanity's Last Exam) dataset. The project uses structured prompts with multi-expert reasoning to evaluate models on two types of questions: Exact Match and Multiple Choice.

## Common Development Commands

### Environment Setup
```bash
# Initial setup
cp .env.example .env
cp configs/parameters.yml.example configs/parameters.yml

# Start Docker environment
docker-compose up -d --build

# Stop Docker environment
docker-compose down

# Access container shell
docker-compose exec app bash

# Test environment
python src/check_env.py
```

### Jupyter Notebook
```bash
# Access Jupyter Notebook at http://localhost:8888
docker-compose up -d
```

### Dependency Management
```bash
# After adding packages to requirements.txt
docker-compose down
docker-compose up -d --build
```

### GPU Support
```bash
# Use GPU-enabled configuration
docker-compose -f docker-compose.gpu.yml up -d --build
```

## Architecture and Code Structure

### Core Components

1. **ModelHandler** (`src/model_handler.py`): Manages LLM loading, inference, and output parsing
   - Loads models from Hugging Face Hub with bfloat16 precision
   - Handles chat template formatting for prompts
   - Parses structured output containing `<think>` blocks and JSON responses

2. **Data Loader** (`src/data_loader.py`): Handles HLE dataset loading
   - Filters text-only samples (excludes image-based questions)
   - Manages Hugging Face Hub authentication

3. **Configuration System** (`src/utils.py`): YAML-based configuration management
   - Loads experiment parameters from `configs/` directory
   - Supports prompt template loading from `configs/prompts/`

4. **Experiment Runner** (`notebooks/01_deepseek_experiment.ipynb`): Main experiment orchestration
   - Supports both local and Google Colab environments
   - Implements full inference pipeline with result storage

### Prompt Architecture

The system uses a structured multi-expert reasoning approach:

- **Exact Match** (`configs/prompts/em_system_prompt.yml`): For questions requiring precise answers
- **Multiple Choice** (`configs/prompts/mc_system_prompt.yml`): For multiple-choice questions

Both prompts follow a two-step process:
1. **Think Process**: Three expert personas analyze the problem
2. **JSON Output**: Structured response with explanation, answer, and confidence

### Configuration System

Configuration files in `configs/` directory:
- `parameters.yml.example`: Template for experiment parameters
- `deepseek_*.yml`: Specific model configurations
- `prompts/`: System prompts for different question types

Key parameters:
- `MODEL_NAME`: Hugging Face model identifier
- `DATASET_NAME`: Dataset name (typically "cais/hle")
- `NUM_SAMPLES_TO_RUN`: Limit samples for testing (comment out for full dataset)
- `MAX_LENGTH`: Maximum generation length
- `TEMPERATURE`: Generation temperature

### Output Structure

Results are saved as CSV files in `outputs/results/` with columns:
- `id`: Question identifier
- `question`: Original question text
- `ground_truth`: Correct answer
- `model_answer`: Model's parsed answer
- `confidence`: Model's confidence score
- `explanation`: Model's explanation
- `think_process`: Multi-expert reasoning process
- `parse_error`: JSON parsing errors (if any)
- `raw_output`: Complete model response

## Environment Variables

Required in `.env` file:
- `HUGGINGFACE_API_KEY` or `HF_TOKEN`: Hugging Face authentication token

## Data Flow

1. Load configuration from YAML files
2. Load HLE dataset and filter text-only samples
3. Initialize ModelHandler with specified model
4. For each sample:
   - Select appropriate prompt template based on `answer_type`
   - Generate response using model
   - Parse structured output (think process + JSON)
   - Store results with metadata
5. Save results to CSV file with configuration name prefix

## Key Implementation Details

- **Memory Optimization**: Uses bfloat16 precision and device_map="auto"
- **Output Parsing**: Robust regex-based extraction of think blocks and JSON responses
- **Error Handling**: Comprehensive error tracking for parsing failures
- **Dual Environment Support**: Works in both Docker and Google Colab environments
- **Caching**: Hugging Face cache is persisted via Docker volumes

## Testing and Validation

Use `python src/check_env.py` to validate:
- Python and PyTorch versions
- CUDA availability
- Library functionality (PyYAML, Pandas, Datasets, Transformers)
- Basic model inference capability

## File Name Conventions

- Configuration files use descriptive names including model and token length
- Output files are prefixed with configuration name: `{config_name}_results.csv`
- Prompt templates follow pattern: `{type}_system_prompt.yml`