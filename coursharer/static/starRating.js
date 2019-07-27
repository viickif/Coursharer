$(document).ready(function(){
 
    $(function () {
        $.get( "/rating/get/1", function( data ) {
            currRating = $.parseJSON(data).rating;

            console.log($.parseJSON(data).rating)
            $("#rateYoRead").rateYo({
                rating: currRating,
                spacing: "10px",
                ratedFill: "#fdd962",
            });

            $("#rateYoRead").on('click', function() {
                newRating = $(this).rateYo("rating");
                $("#rateYoWrite").rateYo({
                    rating: newRating,
                    spacing: "10px",
                    ratedFill: "#fdd962",
                });
            });

            $("#saveRating").on('click', function() {
                console.log($("#rateYoWrite").rateYo("rating"));
                $.post( "/rating/update/1", {
                    rating: $("#rateYoWrite").rateYo("rating")
                });
            });
        });
    });
});