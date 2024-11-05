'use strict';


// Full message from the server
let answerElement = document.getElementById("answer");
let originalAnswer = answerElement.textContent;
let currentLength = 0; // Start with no characters shown
let interval = 3; // Number of characters to reveal at a time

function revealMessage() {
    // Increase the length of displayed message by `interval`
    currentLength += interval;

    // Display a slice of the message
    answerElement.textContent = originalAnswer.slice(0, currentLength);

    //alert("hello");

    if (answerElement.style.visibility === "hidden") {
      answerElement.style.visibility = "visible";
    }

    // Stop revealing when the full message is shown
    if (currentLength >= answerElement.length) {
        clearInterval(revealInterval);
    }
}

// Reveal message every 500 milliseconds (0.5 seconds)
//let revealInterval = setInterval(revealMessage, 50);

document.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    // Do something when Enter is pressed
    setInterval(revealMessage, 50);
  } 
});