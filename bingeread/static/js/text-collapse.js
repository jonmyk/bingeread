$(document).ready(function() {
    var showChar = 800;  
    var moretext = "(show more)";
    var lesstext = "show less ..";
    

    $('.book-description').each(function() {
        var content = description;

        //makes sure characters is above 800
        if(content.length > showChar) {
 
            var show_less_text = content.substr(0, showChar);
            var show_more_text = content.substr(showChar, content.length - showChar);
            console.log(show_more_text);
 
            var html_tag = show_less_text + '<span class="morellipses"> ...</span><span class="morecontent"><span class="text">' + show_more_text + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
            $(this).html(html_tag);
            $( ".text" ).toggle();
            
        }
    });
 
    $(".morelink").click(function(){
        if($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
            $( ".morellipses" ).toggle();
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
            $( ".morellipses" ).toggle();

        }
        $(this).prev().toggle();
        return false;
    });
});