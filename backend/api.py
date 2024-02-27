from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import numpy as np
from keras.models import load_model

app = FastAPI()

# Add CORSMiddleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_path = "../model/models/current_model.h5"
model = load_model(model_path)


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pil_image = Image.open(BytesIO(contents))

        # Resize the image to match the model's expected input size
        img = pil_image.resize((200, 200))

        # Convert the image to array
        img_array = np.array(img)

        # Ensure the image has 3 channels (RGB)
        if img_array.ndim == 2:  # It's a grayscale image
            img_array = np.stack((img_array,) * 3, axis=-1)
        elif img_array.shape[2] == 4:  # It's RGBA
            img_array = img_array[..., :3]

        # Add a batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]

        class_names = ['Pikachu', 'Jigglypuff']
        predicted_name = class_names[predicted_class]

        class_probabilities = prediction[0].tolist()  # Convert to list for JSON serialization

        return JSONResponse(content={"predicted_name": predicted_name, "class_probabilities": class_probabilities}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"An error occurred: {e}", "predicted_name": "Error predicting"}, status_code=500)

