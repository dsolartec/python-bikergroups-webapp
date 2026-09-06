function removePreviousInputError(formName, inputName) {
    const previousInputErrorEl = document.querySelector(`#${formName}-form #${formName}-${inputName} .input__error`);
    if (!previousInputErrorEl) return;
    
    previousInputErrorEl.remove();
}

function showErrorInInput(formName, inputName, errorMessage) {
    if (!errorMessage) return;

    const signInPhoneMainInputEl = document.querySelector(`#${formName}-form #${formName}-${inputName}`);
    if (!signInPhoneMainInputEl) return;

    const spanInputErrorEl = document.createElement("span");
    spanInputErrorEl.classList.add("input__error");
    spanInputErrorEl.append(errorMessage);

    signInPhoneMainInputEl.append(spanInputErrorEl);
}

// Sign in form

const signInFormEl = document.querySelector("#signin-form")
signInFormEl.addEventListener("submit", (e) => {
    const form = new FormData(signInFormEl);

    removePreviousInputError("signin", "phone");
    removePreviousInputError("signin", "password");

    let hasError = false;

    if (!form.get("phone")) {
        showErrorInInput("signin", "phone", "El número de teléfono es obligatorio")
        hasError = true;
    }

    if (!form.get("password")) {
        showErrorInInput("signin", "password", "La contraseña es obligatori")
        hasError = true;
    }

    if (hasError) e.preventDefault();
});

// Sign up form

function validateDisplayName(value) {
    if (!value) return "El nombre visible es obligatorio";
    if (value.length < 4) return "El nombre visible debe tener más de 4 caracteres";
    if (value.length > 100) return "El nombre visible debe tener menos de 100 caracteres";

    return null;
}

function validatePhone(value) {
    if (!value) return "El número de teléfono es obligatorio";
    if (value.length != 10 || !value.startsWith("3")) return "El número de teléfono no es válido";

    return null;
}

const signUpPasswordLengthStatusEl = document.querySelector("#signup-form [data-signup-password-length]");
const signUpPasswordUppersLengthStatusEl = document.querySelector("#signup-form [data-signup-password-uppers-length]");
const signUpPasswordLowersLengthStatusEl = document.querySelector("#signup-form [data-signup-password-lowers-length]");
const signUpPasswordNumbersLengthStatusEl = document.querySelector("#signup-form [data-signup-password-numbers-length]");

function validatePasswordDetailsStatus(value) {
    if (value.length < 8) signUpPasswordLengthStatusEl.classList.remove("done");
    else signUpPasswordLengthStatusEl.classList.add("done");

    if ((value.match(/[A-Z]/g) || []).length == 0) signUpPasswordUppersLengthStatusEl.classList.remove("done");
    else signUpPasswordUppersLengthStatusEl.classList.add("done");

    if ((value.match(/[a-z]/g) || []).length == 0) signUpPasswordLowersLengthStatusEl.classList.remove("done");
    else signUpPasswordLowersLengthStatusEl.classList.add("done");

    if ((value.match(/\d/g) || []).length == 0) signUpPasswordNumbersLengthStatusEl.classList.remove("done");
    else signUpPasswordNumbersLengthStatusEl.classList.add("done");
}

const signUpPasswordInputEl = document.querySelector("#signup-form #signup-password input");
if (signUpPasswordInputEl.value) validatePasswordDetailsStatus(signUpPasswordInputEl.value);

signUpPasswordInputEl.addEventListener("input", (e) => validatePasswordDetailsStatus(e.target.value));

function validatePassword(value) {
    if (!value) return "La contraseña es obligatoria";
    if (value.length < 8) return "La contraseña debe tener mínimo 8 caracteres";
    if (value.length > 80) return "La contraseña solo puede tener máximo 80 caracteres";
    if ((value.match(/[A-Z]/g) || []).length == 0) return "La contraseña debe tener mínimo una letra mayúscula";
    if ((value.match(/[a-z]/g) || []).length == 0) return "La contraseña debe tener mínimo una letra minúscula";
    if ((value.match(/\d/g) || []).length == 0) return "La contraseña debe tener mínimo un número";

    return null;
}

function validateConfirmPassword(value) {
    if (!value) return "Debes confirmar la contraseña";
    if (signUpPasswordInputEl.value != value) return "Las contraseñas no coinciden";

    return null;
}

const validateCallers = {
    "display_name": validateDisplayName,
    "phone": validatePhone,
    "password": validatePassword,
    "confirm_password": validateConfirmPassword,
};

const signUpFormInputs = document.querySelectorAll("#signup-form input");

document.getElementById("signup-form").addEventListener("submit", (e) => {
    let hasError = false;

    signUpFormInputs.forEach((inputEl) => {
        const inputName = inputEl.getAttribute("name");
        if (!inputName) return;

        removePreviousInputError("signup", inputName);

        const value = inputEl.value;

        const errorMessage = validateCallers[inputName](value);
        if (errorMessage) {
            showErrorInInput("signup", inputName, errorMessage);
            hasError = true;
        }
    });

    if (hasError) e.preventDefault();
});
