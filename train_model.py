import tensorflow as tf
# TensorFlow: digunakan sebagai framework utama untuk membangun, melatih, dan menyimpan model CNN.
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
# ImageDataGenerator: digunakan untuk melakukan pra-pemrosesan dan augmentasi citra agar model lebih robust.
from tensorflow.keras.models import Sequential
# Sequential: digunakan untuk menyusun arsitektur CNN secara berurutan dan sederhana.
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
# Conv2D: digunakan untuk mengekstraksi fitur penting citra seperti warna, tepi, dan tekstur.
# MaxPooling2D: digunakan untuk mengurangi dimensi data dan mempercepat komputasi.
# Flatten: digunakan untuk mengubah hasil ekstraksi fitur menjadi bentuk yang dapat diklasifikasikan.
# Dense: digunakan untuk melakukan klasifikasi berdasarkan fitur yang telah diekstraksi.
# Dropout: digunakan untuk mengurangi risiko overfitting selama proses pelatihan.
# GlobalAveragePooling2D: digunakan untuk merangkum feature map sehingga model lebih ringan.
# BatchNormalization: digunakan untuk menstabilkan nilai aktivasi dan mempercepat konvergensi training.
from tensorflow.keras.callbacks import EarlyStopping
# EarlyStopping: digunakan untuk menghentikan training otomatis saat model mulai overfitting.




from google.colab import drive
drive.mount('/content/drive')

# Preprocessing Dataset
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.25,

    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    brightness_range=[0.7, 1.3],
    horizontal_flip=True
)
train_generator = datagen.flow_from_directory(
    '/content/drive/MyDrive/tomato_ripeness_detector/tomato_ripeness_detector/dataset',
    target_size=(128, 128),
    batch_size=16,
    class_mode='categorical',
    subset='training',
    shuffle=True
)
validation_generator = datagen.flow_from_directory(
    '/content/drive/MyDrive/tomato_ripeness_detector/tomato_ripeness_detector/dataset',
    target_size=(128, 128),
    batch_size=16,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Arsitektur CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),

    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(3, activation='softmax')  # 3 kelas: mentah, setengah matang, matang
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

# Pelatihan Model
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=20,
    callbacks=[early_stop]
)

# Simpan Model
model.save('/content/drive/MyDrive/tomato_ripeness_detector/tomato_ripeness_detector/model/model7.h5')
print("Model saved to '/content/drive/MyDrive/tomato_ripeness_detector/tomato_ripeness_detector/model/model7.h5'")
