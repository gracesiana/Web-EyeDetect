from tensorflow.keras.models import load_model

model = load_model("ai_model/eye_disease_model.h5")

for i, layer in enumerate(model.layers):
    print(i, layer.name)