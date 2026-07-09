from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LAST_CONV_LAYER = "Conv_1"


def _load_gradcam_model():
    import tensorflow as tf
    from tensorflow.keras.models import load_model

    model = load_model(BASE_DIR / "eye_disease_model.h5")
    return tf, model


def generate_gradcam(img_path, output_path):
    import numpy as np
    import cv2
    import tensorflow as tf
    from tensorflow.keras.preprocessing import image

    tf, model = _load_gradcam_model()

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [
            model.get_layer(LAST_CONV_LAYER).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        class_idx = np.argmax(predictions[0])

        loss = predictions[:, class_idx]

    grads = tape.gradient(loss, conv_outputs)

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

    heatmap = tf.squeeze(heatmap)

    heatmap = np.maximum(
        heatmap,
        0
    ) / np.max(heatmap)

    img_original = cv2.imread(img_path)

    heatmap = cv2.resize(
        heatmap,
        (
            img_original.shape[1],
            img_original.shape[0]
        )
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    superimposed_img = cv2.addWeighted(
        img_original,
        0.6,
        heatmap,
        0.4,
        0
    )

    cv2.imwrite(
        output_path,
        superimposed_img
    )

    return output_path