import {
    stripeElements, changeLoadingState, orderComplete
} from "./index.js";

const { data } = await axios('/public-key');
let { stripe, cardElement } = stripeElements(data.publicKey);

const button = document.querySelector('#subBtn');
button.addEventListener('click', async (e) => {
    e.preventDefault();
    const setupIntent = await axios.post('/create-setup-intent').then((response) => response.data.client_secret);
    changeLoadingState(true);
    stripe.confirmCardSetup(
        setupIntent, {
        payment_method: {
            card: cardElement,
        },
    }
    ).then(
        (result) => {
            if (result.error) {
                changeLoadingState(false);
                let errorElement = document.getElementById("card-element-errors");
                errorElement.textContent = result.error.message;
            } else {
                orderComplete('/account');
            }
        }
    )
})
