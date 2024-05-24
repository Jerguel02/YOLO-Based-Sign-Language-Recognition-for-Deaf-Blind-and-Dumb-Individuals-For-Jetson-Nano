import torch

if torch.cuda.is_available():
    print(f"CUDA is available. Number of GPU(s): {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
    print(f"CUDA version: {torch.version.cuda}")
else:
    print("CUDA is not available.")