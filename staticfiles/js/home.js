window.onload = function() {
    var boxes = document.querySelectorAll(".box");

    setInterval(function() {
        var randomIndex = Math.floor(Math.random() * boxes.length);
        var box = boxes[randomIndex];
        box.style.filter = "brightness(1.5)";

        setTimeout(function() {
            box.style.filter = "";
        }, 500);
    }, 1000);
}
