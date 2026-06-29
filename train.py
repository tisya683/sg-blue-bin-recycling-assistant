import tensorflow as tf
import numpy as np
from PIL import Image
from utils import (class_names, material_map, recyclable_map,rule_engine)


#best run of mobilenetv2 
model=tf.keras.models.load_model("best_mobilenetv2.keras")

def predict_img(image: Image.Image, is_clean: bool, is_dry: bool, is_rigid: bool)-> dict[str,str]:

    image = image.convert("RGB")# previously not converting to greyscale caused model to suck at predicting uploade/webcam pics  
    image = image.resize((160,160))
    image = np.array(image)
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)[0]

    # print probabilities for debugging
    print("\nPredictions:")
    for i, p in enumerate(prediction):
        print(f"{class_names[i]}: {p:.2%}")

    index=np.argmax(prediction)
    confidence=float(np.max(prediction))

    category=class_names[index]
    material=material_map.get(category)
    recyclable=recyclable_map.get(category)

    rule_engine_result=rule_engine(category, is_clean, is_dry, is_rigid)

    return {
        "predicted_category": category,
        "material": material,
        "recyclability": recyclable,
        "confidence": f"{confidence:.2%}",
        "explanation": rule_engine_result["Explanation"]
    }
