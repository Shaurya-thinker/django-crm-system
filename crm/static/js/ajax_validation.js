const saveBtn =
    document.getElementById(
        'save-btn'
    );

function validateField(
    fieldId,
    validationType,
    messageId,
    existsMessage,
    availableMessage
){

    const input =
        document.getElementById(
            fieldId
        );

    const message =
        document.getElementById(
            messageId
        );

    if(!input){
        return;
    }

    let timer;

    input.addEventListener(
        'input',
        function(){

            clearTimeout(timer);

            timer = setTimeout(
                function(){

                    const value =
                        input.value.trim();

                    const minLength =
                        validationType === 'phone'
                        ? 10
                        : 3;

                    if(value.length < minLength){

                        message.innerHTML = '';

                        saveBtn.disabled = false;

                        return;
                    }
                    message.innerHTML =
                        '<span class="text-secondary">Checking...</span>';

                    fetch(
                        `/ajax/validate/?type=${validationType}&value=${encodeURIComponent(value)}`
                    )

                    .then(
                        response => response.json()
                    )

                    .then(
                        data => {

                            if(data.exists){

                                message.innerHTML =
                                    `<span class="text-danger">❌ ${existsMessage}</span>`;

                                saveBtn.disabled = true;

                            }
                            else{

                                message.innerHTML =
                                    `<span class="text-success">✅ ${availableMessage}</span>`;

                                saveBtn.disabled = false;

                            }

                        });

                },
                500
            );

        }
    );

}