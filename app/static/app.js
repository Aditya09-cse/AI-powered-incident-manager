document.addEventListener("DOMContentLoaded", () => {

    const chatMessages =
        document.getElementById("chatMessages");

    const assistantInput =
        document.getElementById("assistantInput");

    const chatForm =
        document.getElementById("chatForm");


    // Scroll AI chat to latest message
    if (chatMessages) {
        chatMessages.scrollTop =
            chatMessages.scrollHeight;
    }


    // Quick prompt buttons
    document
        .querySelectorAll("[data-prompt]")
        .forEach((button) => {

            button.addEventListener("click", () => {

                if (!assistantInput) {
                    return;
                }

                assistantInput.value =
                    button.dataset.prompt;

                assistantInput.focus();

            });

        });


    // Enter = Send
    // Shift + Enter = New line
    if (assistantInput && chatForm) {

        assistantInput.addEventListener(
            "keydown",
            (event) => {

                if (
                    event.key === "Enter" &&
                    !event.shiftKey
                ) {

                    event.preventDefault();

                    chatForm.requestSubmit();
                }

            }
        );
    }


    // Button loading state
    document
        .querySelectorAll("form")
        .forEach((form) => {

            form.addEventListener("submit", () => {

                const button =
                    form.querySelector("[data-loading]");

                if (!button) {
                    return;
                }

                button.disabled = true;

                button.textContent =
                    button.dataset.loading;

            });

        });


    // Auto resize AI textarea
    if (assistantInput) {

        assistantInput.addEventListener(
            "input",
            () => {

                assistantInput.style.height = "auto";

                assistantInput.style.height =
                    Math.min(
                        assistantInput.scrollHeight,
                        180
                    ) + "px";

            }
        );
    }


    // Mobile sidebar
    const mobileMenu =
        document.getElementById("mobileMenu");

    const sidebar =
        document.getElementById("sidebar");

    if (mobileMenu && sidebar) {

        mobileMenu.addEventListener("click", () => {

            sidebar.classList.toggle(
                "mobile-open"
            );

        });
    }

});