from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
from io import BytesIO
from PIL import Image
import numpy as np
from keras.models import load_model
from keras.preprocessing import image

app = FastAPI()

model_path = ""
model = load_model(model_path)


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Read image file
        contents = await file.read()
        pil_image = Image.open(BytesIO(contents))

        # Preprocess the image here (the same way you did during training)
        img = pil_image.resize((128, 128))  # Example resize, adjust to your model's input size
        img_array = np.array(img)
        img_array = img_array / 255.0  # Example normalization, adjust as per your model's training
        img_array = img_array[np.newaxis, ...]

        # Prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)

        # Assuming you have a mapping of class indices to Pokémon names
        class_names = ['Pikachu', 'Bulbasaur', 'Charmander']  # Example, adjust as needed
        predicted_name = class_names[predicted_class[0]]

        return JSONResponse(content={"predicted_name": predicted_name}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": f"An error occurred: {str(e)}"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
