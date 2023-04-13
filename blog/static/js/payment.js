import {
    stripeElements, changeLoadingState, orderComplete
} from "./index.js";

const { data } = await axios('/public-key');
let { stripe, cardElement } = stripeElements(data.publicKey);

const button = document.querySelector('#subBtn');
button.addEventListener('click', async (e) => {
    e.preventDefault();
    const emailInput = document.getElementById('user_email');
    changeLoadingState(true);
    stripe.confirmCardPayment(
        button.dataset.cls, {
        payment_method: {
            card: cardElement,
            billing_details: {
                email: emailInput.value,
            },
        },
    }
    ).then(
        (result) => {
            if (result.error) {
                changeLoadingState(false);
                let errorElement = document.getElementById("card-element-errors");
                errorElement.textContent = result.error.message;
            } else {
                orderComplete('/subscription-success?paymentIntentStatus=', result.paymentIntent.status);
            }
        }
    )
})
