
========== Page https://www.microsoft.com/en-us/research/blog/promptwizard-the-future-of-prompt-optimization-through-feedback-driven-self-evolving-prompts/ ==========:

[Skip to main content](javascript:void(0))

[Return to Blog Home](https://www.microsoft.com/en-us/research/blog/)

## Microsoft Research Blog

![A diagram illustrating the joint optimization process of instructions and in-context examples in PromptWizard. The figure demonstrates how the framework iteratively refines both components, integrating feedback to enhance the overall prompt effectiveness and adaptability across tasks. ](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/PromptWizard-BlogHeroFeature-1400x788-1.png)

## The challenge of effective prompting

AI is reshaping industries—from education to healthcare—thanks to advancements in large language models (LLMs). These models rely on prompts, carefully crafted inputs that guide them to produce relevant and meaningful outputs. While the impact of prompts is profound, creating prompts that can help with complex tasks is a time-intensive and expertise-heavy process, often involving months of trial and error.

This challenge grows as new tasks arise and models evolve rapidly, making manual methods for prompt engineering increasingly unsustainable. The question then becomes: **How can we make prompt optimization faster, more accessible, and more adaptable across diverse tasks?**

- Download [PromptWizard](https://github.com/microsoft/PromptWizard)

To address this challenge, we developed PromptWizard (PW), a research framework that automates and streamlines the process of prompt optimization. We are open sourcing the [PromptWizard codebase (opens in new tab)](https://github.com/microsoft/PromptWizard) to foster collaboration and innovation within the research and development community.

## Introducing PromptWizard

PromptWizard (PW) is designed to **automate and simplify prompt optimization**. It combines iterative feedback from LLMs with efficient exploration and refinement techniques to **create highly effective prompts within minutes**.

**PromptWizard optimizes both the instruction and the in-context learning examples.** Central to PW is its self-evolving and self-adaptive mechanism, where the LLM iteratively generates, critiques, and refines prompts and examples in tandem. This process ensures continuous improvement through feedback and synthesis, achieving a holistic optimization tailored to the specific task at hand. By evolving both instructions and examples simultaneously, PW ensures significant gains in task performance.

**Three key insights behind PromptWizard**:

- _Feedback-driven refinement:_ At its core, PW leverages an iterative feedback loop where the LLM generates, critiques, and refines its own prompts and examples. This continuous improvement mechanism ensures that each iteration is better than the last, leading to highly effective prompts and examples.
- _Joint optimization and synthesis of diverse examples:_ PW generates synthetic examples that are not only robust and diverse but also task-aware. By optimizing prompts and examples together, it ensures they work in tandem to address specific task requirements effectively.
- _Self-generated chain-of-thought (CoT) steps_: Incorporating CoT reasoning improves the problem-solving capabilities of the model. By using selected few-shot examples, PW generates a detailed reasoning chain for each example, facilitating nuanced and step-by-step problem-solving approaches.

![Fig 1: A diagram providing an overview of the PromptWizard process. It illustrates the main components, including iterative prompt generation, feedback-based refinement, and joint optimization of instructions and examples. The workflow emphasizes modularity and adaptability, demonstrating how PromptWizard evolves prompts to improve performance across diverse tasks.](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/PromptWizard_Fig-1.png)Figure 1. Overview of PromptWizard

## How PromptWizard works

PromptWizard begins with a user input: a problem description, an initial prompt instruction, and a few training examples that serve as a foundation for the task at hand.

Its output is a refined, optimized set of prompt instructions paired with carefully curated in-context few-shot examples. These outputs are enriched with detailed reasoning chains, task intent, and an expert profile that bridges human-like reasoning with the AI’s responses.

**Stage 1: Refinement of prompt instruction**

The first stage focuses on refining the task instructions of a prompt. PromptWizard generates multiple candidate instructions, evaluates them using feedback from the LLM, and iteratively synthesizes improved versions. This process balances **exploration**—trying diverse ideas—and **exploitation**—refining the most promising ones.

For example, if an initial instruction yields suboptimal results, PW incorporates feedback to identify its shortcomings and generates an improved version. Over three to five iterations, this iterative cycle ensures that the instruction converges to an optimal state.

![Fig 2: A visualization of the refinement process for prompt instructions in PromptWizard. The figure highlights iterative improvements, where initial instructions are critiqued, adjusted based on feedback, and fine-tuned to achieve greater accuracy and alignment with task objectives.](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/PromptWizard_Fig-2.png)Figure 2. Refinement of prompt instruction

**Stage 2: Joint optimization of instructions and examples**

The refined prompt obtained from Stage 1 is combined with carefully selected examples, and both are optimized together. Through the critique-and-synthesis mechanism, PromptWizard ensures alignment between the prompt and examples, simultaneously synthesizing new examples to enhance task performance.

This structured approach makes PromptWizard highly versatile, adapting to tasks as varied as solving math problems or generating creative content.

![Fig 3: A diagram illustrating the joint optimization process of instructions and in-context examples in PromptWizard. The figure demonstrates how the framework iteratively refines both components, integrating feedback to enhance the overall prompt effectiveness and adaptability across tasks.](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/PromptWizard_Fig-3.png)Figure 3. Joint optimization of instructions and examples

Microsoft Research Blog

[![White outline illustrations for AIOps on a blue and green gradient background.](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/AIOps-Lab-BlogHeroFeature-1400x788-1.png)](https://www.microsoft.com/en-us/research/blog/aiopslab-building-ai-agents-for-autonomous-clouds/)

## AIOpsLab: Building AI agents for autonomous clouds

AIOpsLab is an open-source framework designed to evaluate and improve AI agents for cloud operations, offering standardized, scalable benchmarks for real-world testing, enhancing cloud system reliability.

[Read more](https://www.microsoft.com/en-us/research/blog/aiopslab-building-ai-agents-for-autonomous-clouds/)

Opens in a new tab

## Results

PromptWizard stands out for its feedback-driven refinement and systematic exploration, delivering exceptional results across a wide variety of tasks while maintaining computational efficiency.

### Comprehensive evaluation across tasks

PromptWizard was rigorously evaluated on over 45 tasks, spanning both general and domain-specific challenges. Benchmarked against state-of-the-art techniques—including Instinct, InstructZero, APE, PromptBreeder, EvoPrompt, DSPy, APO, and PromptAgent—PW consistently outperformed competitors in accuracy, efficiency, and adaptability. Please see detailed results in [our paper](https://www.microsoft.com/en-us/research/publication/promptwizard-task-aware-agent-driven-prompt-optimization-framework/).

- **Accuracy**: PW consistently outperformed other methods, maintaining performance close to the best across all tasks. Figure 4 shows the performance profile curve that highlights PW’s reliability, demonstrating how frequently it achieves near-best accuracy compared to other approaches for BigBench Instruction Induction dataset (BBII).
- **Efficiency**: Beyond accuracy, PW demonstrates its computational efficiency. Unlike many baseline methods that require extensive API calls and computational resources, PW achieves superior results with minimal overhead by striking an effective balance between exploration and exploitation. Table 1 demonstrates PW’s cost-effectiveness, with significantly reduced token usage for input and output while optimizing prompts effectively.

![Fig 4: A performance profile curve illustrating PromptWizard's reliability on the BigBench Instruction Induction (BBII) dataset. The curve demonstrates how often PromptWizard achieves accuracy levels close to the best performance when compared to other approaches, highlighting its consistency and effectiveness.](https://www.microsoft.com/en-us/research/uploads/prod/2024/12/PromptWizard_Fig-4.png)Figure 4. Performance Profile curve on BBII dataset

| Methods | API calls | Total tokens |
| --- | --- | --- |
| Instinct | 1730 | 115k |
| PromptBreeder | 18600 | 1488k |
| EvoPrompt | 5000 | 400k |
| **PW** | **69** | **24k** |

Table 1. Cost analysis on BBII dataset

We also have conducted numerous experiments to highlight PromptWizard’s efficacy with limited training data and smaller LLMs.

### Resilience with limited data

Real-world scenarios often lack abundant training data. PW excels in such conditions, requiring as few as five examples to produce effective prompts. Across five diverse datasets, PW demonstrated an average accuracy drop of only 5% when using five examples compared to 25 examples—highlighting its adaptability and efficiency (see Table 2).

| Datasets | 5 Examples | 25 Examples |
| --- | --- | --- |
| MMLU | 80.4 | 89.5 |
| GSM8k | 94 | 95.4 |
| Ethos | 86.4 | 89.4 |
| PubMedQA | 68 | 78.2 |
| MedQA | 80.4 | 82.9 |
| **Average** | **81.9** | **87** |

Table 2. PW’s performance with varying number of examples

### Leveraging smaller models for optimization

PromptWizard also reduces computational costs by using smaller LLMs for prompt generation, reserving more powerful models for inference. For example, using Llama-70B for prompt generation resulted in negligible performance differences compared to GPT-4, while significantly lowering resource usage (see Table 3).

| Dataset | Prompt Gen: Llama-70B | Prompt Gen: GPT4 |
| --- | --- | --- |
| GSM8k | 94.6 | 95.4 |
| Ethos | 89.2 | 89.4 |
| **Average** | **91.9** | **92.4** |

Table 3. Performance with smaller LLMs for prompt generation

PromptWizard shows that effective prompts combine optimized instructions refined through iterative feedback, thoughtfully chosen in-context examples, and a modular design that incorporates expert knowledge and task-specific intent. This approach enables the framework to handle a broad range of tasks, from simple to highly complex, with exceptional efficiency and flexibility.

Whether you are a researcher addressing cutting-edge challenges or an organization looking to streamline workflows, PromptWizard provides a practical, scalable, and impactful solution for enhancing model performance.