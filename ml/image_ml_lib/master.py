import os
import sys
from transformers import CLIPProcessor, CLIPModel

for x in ["/home/samir/Desktop/ARIMA/colab/server"]:
    if os.path.isdir(x):
        sys.path.insert(0, x)

class ImageMaster:

    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")    

    def vector_product(self, images, text):
        classes = ["This is a picture of " + text, "This is not a picture of " + text]

        inputs = self.processor(text=classes, images=images, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image 
        probs = logits_per_image.softmax(dim=1)
        return bool((probs[0][0] > probs[0][1]).detach().numpy())
    
    def vector_product_magnitude(self, images, text):
        classes = ["This is a picture of " + text, "This is not a picture of " + text]

        inputs = self.processor(text=classes, images=images, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image 
        probs = logits_per_image.softmax(dim=1)
        if bool((probs[0][0] > probs[0][1]).detach().numpy()):
            return float(probs[0][0].detach().numpy())
        else:
            return 0.0