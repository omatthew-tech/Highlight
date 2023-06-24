document.addEventListener('DOMContentLoaded', (event) => {
    var rows = Array.from(document.querySelectorAll(".row"));

    function shuffle(array) {
        var currentIndex = array.length, temporaryValue, randomIndex;

        while (0 !== currentIndex) {
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    }

    rows = shuffle(rows);

    function highlightRow(index) {
        var row = rows[index];
        row.classList.add("highlight");

        // Check if there is another row to highlight
        if (index < rows.length - 1) {
            setTimeout(function() {
                highlightRow(index + 1);
            }, 2000); // Wait for the current row's animation to finish before starting the next one
        }
    }

    highlightRow(0); // Start highlighting from the first row of the shuffled array
});











