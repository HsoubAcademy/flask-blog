export let displayError = (event) => {
    let displayError = document.getElementById("card-element-errors");
    if (event.error) {
        displayError.textContent = event.error.message;
        document.querySelector(".classBtn").disabled = true;
    } else {
        displayError.textContent = '';
        document.querySelector(".classBtn").disabled = false;
    }
};

export let stripeElements = (publicKey) => {
    const stripe = Stripe(publicKey, { locale: 'ar' });
    document.querySelector(".classBtn").disabled = true;
    const elements = stripe.elements();
    let cardElement = elements.create("card");
    cardElement.mount("#stripeCard");
    cardElement.on("change", (event) => {
        displayError(event);
    });
    cardElement.on("focus", () => {
        let el = document.getElementById("stripeCard");
        el.classList.add("focused")
    });
    cardElement.on("blur", () => {
        let el = document.getElementById("stripeCard");
        el.classList.add("focused")
    });
    return { stripe, cardElement }
};

export let changeLoadingState = (isLoading) => {
    if (isLoading) {
        document.querySelector(".classBtn").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector(".classBtn").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
}

export let orderComplete = (redirect_url, args = "") => {
    document.querySelector(".classBtn").disabled = true;
    document.querySelector(".result-message").classList.remove("hidden");
    document.querySelector(".payment-form").classList.add("hidden");

    setTimeout(() => {
        window.location.href = redirect_url + args;
    }, 3000);
    changeLoadingState(false)
}