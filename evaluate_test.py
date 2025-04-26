import os
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Configuration
BASE_MODEL_PATH = "/DATA/Shubham/Projects/IndicTrans2/huggingface_interface/indictrans2-en-indic-1B"
LORA_CHECKPOINT = "/DATA/Shubham/Projects/Kashmiri_language_Translation/lora-output/checkpoint-4500"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def load_models():
    base_model = AutoModelForSeq2SeqLM.from_pretrained(
        BASE_MODEL_PATH,
        trust_remote_code=True,
        device_map="auto"
    )
    
    peft_config = PeftConfig.from_pretrained(LORA_CHECKPOINT)
    ft_model = PeftModel.from_pretrained(
        base_model,
        LORA_CHECKPOINT,
        device_map="auto"
    )
    
    # Verify model sizes
    print(f"\n[MODEL] Base params: {sum(p.numel() for p in base_model.parameters()):,}")
    print(f"[MODEL] LoRA params: {sum(p.numel() for p in ft_model.parameters()):,}")
    
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_PATH,
        trust_remote_code=True,
        use_fast=False
    )
    
    return ft_model, base_model, tokenizer

def translate_sentence(sentence, model, tokenizer, processor):
    # Format with proper tags and spacing
    formatted_input = f"<2en><2kas> {sentence}"
    
    processed_src = processor.preprocess_batch(
        [formatted_input],
        src_lang="eng_Latn",
        tgt_lang="kas_Arab",
        is_target=False
    )[0]
    print(f"\n[DEBUG] Processed input: {processed_src}")

    inputs = tokenizer(
        processed_src,
        return_tensors="pt",
        max_length=256,
        truncation=True,
        padding="longest"
    ).to(DEVICE)
    
    # Debug tokenization
    print(f"[TOKEN] Input IDs: {inputs.input_ids}")
    print(f"[TOKEN] Decoded: {tokenizer.decode(inputs.input_ids[0])}")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=256,
            num_beams=5,
            early_stopping=True
        )

    translation = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    ).strip()
    
    return translation

if __name__ == "__main__":
    processor = IndicProcessor(inference=False)
    ft_model, base_model, tokenizer = load_models()
    
    test_sentence = "Hello world"
    
    try:
        print("\n=== Testing Base Model ===")
        base_translation = translate_sentence(test_sentence, base_model, tokenizer, processor)
        
        print("\n=== Testing Fine-Tuned Model ===")
        ft_translation = translate_sentence(test_sentence, ft_model, tokenizer, processor)
    except Exception as e:
        print(f"Error: {e}")
        raise

    print(f"\n{' INPUT ':=^50}")
    print(test_sentence)
    
    print(f"\n{' BASE ':=^50}")
    print(base_translation)
    
    print(f"\n{' FINE-TUNED ':=^50}")
    print(ft_translation)


