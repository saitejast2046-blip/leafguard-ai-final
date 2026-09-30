"""Train and evaluate MobileNetV3 on PlantVillage, then export a TensorFlow Lite model.
Run in Google Colab with a GPU: python train.py"""
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from sklearn.metrics import classification_report, confusion_matrix

IMG, BATCH = 224, 64


def load_data():
    (tr, va, te), info = tfds.load(
        "plant_village",
        split=["train[:70%]", "train[70%:85%]", "train[85%:]"],
        with_info=True, as_supervised=True)
    prep = lambda x, y: (tf.image.resize(x, (IMG, IMG)), y)
    aug = tf.keras.Sequential([
        tf.keras.layers.RandomFlip(), tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomBrightness(0.2), tf.keras.layers.RandomZoom(0.15)])
    tr = (tr.map(prep).shuffle(2000).batch(BATCH)
          .map(lambda x, y: (aug(x, training=True), y)).prefetch(2))
    va = va.map(prep).batch(BATCH).prefetch(2)
    te = te.map(prep).batch(BATCH).prefetch(2)
    return tr, va, te, info.features["label"].names


def build_model(n_classes):
    base = tf.keras.applications.MobileNetV3Small(
        input_shape=(IMG, IMG, 3), include_top=False, weights="imagenet", pooling="avg")
    base.trainable = False
    model = tf.keras.Sequential([base, tf.keras.layers.Dropout(0.2),
                                 tf.keras.layers.Dense(n_classes, activation="softmax")])
    return base, model


def main():
    tr, va, te, names = load_data()
    base, model = build_model(len(names))
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(tr, validation_data=va, epochs=3)
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False
    model.compile(tf.keras.optimizers.Adam(1e-4), "sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(tr, validation_data=va, epochs=5,
              callbacks=[tf.keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)])
    y_true = np.concatenate([y.numpy() for _, y in te])
    y_pred = np.argmax(model.predict(te), axis=1)
    print(classification_report(y_true, y_pred, target_names=names))
    print(confusion_matrix(y_true, y_pred))
    conv = tf.lite.TFLiteConverter.from_keras_model(model)
    conv.optimizations = [tf.lite.Optimize.DEFAULT]
    with open("leafguard.tflite", "wb") as f:
        f.write(conv.convert())


if __name__ == "__main__":
    main()
