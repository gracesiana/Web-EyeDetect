import tensorflow as tf

model = tf.keras.models.load_model(
    "ai_model/eye_disease_model.h5"
)

model.summary()