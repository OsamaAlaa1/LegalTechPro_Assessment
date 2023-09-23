
document.addEventListener("DOMContentLoaded", function () {
    const chatOutputContract = document.getElementById("chat-output-contract");
    const chatOutputNegotiation = document.getElementById("chat-output-negotiation");
    const chatOutputSimulation = document.getElementById("chat-output-simulate");
    const chatOutputTune = document.getElementById("chat-output-tune");


    const userInputContract = document.getElementById("user-input-contract");
    const userInputNegotiation = document.getElementById("user-input-negotiation");
    const userInputSimulation = document.getElementById("user-input-simulate");
    const userInputTune = document.getElementById("user-input-tune");


    const sendButtonContract = document.getElementById("send-button-contract");
    const sendButtonNegotiation = document.getElementById("send-button-negotiation");
    const sendButtonSimulation = document.getElementById("send-button-simulate");
    const sendButtonTune = document.getElementById("send-button-tune");


    sendButtonContract.addEventListener("click", async () => {
        handleButtonClick("analyze_clause", userInputContract, chatOutputContract);
    });

    sendButtonNegotiation.addEventListener("click", async () => {
        handleButtonClick("assist", userInputNegotiation, chatOutputNegotiation);
    });

    sendButtonSimulation.addEventListener("click", async () => {
        handleButtonClick("simulate", userInputSimulation, chatOutputSimulation);
    });

    sendButtonTune.addEventListener("click", async () => {
        handleButtonClick("fine_tune", userInputTune, chatOutputTune);
    });

    async function handleButtonClick(functionName, userInput, chatOutput) {
        const userMessage = userInput.value;
        if (!userMessage.trim()) return;
    
        // Display the user's message
        appendMessage(chatOutput, "You", userMessage);
    
        try {
            // Send user message to the server for analysis
            const response = await fetch(`/${functionName}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `userMessage=${encodeURIComponent(userMessage)}`,
            });
    
            if (response.ok) {
                const data = await response.json();
                const aiResponse = data.response;
    
                // Display the AI's analysis
                appendMessage(chatOutput, "AI", aiResponse);
            } else {
                console.error('Server returned an error:', response.status);
                appendMessage(chatOutput, "AI", "An error occurred.");
            }
        } catch (error) {
            console.error('An error occurred while making the request:', error);
            appendMessage(chatOutput, "AI", "An error occurred.");
        }
    
        // Clear the user input
        userInput.value = "";
    }
    

    function appendMessage(chatOutput, sender, message) {
        const messageElement = document.createElement("div");
        messageElement.className = "message";
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatOutput.appendChild(messageElement);

        // Scroll to the bottom of the chat output
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }
});

function downloadFile(downloadURL, fileName) {
    // Send an AJAX request to trigger the file download
    var xhr = new XMLHttpRequest();
    xhr.open("GET", downloadURL, true);
    xhr.responseType = "blob";

    xhr.onload = function () {
        if (xhr.status === 200) {
            // Create a temporary anchor element to trigger the download
            var blob = new Blob([xhr.response], { type: "application/octet-stream" });
            var url = window.URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = url;
            a.download = fileName; // Set the desired filename
            a.style.display = "none";
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        }
    };

    xhr.send();
}

// function to upload file
function uploadFile(
    input,
    uploadTextElement,
    downloadButtonElement,
    uploadEndpoint
) {
    const fileInput = input;
    const uploadText = uploadTextElement;
    const downloadButton = downloadButtonElement;
    const chatbox = document.getElementById("chat-box-container");
    const finetunebuton = document.getElementById("fine-tune-button");


    const file = fileInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        // Show loading indicator and hide upload text
        uploadText.textContent = "loading...";

        fetch(uploadEndpoint, {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                if (response.ok) {
                    // Hide the loading indicator and display the success icon
                    uploadText.textContent = "Almost...";

                    // Show the buttons after a successful upload
                    downloadButton.style.opacity = "1";

                    console.log("File uploaded successfully!");
                } else {
                    console.error("File upload failed.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
            })
            .finally(() => {
                // Show the "Completed" text
                uploadText.textContent = "Completed";
                if(uploadEndpoint == '/upload_scenarios'){chatbox.style.opacity = "1";}
                if(uploadEndpoint == '/upload_tune_scenarios'){finetunebuton.style.opacity = "1";}
            });
    }
}


// JavaScript to update scenario prompt when difficulty is selected
const difficultySelect = document.getElementById('difficulty');
const chatOutput = document.getElementById('chat-output-simulate');

difficultySelect.addEventListener('change', function () {
    const selectedDifficulty = this.value;

    // Fetch the scenario prompt based on the selected difficulty
    fetch(`/get_scenario_prompt?difficulty=${selectedDifficulty}`)
        .then(response => response.json())
        .then(data => {
            // Update the chat output with the scenario prompt
            chatOutput.innerText = data.prompt;
        })
        .catch(error => {
            console.error('Error fetching scenario prompt:', error);
            chatOutput.innerText = 'Error fetching scenario prompt.';
        });
});

 // for Fine-Tune button 

document.addEventListener('DOMContentLoaded', function () {

    const FineTuneButton = document.getElementById('fine-tune-button');
    const buttonText = document.getElementById('fine-tune-text');



    FineTuneButton.addEventListener('click', function () {
        // Disable the button and show the loading indicator
        FineTuneButton.disabled = true;
        buttonText.textContent = 'Loading...';

        // Make an AJAX POST request to the Flask route
        fetch('/increment_tune', {
            method: 'POST',
        })

            .then(function () {
                // Hide loading and show success
                buttonText.textContent = 'Completed';
            })
            .catch(function (error) {
                console.error('Error:', error);
                // Handle error here if necessary
            })
            .finally(function () {
                // Re-enable the button after execution
                FineTuneButton.disabled = false;
            });
    });
});