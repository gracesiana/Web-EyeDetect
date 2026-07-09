from predict import predict_image

hasil, conf = predict_image(
    "EyeDetect/dataset/test/cataract/_0_4015166.jpg"
)

print("Hasil :", hasil)
print("Confidence :", conf)