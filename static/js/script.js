$(document).ready(function(){
    $('.collapsible').collapsible();
    $("select").material_select();
    $(".button-collapse").sideNav();
    $('.carousel.carousel-slider').carousel({fullWidth: true});
    setInterval(function() {
        $(".carousel").carousel("next");
    }, 2500);
  });

$('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year,
    today: 'Today',
    clear: 'Clear',
    close: 'Ok',
    closeOnSelect: false // Close upon selecting a date,
  });

  document.getElementById("matfix").addEventListener("click", function(e) {
	e.stopPropagation();
});