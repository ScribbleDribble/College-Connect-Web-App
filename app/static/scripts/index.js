$(document).ready(function(){

    $('div.glyphicon.glyphicon-remove').click(function() {
        $(this.parentElement).hide();
        console.log("here")
    });

});