document.querySelectorAll("[data-toggle-main-navigation]").forEach((btnEl) => {
    btnEl.addEventListener('click', () => {
        const mainNavigationEl = document.querySelector(".main-navigation__nav");
        if (!mainNavigationEl) return;

        mainNavigationEl.classList.toggle("show");
    });
});

document.querySelectorAll("[data-toggle-password-input]").forEach((btnEl) => {
    btnEl.addEventListener('click', () => {
        const inputName = btnEl.getAttribute("data-input-name");
        if (!inputName) return;

        const inputEl = document.querySelector(`#${inputName} input`);
        if (!inputEl) return;

        const iconEl = btnEl.querySelector(".icon");
        if (!iconEl) return;

        if (inputEl.type == "password") {
            inputEl.type = "text";
            iconEl.classList.remove("icon--eye");
            iconEl.classList.add("icon--eye-off");
        } else {
            inputEl.type = "password";
            iconEl.classList.remove("icon--eye-off");
            iconEl.classList.add("icon--eye");
        }
    });
});
