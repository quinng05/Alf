import torch
from faster_whisper import WhisperModel

### Sets FW voice model based on system specs


# TO-DO set model for cuda based on GPU specs
def set_cuda_model(gpu):
    return WhisperModel("medium.en", device="cuda", compute_type="float16")

# check for CUDA 
def set_model():
    if(torch.backends.cuda.is_built()):
        print("Machine has CUDA -")
        print("GPU: ", torch.cuda.get_device_name(0))
        set_cuda_model(torch.cuda.get_device_name(0))
    else:
        print("No CUDA")
        print("Fetching FW model 'small' ...")
        return WhisperModel("small.en", device="cpu", compute_type="int8")
    
      





