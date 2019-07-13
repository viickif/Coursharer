$(document).ready(function(){
 
    $(function () {
        $("#rateYoRead").rateYo({
            rating: 3.2,
            readOnly: true
        });

        $("#rateYoWrite").rateYo({
            rating: 0
        });

        $("#saveRating").on('click', function() {
            console.log($("#rateYoWrite").rateYo("rating"));
            $.post( "/rate/1", {
                rating: $("#rateYoWrite").rateYo("rating")
            });
        });
    });
});