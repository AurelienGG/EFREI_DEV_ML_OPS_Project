async function uploadAndPredict() {
    let imageUpload = document.getElementById('imageUpload');
    let formData = new FormData();
    formData.append("file", imageUpload.files[0]);

    // Display uploaded image
    let uploadedImage = document.getElementById('uploadedImage');
    uploadedImage.src = URL.createObjectURL(imageUpload.files[0]);
    uploadedImage.hidden = false;


    // API call to prediction endpoint
    let response = await fetch('http://localhost:8000/predict/', {
        method: 'POST',
        body: formData
    });
    let result = await response.json();

    // Display prediction results
    let predictionResult = document.getElementById('predictionResult');
    predictionResult.hidden = false;
    predictionResult.innerHTML = `<p>Predicted Name:<br/> ${result.predicted_name}</p>
                                  <p>Probabilities:<br/> ${result.class_probabilities.map((prob, index) => 
                                    `<span>${index}: ${prob.toFixed(2)}</span>`).join(', ')}</p>`;


}
