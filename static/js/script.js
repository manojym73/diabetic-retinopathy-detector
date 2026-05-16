// =========================================
// IMAGE PREVIEW
// =========================================

const imageInput =
    document.getElementById("imageInput");

const previewImage =
    document.getElementById("previewImage");

if(imageInput){

    imageInput.addEventListener(
        "change",
        function(){

            const file = this.files[0];

            if(file){

                const reader =
                    new FileReader();

                reader.onload = function(e){

                    previewImage.src =
                        e.target.result;

                    previewImage.classList.remove(
                        "d-none"
                    );

                };

                reader.readAsDataURL(file);

            }

        }
    );

}

// =========================================
// DRAG DROP
// =========================================

const dropArea =
    document.getElementById("dropArea");

if(dropArea){

    ["dragenter","dragover"].forEach(
        eventName => {

            dropArea.addEventListener(
                eventName,
                e => {

                    e.preventDefault();

                    dropArea.classList.add(
                        "drag-active"
                    );

                }
            );

        }
    );

    ["dragleave","drop"].forEach(
        eventName => {

            dropArea.addEventListener(
                eventName,
                e => {

                    e.preventDefault();

                    dropArea.classList.remove(
                        "drag-active"
                    );

                }
            );

        }
    );

    dropArea.addEventListener(
        "drop",
        e => {

            const files =
                e.dataTransfer.files;

            imageInput.files = files;

            imageInput.dispatchEvent(
                new Event("change")
            );

        }
    );

}

// =========================================
// LOADER
// =========================================

const uploadForm =
    document.getElementById("uploadForm");

if(uploadForm){

    uploadForm.addEventListener(
        "submit",
        () => {

            document.getElementById(
                "loader"
            ).classList.remove(
                "d-none"
            );

        }
    );

}

// =========================================
// CHATBOT
// =========================================

async function sendMessage(){

    const input =
        document.getElementById(
            "chatInput"
        );

    const messages =
        document.getElementById(
            "chatMessages"
        );

    const text =
        input.value.trim();

    if(text === "") return;

    // USER MESSAGE

    const userDiv =
        document.createElement("div");

    userDiv.className =
        "user-message";

    userDiv.innerHTML = text;

    messages.appendChild(userDiv);

    input.value = "";

    // BOT TYPING

    const typingDiv =
        document.createElement("div");

    typingDiv.className =
        "bot-message";

    typingDiv.innerHTML =
        "Typing...";

    messages.appendChild(typingDiv);

    messages.scrollTop =
        messages.scrollHeight;

    // FETCH API

    try{

        const response =
            await fetch("/chat", {

                method:"POST",

                headers:{
                    "Content-Type":
                    "application/json"
                },

                body:JSON.stringify({

                    message:text

                })

            });

        const data =
            await response.json();

        typingDiv.innerHTML =
            data.response;

    }

    catch(error){

        typingDiv.innerHTML =
            "Connection failed.";

    }

    messages.scrollTop =
        messages.scrollHeight;

}

// =========================================
// ENTER KEY
// =========================================

const chatInput =
    document.getElementById(
        "chatInput"
    );

if(chatInput){

    chatInput.addEventListener(
        "keypress",
        function(e){

            if(e.key === "Enter"){

                sendMessage();

            }

        }
    );

}