let stripe = (async () => {
    const response = await fetch('/pub_key/', {method: 'GET'})
    let pub = await response.json()
    let pub_key = await pub.pub_key
    return await Stripe(pub_key);
})();

stripe = stripe.then(stripe => {return stripe});


function format_response(response) {
    return response.json();
};


async function redirection_event(item_id) {
    stripe = await stripe.then(stripe => {return stripe});
    await fetch(`/buy/${item_id}`, {method: 'GET'}).then(response => format_response(response)).then(session => stripe.redirectToCheckout({ sessionId: session.id }));
};


async function order_redirection(order_id) {
    stripe = await stripe.then(stripe => {return stripe});
    await fetch(`/order/buy/${order_id}`, {method: 'GET'}).then(response => format_response(response)).then(session => stripe.redirectToCheckout({ sessionId: session.id }));
};


async function get_pub_key() {
    const pub_key = await fetch('/pub_key/', {method: 'GET'}).then(response => format_response(response));
    return await pub_key.pub_key;
};

function get_stripe() {
    const stripe = Stripe(pub_key);
    return stripe;
};


async function get_secret_for_intent(order_id) {
    try {
        stripe = await stripe.then(stripe => {return stripe});
    } catch {};

    const response = await fetch(`/intent/${order_id}`);
    const clientSecret = await response.json();
    await console.log(clientSecret)
    const options = {
        clientSecret: clientSecret.clientSecret
    };

    // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 2
    const elements = stripe.elements(options);

    // Create and mount the Payment Element
    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');
    document.getElementById("get-intent").remove();
    let submit_button = await document.createElement("button");
    submit_button.id = "submit";
    submit_button.innerHTML = "Submit";
    document.getElementById("payment-form").appendChild(submit_button);

    document.getElementById("payment-form").addEventListener('submit', async (event) => {
        event.preventDefault();

        const {error} = await stripe.confirmPayment({
        //`Elements` instance that was used to create the Payment Element
        elements,
        confirmParams: {
          return_url: return_url,
        },
        });

        if (error) {
        // This point will only be reached if there is an immediate error when
        // confirming the payment. Show error to your customer (for example, payment
        // details incomplete)
        const messageContainer = document.querySelector('#error-message');
        messageContainer.textContent = error.message;
        } else {
        // Your customer will be redirected to your `return_url`. For some payment
        // methods like iDEAL, your customer will be redirected to an intermediate
        // site first to authorize the payment, then redirected to the `return_url`.
        }
        });
};


async function set_status(order_id) {
    try {
        stripe = await stripe.then(stripe => {return stripe});
    } catch {};
    const clientSecret = new URLSearchParams(window.location.search).get(
      'payment_intent_client_secret'
    );

    // Retrieve the PaymentIntent
    stripe.retrievePaymentIntent(clientSecret).then(({paymentIntent}) => {
        const message = document.querySelector('#message');

        // Inspect the PaymentIntent `status` to indicate the status of the payment
        // to your customer.
        //
        // Some payment methods will [immediately succeed or fail][0] upon
        // confirmation, while others will first enter a `processing` state.
        //
        // [0]: https://stripe.com/docs/payments/payment-methods#payment-notification
        switch (paymentIntent.status) {
        case 'succeeded':
          message.innerText = 'Success! Payment received.';
          fetch(`/intent/${order_id}/status/success`, {method: 'GET'})
          break;

        case 'processing':
          message.innerText = "Payment processing. We'll update you when payment is received.";
          break;

        case 'requires_payment_method':
          message.innerText = 'Payment failed. Please try another payment method.';
          // Redirect your user back to your payment page to attempt collecting
          // payment again
          break;

        default:
          message.innerText = 'Something went wrong.';
          break;
        }
        });
};


