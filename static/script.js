document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");

    const button = document.getElementById("scan-btn");

    const loading = document.getElementById("loading");

    form.addEventListener("submit", function () {

        button.disabled = true;

        button.innerText = "Scanning...";

        loading.style.display = "block";

    });

});

document.addEventListener("DOMContentLoaded", function () {

    const error = document.querySelector(".error-message");

    if (error) {

        setTimeout(function () {

            error.style.transition = "opacity 0.5s";

            error.style.opacity = "0";

            setTimeout(function () {

                error.remove();

            }, 500);

        }, 3000);

    }

});