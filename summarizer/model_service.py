import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Base model (replace with what you used originally)
BASE_MODEL = "meta-llama/Llama-2-7b-hf"

# Path to LoRA checkpoint
ADAPTER_PATH = "finetunedModel/checkpoint-20"

print("Loading model... this may take a while.")

# Load base + tokenizer
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_auth_token=True)
model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=torch.float16, device_map="auto")

# Attach LoRA adapter
model = PeftModel.from_pretrained(model, ADAPTER_PATH)

def generate_text(prompt, max_new_tokens=200):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        temperature=0.7,
        top_p=0.9,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
