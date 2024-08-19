
var currentStation = "{{ station }}";

// Function to show the modal with a message
function showModal(message) {
    var myModal = document.getElementById('myModal');
    var modalText = document.getElementById('modalText');
    if (myModal && modalText) {
        modalText.innerHTML = message; // Update the modal text
        myModal.style.display = "block";
    }
}

// Function to close the modal and start the timer
function closeModal() {
    var myModal = document.getElementById('myModal');
    if (myModal) {
        myModal.style.display = "none";
        startCountdown(); // Start the timer after closing the modal
    }
}

// Initialize the countdown timer to 120 seconds
let countdown = 120;

// Function to start the countdown timer
function startCountdown() {
    const timerElement = document.getElementById('timer');

    const countdownInterval = setInterval(function() {
        // Update the timer display
        timerElement.textContent = countdown;

        // Decrease the countdown by one second
        countdown--;

        // If the countdown reaches zero, redirect to the fail page
        if (countdown < 0) {
            clearInterval(countdownInterval);
            window.location.href = "/wrong"; // Redirect to the fail page
        }
    }, 1000); // Update every second
}

// Set up close functionality
document.addEventListener('DOMContentLoaded', function() {
    var closeButton = document.getElementsByClassName("close")[0];
    var myModal = document.getElementById('myModal');

    if(closeButton && myModal) {
        // Close modal when the close button is clicked
        closeButton.onclick = function() {
            closeModal();
        };

        // Close modal when clicking outside of the modal content
        window.onclick = function(event) {
            if (event.target == myModal) {
                closeModal();
            }
        };
    }

    // Show the modal if the station is 's3'
    if (currentStation === 's3') {
        showModal(`However, the metro stops at s3 unexpectedly, and could not continue to the 
        direction of s14. <br>
        It is due to ongoing construction at s4, with no metros able to pass through.  <br>
        Please design your trip accordingly.
        <br><br>
        Note: you have a maximum of 2 minutes to decide your next action. 
        <br>If you don't act within this time, you'll miss the next metro, ensuring you will be late and fail the task. 
        <br>A timer will start upon closing this message.`);
    }

    let currentScore = parseInt("{{ score }}", 10); 

    // Check the score and show the modal if score <= 0
    if (currentScore <= 0) {
        showModal('Sorry, you have run out of time. You will be directed to the result page in 3 seconds.');
        setTimeout(function() {
            window.location.href = "/wrong"; // Redirect to the wrong.html page
        }, 3000); // 3000 milliseconds = 3 seconds
    }
    if (currentStation === 's5') {
        showModal('You have reached your destination! Now you can get out of the metro and finish the task.');
    }
});
