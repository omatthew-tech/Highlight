document.addEventListener('DOMContentLoaded', (event) => {
    var rows = Array.from(document.querySelectorAll(".row"));
    var unhighlightedRows = Array.from(Array(rows.length).keys());

    var lastDirectionRight = false;  // Track the last direction used

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

    function highlightRow() {
        if (unhighlightedRows.length === 0) {
            return;
        }

        // Pick a random index from unhighlightedRows
        var randomIndex = Math.floor(Math.random() * unhighlightedRows.length);
        var indexToHighlight = unhighlightedRows[randomIndex];

        // Remove the highlighted index from the array
        unhighlightedRows = unhighlightedRows.filter(index => index !== indexToHighlight);
        var row = rows[indexToHighlight];

        // Check if row is already highlighted
        if(row.classList.contains("sweep-right") || row.classList.contains("sweep-left")) {
            // If it's already highlighted, call highlightRow again to pick another row
            highlightRow();
        } else {
            // Add class based on the last direction used
            if (lastDirectionRight) {
                row.classList.add("sweep-left");
                row.classList.add("row-left");
            } else {
                row.classList.add("sweep-right");
                row.classList.add("row-right");
            }

            lastDirectionRight = !lastDirectionRight;  // Alternate the direction

            // Schedule next highlight
            if (unhighlightedRows.length > 0) {
                setTimeout(highlightRow, 2000);
            }
        }
    }

    highlightRow(); // Start highlighting from the first row of the shuffled array
});











    





















