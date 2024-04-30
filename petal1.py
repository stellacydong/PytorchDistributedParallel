from accelerate import Accelerator
from transformers import AutoTokenizer
import torch
import time

# Attempt to import the correct class from petals.client
try:
    from petals.client import DistributedLlamaForCausalLM  # Try this import
except ImportError:
    print("Error importing 'DistributedLlamaForCausalLM'. Please check your petals installation.")

# Initialize the Accelerator for multi-GPU setup
accelerator = Accelerator()

# GPT-2 Small model with 124M parameters
model_path = "petals-team/StableBeluga2"  # Example model from Petals
num_gpus = torch.cuda.device_count()

print(f"Using {num_gpus} GPUs for distributed processing.")

# Check if the import was successful before proceeding
if 'DistributedLlamaForCausalLM' in globals():
    # Set the correct device and load the model
    current_device = torch.device(f"cuda:{accelerator.process_index}")
    model = DistributedLlamaForCausalLM.from_pretrained(
        model_path,
        device_map={"": current_device},  # Explicitly set the device
        torch_dtype=torch.float16,  # Mixed precision for efficiency
    )

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Example prompts for testing
    prompts = ["Hello, world!", "What's your favorite movie?", "Tell me a story."]

    # Synchronize GPUs and start the timer
    accelerator.wait_for_everyone()
    start_time = time.time()

    # Distribute prompts across GPUs and gather results
    outputs = []
    gpu_usage = []

    with accelerator.split_between_processes(prompts) as subset_prompts:
        gpu_start_time = time.time()  # Start time for GPU processing
        for prompt in subset_prompts:
            inputs = tokenizer(prompt, return_tensors="pt").to(current_device)
            generated_ids = model.generate(inputs["input_ids"], max_new_tokens=50)
            generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            outputs.append(generated_text)

    # Synchronize processes and calculate inference time
    accelerator.wait_for_everyone()
    elapsed_time = time.time() - start_time

    # Display results if in the main process
    if accelerator.is_main_process():
        print(f"Inference completed in {elapsed_time:.2f} seconds.")
        print("Generated Outputs:")
        for i, output in enumerate(outputs):
            print(f"Output {i + 1}: {output}")

else:
    print("Failed to import the required class. Please ensure 'petals' is correctly installed and updated.")