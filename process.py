import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained("priyanshisalujaaa112/waf_roberta")
tokenizer = AutoTokenizer.from_pretrained("priyanshisalujaaa112/waf_roberta")
model.eval()

def process(log):
    inputs = tokenizer(
        log,
        return_tensors="pt",
        truncation=True,
        padding=False,
        max_length=256
    )

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)

    malicious_prob = probs[0][1].item()
    prediction = int(malicious_prob > 0.5)

    return {
        "prediction": prediction,
        "malicious_probability": malicious_prob
    }