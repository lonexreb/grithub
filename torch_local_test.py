# torch_local_test.py
from services.form_advice_service import form_advice_service_instance
text_prompt = "How to improve my tennis backhand?"
image_path = "/Users/lonexreb/Documents/hacklytics2025/grithub/TableTennis_wrist_handling/table-tennis-grip-shakehand.webp"

advice = form_advice_service_instance.generate_advice(text_prompt, image_path)
print("Advice:", advice)
