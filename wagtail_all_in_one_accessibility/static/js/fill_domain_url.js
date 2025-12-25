// fill_domain_url.js
// Automatically fills the 'domain_url' field with the current page's protocol + hostname
document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector("input[name='domain_url']");

    if (input) {
        const protocol = window.location.protocol;
        const hostname = window.location.hostname;

        const domain = protocol + "//" + hostname;

        // Always update, even if already filled
        input.value = domain;
    }
});



