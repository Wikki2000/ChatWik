$(document).ready(function () {
  const user_name = $("#storage").data('user_name');
  const welcomeText = `Welcome ${user_name}!`
  typeLetter(welcomeText, 0);
});


/**
 * Display a welcome text by typing word one by one.
 *
 * @param {string} text - The text to animate.
 * @param {integer} i - Count the number of string.
 */
function typeLetter(text, i) {
    if (i < text.length) {
        $("#welcome").append(text[i]);
        setTimeout(function () {
            typeLetter(text, i + 1);
        }, 200);  // Delay in milliseconds
    }
}
