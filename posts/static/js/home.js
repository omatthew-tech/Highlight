window.onload = function() {
    var boxes = document.querySelectorAll(".box");

    setInterval(function() {
        // Reset the brightness for all boxes
        boxes.forEach(function(box) {
            box.style.filter = "";
        });

        var randomIndex = Math.floor(Math.random() * boxes.length);
        var box = boxes[randomIndex];
        box.style.filter = "brightness(1.0)";

        setTimeout(function() {
            box.style.filter = "";
        }, 500);
    }, 1000);
};

