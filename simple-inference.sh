# # python3 -m pip install transformers accelerate torch bitsandbytes

# # huggingface-cli login --token  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 --add-to-git-credential

# export NCCL_P2P_DISABLE="1"
# export NCCL_IB_DISABLE="1"

# # Set the correct number of processes and machines
# accelerate launch \
#   --num_processes 8 \
#   --num_machines 1 \
#   --mixed_precision "no" \
#   PytorchDistributedParallel/simple-inference.py


# Shell script to set up the environment and run the code

echo "Setting up Accelerate configuration..."

# Set the correct number of processes and machines
accelerate launch \
  --num_processes 8 \
  --num_machines 1 \
  --mixed_precision "no" \
  -distributed_type "multi-GPU" \
  PytorchDistributedParallel/simple-inference.py

  
# accelerate config 

# Use the following configuration:
# - Device placement: default
# - Mixed precision: no
# - Number of machines: 1
# - Number of processes per machine: 8
# - Distributed type: multi-GPU
# - Use torch.distributed.launch for distributed training
# - Configure other parameters as needed

echo "Launching multi-GPU script with Accelerate..."
# Replace 'simple-inference.py' with the name of your Python script
accelerate launch simple-inference.py
