document.addEventListener('DOMContentLoaded', (event) => {
    var rows = Array.from(document.querySelectorAll(".row"));
    
    // Shuffle rows at the start
    for(let i = rows.length - 1; i > 0; i--){
        const j = Math.floor(Math.random() * i)
        const temp = rows[i]
        rows[i] = rows[j]
        rows[j] = temp
    }

    var lastDirectionRight = false;  // Track the last direction used

    function highlightRow() {
        if (rows.length === 0) {
            return;
        }

        // Pop a row from shuffled rows
        var row = rows.pop();

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
        if (rows.length > 0) {
            setTimeout(highlightRow, 2000);
        }
    }

    highlightRow(); // Start highlighting from the first row of the shuffled array
});













    





















