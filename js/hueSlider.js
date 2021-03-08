$(document).ready(function() {

    // Create the hue slider
    $("#hueSlider").slider({
        range: true,
        min: 0,
        max: 360,
        values: [0, 360],

        // Using the slider updates the hue range input
        slide: function(event, ui) {
            $("#hueRange").val(ui.values[0] + " - " + ui.values[1]);
        }
    });

    // Initially fill the hue range input
    $("#hueRange").val($("#hueSlider").slider("values",0) + " - " + $("#hueSlider").slider("values",1));
});