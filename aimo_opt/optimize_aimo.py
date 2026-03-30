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

from loguru import logger


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

        try:
            # First try to find Python code blocks
            import re
            code_pattern = r'```python\s*(.*?)\s*```'
            code_matches = re.findall(code_pattern, answer, re.DOTALL)

            if code_matches:
                # Take the last code block if multiple exist
                code = code_matches[-1].strip()

                # Execute the code using PythonREPL
                from promptwizard.glue.common.utils.python_repl import PythonREPL
                repl = PythonREPL(timeout=10)
                success, output = repl(code)

                if success:
                    # Extract the last numeric value from output
                    import re
                    numbers = re.findall(r'-?\d+\.?\d*', output)
                    if numbers:
                        # Take the last number printed
                        answer = str(int(float(numbers[-1])))
                        logger.info(f"Extracted answer {answer} from code output: {output}")
                        return answer
                    else:
                        logger.warning(f"No numeric output found in code execution result: {output}")
                else:
                    logger.warning(f"Code execution failed: {output}")

            # If no code block or execution failed, try boxed notation
            boxed_pattern = r'\\boxed\{([^}]+)\}'
            boxed_matches = re.findall(boxed_pattern, answer)

            if boxed_matches:
                # Take the last boxed answer if multiple exist
                answer = boxed_matches[-1].strip()
                # Convert to numeric and back to string to standardize
                answer = str(int(float(answer)))
                return answer

            logger.warning(f"Could not find valid answer in response:\n{answer}")
            return self.INVALID_ANS

        except Exception as e:
            logger.error(f"Error extracting answer: {str(e)}")
            return self.INVALID_ANS


def main():
    # Create data directory if it doesn't exist
    if not os.path.exists("opt_data"):
        os.makedirs("opt_data")

    # Load AIME 2024 problems for test set
    import pandas as pd
    train_data = pd.read_parquet("data/aimo-validation-aime/data/train-00000-of-00001.parquet")
    train_data = train_data[train_data['url'].str.contains('2024', na=False)]
    train_data = train_data.to_dict('records')

    # Load sample problems for training set
    from sample_problems import aimo_sample_problems
    test_data = [{"problem": p.problem_statement, "answer": p.solution} for p in aimo_sample_problems]

    # Initialize processor
    amc_processor = AMCProcessor()

    # Save train and test files
    amc_processor.dataset_to_jsonl("opt_data/train.jsonl", dataset=train_data)

    amc_processor.dataset_to_jsonl("opt_data/test.jsonl", dataset=test_data)

    # Set up paths
    train_file_name = os.path.join("opt_data", "train.jsonl")

    # logger.critical("TEMP_TWEAK: training on test")  # @TEMP_TWEAK
    # train_file_name = os.path.join("opt_data", "test.jsonl")

    test_file_name = os.path.join("opt_data", "test.jsonl")
    path_to_config = "configs"

    promptopt_config_path = os.path.join(path_to_config, "promptopt_config.yaml")

    # logger.critical("TEMP_TWEAK: using test config")  # @TEMP_TWEAK
    # promptopt_config_path = os.path.join(path_to_config, "test_promptopt_config.yaml")

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
        generate_synthetic_examples=False,
    )

    # Save results
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    with open(os.path.join(results_dir, "best_prompt.pkl"), 'wb') as f:
        pickle.dump(best_prompt, f)
    with open(os.path.join(results_dir, "expert_profile.pkl"), 'wb') as f:
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
