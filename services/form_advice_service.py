import torch
from transformers import AutoModel, AutoProcessor
from PIL import Image

class FormAdviceService:
    def __init__(self):
        self.model = AutoModel.from_pretrained("unum-cloud/uform-gen2-dpo", trust_remote_code=True)
        # Force everything to float32
        self.model.to(dtype=torch.float32)
        self.model.eval()

        self.processor = AutoProcessor.from_pretrained("unum-cloud/uform-gen2-dpo", trust_remote_code=True)

    def generate_advice(self, prompt: str, image_path: str) -> str:
        image = Image.open(image_path)
        inputs = self.processor(text=[prompt], images=[image], return_tensors="pt")

        # Also force input to float32
        for k, v in inputs.items():
            if torch.is_tensor(v):
                inputs[k] = v.to(torch.float32)

        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                do_sample=False,
                use_cache=True,
                max_new_tokens=25,
                min_new_tokens=10,
                eos_token_id=151645
            )

        prompt_len = inputs["input_ids"].shape[1]
        decoded_text = self.processor.batch_decode(output[:, prompt_len:])[0]
        if "<|im_end|>" in decoded_text:
            final_text = decoded_text.split("<|im_end|>")[0]
        else:
            final_text = decoded_text
        return final_text

form_advice_service_instance = FormAdviceService()
