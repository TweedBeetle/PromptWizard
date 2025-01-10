import pickle
import sys

from promptwizard.glue.common.utils.runtime_tasks import logger

sys.path.insert(0, "../")
import promptwizard
from promptwizard.glue.promptopt.instantiate import GluePromptOpt
from promptwizard.glue.promptopt.techniques.common_logic import DatasetSpecificProcessing
from promptwizard.glue.common.utils.file import save_jsonlist
from typing import Any
from tqdm import tqdm
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


class AMCProcessor(DatasetSpecificProcessing):
    def __init__(self):
        super().__init__()
        self.INVALID_ANS = "[invalid]"

    def dataset_to_jsonl(self, dataset_jsonl: str, **kwargs: Any) -> None:
        examples_set = []

        for _, sample in tqdm(enumerate(kwargs["dataset"]), desc="Processing samples"):
            example = {
                DatasetSpecificProcessing.QUESTION_LITERAL: sample['problem'],
                DatasetSpecificProcessing.ANSWER_WITH_REASON_LITERAL: sample.get('solution', ''),
                DatasetSpecificProcessing.FINAL_ANSWER_LITERAL: str(sample['answer'])
            }
            examples_set.append(example)

        save_jsonlist(dataset_jsonl, examples_set, "w")

    def extract_final_answer(self, answer: str):
        if not answer:
            return self.INVALID_ANS

        # Extract numeric answer from the response
        try:
            # Look for answer between tags if present
            if "<ANS_START>" in answer and "<ANS_END>" in answer:
                start_idx = answer.find("<ANS_START>") + len("<ANS_START>")
                end_idx = answer.find("<ANS_END>")
                answer = answer[start_idx:end_idx].strip()

            # Convert to numeric and back to string to standardize
            answer = str(int(float(answer.strip())))
            return answer
        except:
            return self.INVALID_ANS


def main():
    # Create data directory if it doesn't exist
    if not os.path.exists("aimo_opt/opt_data"):
        os.makedirs("aimo_opt/opt_data")

    # Load AMC validation dataset and filter for 2024
    import pandas as pd
    dataset = pd.read_parquet("data/aimo-validation-aime/data/train-00000-of-00001.parquet")

    # Filter for 2024 problems by checking URL
    dataset = dataset[dataset['url'].str.contains('2024', na=False)]
    dataset = dataset.to_dict('records')

    # Initialize processor
    amc_processor = AMCProcessor()

    # Split into train/test (using first 25 for train, rest for test)
    train_data = dataset[:25]
    test_data = dataset[25:]

    # Save train and test files
    amc_processor.dataset_to_jsonl("aimo_opt/opt_data/train.jsonl", dataset=train_data)
    amc_processor.dataset_to_jsonl("aimo_opt/opt_data/test.jsonl", dataset=test_data)

    # Set up paths
    train_file_name = os.path.join("aimo_opt/opt_data", "train.jsonl")
    test_file_name = os.path.join("aimo_opt/opt_data", "test.jsonl")
    path_to_config = "configs"

    # promptopt_config_path = os.path.join(path_to_config, "promptopt_config.yaml")

    logger.critical("TEMP_TWEAK: using test config")  # @TEMP_TWEAK
    promptopt_config_path = os.path.join(path_to_config, "test_promptopt_config.yaml")

    setup_config_path = os.path.join(path_to_config, "setup_config.yaml")

    # Initialize prompt optimization
    gp = GluePromptOpt(
        promptopt_config_path,
        setup_config_path,
        train_file_name,
        amc_processor
    )

    # Get optimized prompt
    best_prompt, expert_profile = gp.get_best_prompt(
        use_examples=True,
        run_without_train_examples=False,
        generate_synthetic_examples=False
    )

    # Save results
    if not os.path.exists("results"):
        os.makedirs("results")

    with open("aimo_opt/results/best_prompt.pkl", 'wb') as f:
        pickle.dump(best_prompt, f)
    with open("aimo_opt/results/expert_profile.pkl", 'wb') as f:
        pickle.dump(expert_profile, f)

    print(f"Best prompt: {best_prompt}")
    print(f"Expert profile: {expert_profile}")

    # Evaluate on test set
    gp.EXPERT_PROFILE = expert_profile
    gp.BEST_PROMPT = best_prompt
    accuracy = gp.evaluate(test_file_name)
    print(f"Final Accuracy: {accuracy}")


if __name__ == "__main__":
    main()
