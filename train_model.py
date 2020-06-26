from keras.callbacks import CSVLogger, EarlyStopping, ModelCheckpoint
from keras_preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np
import pdb

from DataProcessing.util import append_png
from nn_model import build_simple_model, build_model, IMAGE_SIZE


EPOCHS = 20
BATCH_SIZE_TRAIN = 1
BATCH_SIZE_TEST = 1


# Read training and testing sprites
traindf = pd.read_csv('Dataset/train.csv', names=['Sprite', 'Types'])
testdf = pd.read_csv('Dataset/test.csv', names=['Sprite', 'Types'])

traindf = traindf.sort_values('Sprite')
testdf = testdf.sort_values('Sprite')

traindf['Sprite'] = traindf['Sprite'].apply(append_png)
testdf['Sprite'] = testdf['Sprite'].apply(append_png)

datagen = ImageDataGenerator(rescale=1/255, validation_split=0.2)


# Train generator to feed training data to NN
train_generator = datagen.flow_from_dataframe(
    dataframe=traindf,
    directory='Dataset/Train',
    x_col='Sprite',
    y_col='Types',
    subset='training',
    batch_size=BATCH_SIZE_TRAIN,
    seed=42,
    shuffle=True,
    class_mode='categorical',
    target_size=IMAGE_SIZE,
    validate_filenames=False
)


# Validation generator to feed validation data to NN
valid_generator = datagen.flow_from_dataframe(
    dataframe=traindf,
    directory='Dataset/Train',
    x_col='Sprite',
    y_col='Types',
    subset='validation',
    batch_size=BATCH_SIZE_TRAIN,
    seed=42,
    shuffle=True,
    class_mode='categorical',
    target_size=IMAGE_SIZE,
    validate_filenames=False
)


# Build model 
model = build_simple_model()


# Stream epoch results to csv
# epoch_log = CSVLogger('log.csv', append=False, separator=';')


# Save best model
best_model = ModelCheckpoint(
        'best_model.h5', 
        monitor='val_accuracy', 
        mode='max', 
        verbose=1, 
        save_best_only=True
)


# Train model
STEP_SIZE_TRAIN = train_generator.n // train_generator.batch_size
STEP_SIZE_VALID = valid_generator.n // valid_generator.batch_size

model.fit(
    x=train_generator,
    validation_data=valid_generator,
    validation_steps=STEP_SIZE_VALID,
    epochs=EPOCHS,
    steps_per_epoch=STEP_SIZE_TRAIN,
    verbose=1
    # callbacks=[best_model]
)

model.evaluate(x=valid_generator, steps=STEP_SIZE_VALID)


# Test model
test_datagen = ImageDataGenerator(rescale=1/255)

test_generator = test_datagen.flow_from_dataframe(
    dataframe=testdf,
    directory='Dataset/Test',
    x_col='Sprite',
    y_col='Types',
    batch_size=BATCH_SIZE_TEST,
    class_mode='categorical',
    target_size=IMAGE_SIZE,
    validate_filenames=False
)

STEP_SIZE_TEST = test_generator.n // test_generator.batch_size

test_generator.reset()
pred = model.predict(
    test_generator,
    steps=STEP_SIZE_TEST,
    verbose=1
)

predicted_class_indices = np.argmax(pred, axis=1)

labels = train_generator.class_indices
labels = dict((v,k,) for k, v in labels.items())
predictions = [labels[k] for k in predicted_class_indices]


# Temporary evaluator
print('==========results==========')
answer = testdf['Types'].tolist()
print(predictions[:])
print(answer)
count, i = 0, 0
for prediction in predictions:
    if prediction != answer[i]:
        count += 1
    i += 1
print('score: ', count, ' / ', len(answer))
print('accuracy: ', count / len(predictions))
