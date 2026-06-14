from pathlib import Path
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing import image
import numpy as np

# ==========================
# LOAD MODEL
# ==========================

BASE_DIR = Path(__file__).resolve().parent

model = load_model(
    BASE_DIR / 'eye_disease_model.h5'
)

# ==========================
# FEATURE EXTRACTION MODEL
# ==========================

feature_model = Model(
    inputs=model.input,
    outputs=model.layers[-2].output
)

# ==========================
# CLASS LABEL
# ==========================

classes = [
    'Cataract',
    'Diabetic Retinopathy',
    'Glaucoma',
    'Normal'
]

# ==========================
# EXTRACT FEATURES
# ==========================

def extract_features(img_path):

    img = image.load_img(
        img_path,
        target_size=(224,224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array /= 255.0

    features = feature_model.predict(img_array)

    return features


# ==========================
# PREDICT IMAGE
# ==========================

def predict_image(img_path):

    img = image.load_img(
        img_path,
        target_size=(224,224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array /= 255.0

    prediction = model.predict(img_array)

    print("PREDICTION RAW:", prediction)

    result = classes[np.argmax(prediction)]

    confidence = np.max(prediction) * 100

    return result, confidence