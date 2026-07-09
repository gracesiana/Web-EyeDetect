from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
model = None
feature_model = None

classes = [
    'Cataract',
    'Diabetic Retinopathy',
    'Glaucoma',
    'Normal'
]

# ==========================
# EXTRACT FEATURES
# ==========================

def _load_model():
    global model, feature_model
    if model is None or feature_model is None:
        from tensorflow.keras.models import load_model, Model
        from tensorflow.keras.preprocessing import image

        model = load_model(BASE_DIR / 'eye_disease_model.h5')
        feature_model = Model(
            inputs=model.input,
            outputs=model.layers[-2].output
        )
    return model, feature_model


def extract_features(img_path):
    import numpy as np
    from tensorflow.keras.preprocessing import image

    _, feature_model = _load_model()

    img = image.load_img(
        img_path,
        target_size=(224,224)
    )

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    features = feature_model.predict(img_array)
    return features


# ==========================
# PREDICT IMAGE
# ==========================

def predict_image(img_path):
    from tensorflow.keras.preprocessing import image

    model, _ = _load_model()

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