
document.addEventListener("DOMContentLoaded", function () {
const urlParams = new URLSearchParams(window.location.search);
const odysseyCode = urlParams.get("id");

// Detect if running locally or on GitHub Pages
function getBaseURL() {
    const hostname = window.location.hostname;
    
    // If on localhost or 127.0.0.1, use local URL
    if (hostname === 'localhost' || hostname === '127.0.0.1' || hostname.startsWith('192.168.')) {
        return window.location.protocol + '//' + window.location.host;
    }
    
    // Otherwise use GitHub Pages URL
    return 'https://cbitosc.github.io/verify25';
}

// Get the event name from current path
function getEventName() {
    const path = window.location.pathname;
    const match = path.match(/\/(hfest[A-Za-z]+)\//);
    return match ? match[1] : 'hfestP';
}

fetch("data.json")
    .then((response) => response.json())
    .then((jsonData) => {
        const matchingEntry = jsonData.find((entry) => entry.code === odysseyCode);

        if (matchingEntry) {
            const generalHeader = document.getElementById("general-header");
            generalHeader.classList.add("hidden");

            const nameElement = document.getElementById("name-element");
            nameElement.textContent = `${matchingEntry.holder}`;

            const headerNameElement = document.getElementById("header-name-element");
            headerNameElement.textContent = `${matchingEntry.holder}`;

            const certHeader = document.getElementById("cert-header");
            const certificate = document.getElementById("certificate");

            certHeader.classList.remove("hidden");
            certificate.classList.remove("hidden");

            const qrContainer = document.getElementById("qr-container");

            // Generate QR code with appropriate URL
            const baseURL = getBaseURL();
            const eventName = getEventName();
            const qrURL = baseURL + '/' + eventName + '/?id=' + matchingEntry.code;

            const qr = new QRCode(qrContainer, {
                text: qrURL,
                width: 384,
                height: 384,
                typeNumber: 8,
                correctLevel: QRCode.CorrectLevel.H,
                colorDark: "#000000",
                colorLight: "#ffffff"
            });
            
            console.log('Generated QR for:', qrURL);
        } else {
            console.error("No matching entry found for the provided code.");
        }
    })
    .catch((error) => console.error("Error loading JSON:", error));
});
