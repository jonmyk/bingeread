/*
This script needs the following variables:
    csrf_token
*/

$(window).on("load", function(){
    /* Inserts the values in all the rating-widgets on the page. 
     * NOTE: This doesn't do anything on the bookshelf page as a list has yet to be selected */
    $('.rating-container').each(function(i, obj){
        updateRatingWidget($(this));
    }); 
    
    // Toggle popup on button click
    $('body').on('click', '.rating-button', function() {
        // NOTE: This is a workaround since toggleClass didn't work on the bookshelf page for some reason
        var popup = $(this).siblings('.rating-overlay');
        if (popup.is(":visible")) {
            popup.hide();
        } else {
            popup.show();
        } 
    });
    // Hide popup on mouseleave
    $('body').on('mouseleave', '.user-score', function() {
        $(this).find('.rating-overlay').hide();
    });

    // Add user score when a star icon is clicked
    $('body').on('click', '.rating-overlay span', function() {
        $(this).siblings('.checked').removeClass('checked');
        $(this).addClass('checked');
        setUserScore($(this).closest('.rating-container'));
    });

    // Remove user score when the (X) icon is clicked
    $('body').on('click', '.rating-container .rating-overlay .remove', function() {
        removeUserScore($(this).closest('.rating-container'));
    });

});

function insertUserRating(wrapper, json){
    // Select the star based on the user score
    wrapper.find('.rating-overlay span.checked').removeClass('checked');
    if (json && json.score) {
        wrapper.find('.rating-overlay span').filter('[data-score="'+json.score+'"]').addClass('checked'); 
        wrapper.find('.rating-button').addClass('filled');
        wrapper.find('.user-score .output-field').html(json.score);
    }
    else {
        wrapper.find('.rating-button').removeClass('filled');
        wrapper.find('.user-score .output-field').html('Rate this');
    }
}

function insertCollectiveRatings(wrapper, json){
    // Insert the global rating (average and count)
    if (json.count > 0){
        wrapper.find('.avg-score').addClass('filled');
        wrapper.find('.score-count').addClass('filled');
        wrapper.find('.avg-score .output-field').html(json.avg.toFixed(1));
        wrapper.find('.score-count').html(json.count);
    } else {
        wrapper.find('.avg-score').removeClass('filled');
        wrapper.find('.score-count').removeClass('filled');
        wrapper.find('.avg-score .output-field').html((0).toFixed(1));
        wrapper.find('.score-count').html(0);
    }
}

function getCollectiveRatings(wrapper){
    // Fetches the global rating (average and count)
    $.ajax({
        type:'GET',
        url:'/score/global',
        dataType: 'json',
        data:{id: wrapper.data('book-id')},
        success:function(json){
            insertCollectiveRatings(wrapper, json);
        },
        error:function(){
            alert("Something went wrong");
        }
    });
}


function getUserRating(wrapper){
    // Fetches the user rating
    $.ajax({
        type:'GET',
        url:'/score/user',
        dataType: 'json',
        data:{id: wrapper.data('book-id')},
        success:function(json){
            insertUserRating(wrapper, json);
        },
        error:function(xhr){
            console.log('User score chould not be retrieved | ' + xhr.status + ' ' + xhr.statusText);
            insertUserRating(wrapper, {});
        }
    });
}


function updateRatingWidget(wrapper){
    // Updates the values displayed on the rating widget
    getCollectiveRatings(wrapper);
    getUserRating(wrapper);
}


function setUserScore(wrapper){
    $.ajax({
        type:'POST',
        url:'/score/add',
        dataType:'html',
        data:{
            id: wrapper.data('book-id'),
            score: wrapper.find('.rating-overlay span.checked').data('score'),
            csrfmiddlewaretoken: csrf_token,
        },
        success:function(){
            console.log("User score successfully added");
            updateRatingWidget(wrapper);
        },
        error:function(xhr){
            console.log('User score was not added | ' + xhr.status + ' ' + xhr.statusText);
        }
    });
}

function removeUserScore(wrapper){
    $.ajax({
        type:'POST', 
        url:'/score/remove', 
        dataType:'html',
        data:{
            id:wrapper.data('book-id'), 
            csrfmiddlewaretoken:csrf_token
        },
        success:function(){
            console.log('User score successfully removed');
            updateRatingWidget(wrapper);
        }, 
        error:function(xhr){
            console.log('User score was not removed | ' + xhr.status + ' ' + xhr.statusText);
        }
    });
}