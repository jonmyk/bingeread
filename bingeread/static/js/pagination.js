const element = document.querySelector(".pagination ul");

FIRST_PAGE=1
LAST_PAGE=totalPages;

element.innerHTML = pagination(totalPages, curr_page);

function determine_prev_button (curr_page,totalPages){

    let prev_button = '';
    if (curr_page != 1){
        prev_button = `<li class="btn prev" onclick="pagination(${totalPages}, ${curr_page - 1})"><span><i class="fas fa-angle-left"></i> Prev</span></li>`;
    }
    return prev_button;
}

function determine_next_button (curr_page,totalPages){
    let next_button = '';
    if (curr_page < totalPages) { 
        next_button += `<li class="btn next" onclick="pagination(${totalPages}, ${curr_page + 1})"><span>Next <i class="fas fa-angle-right"></i></span></li>`;
    }
    return next_button;
}

function active_or_not(curr_page,page,totalPages){
    let button = '';
    if (page === curr_page){
        button = `<li class="numb ${"active"}"><span>${page}</span></li>`;
    }
    else{
        button = `<li class="numb" onclick="pagination(${totalPages}, ${page})"><span>${page}</span></li>`;
    }
    return button;
}

function set_number_buttons (curr_page){
    let number_buttons = '';
    let page=FIRST_PAGE;
    for (; page <= LAST_PAGE; page++){
        let button = active_or_not(curr_page,page,totalPages);
        number_buttons += button;
    }
    return number_buttons;
}

function determine_left_dots (curr_page){
    let left_dots = '';
    if(curr_page > 3 ){
        left_dots =  `<li class="dots"><span>...</span></li>`;
    }
    return left_dots;
}

function set_first_button (curr_page,totalPages){
    let first_button = '';
    if (curr_page === 1){
       first_button = `<li class="numb ${"active"}"><span>${1}</span></li>`;
    }
    else{
        first_button = `<li class="numb" onclick="pagination(${totalPages}, ${1})"><span>${1}</span></li>`;
    }
    return first_button;
}

function set_middle_buttons (curr_page,totalPages){
    let middle_buttons = '';
    let SECOND_PAGE = 2;
     
    if(curr_page == 1 || curr_page == 2 ){
        for( var page = SECOND_PAGE; page <= 4; page++){
            let button = active_or_not (curr_page,page,totalPages);
            middle_buttons += button;  
        }
    }
    else if (curr_page == totalPages || curr_page == totalPages-1){
        for(var page = totalPages-3; page < totalPages; page++){
            let button = active_or_not (curr_page,page,totalPages);
            middle_buttons += button;
        }
    }
    else{
        let left_button = `<li class="numb" onclick="pagination(${totalPages}, ${curr_page - 1})"><span>${curr_page - 1}</span></li>`;
        let current_button = `<li class="numb ${"active"}" onclick="pagination(${totalPages}, ${curr_page})"><span>${curr_page}</span></li>`;
        let right_button = `<li class="numb" onclick="pagination(totalPages, ${curr_page + 1})"><span>${curr_page + 1}</span></li>`;
        middle_buttons = left_button + current_button + right_button;
    }

    return middle_buttons;
}

function determine_right_dots (curr_page,totalPages){
    let right_dots = '';
    if(curr_page  <= totalPages-3 ){
        right_dots =  `<li class="dots"><span>...</span></li>`;
    }
    return right_dots;
}

function set_last_button (curr_page,totalPages){
    let last_button = '';

    if(curr_page === totalPages){
        last_button =  `<li class="numb ${"active"}"><span>${totalPages}</span></li>`;
    }
    else{
        last_button =  `<li class="numb" onclick="pagination(${totalPages}, ${totalPages})"><span>${totalPages}</span></li>`;
    }
    return last_button;

} 

function pagination (totalPages, curr_page){
    let liTag = '';

    if (totalPages < 6){
        let prev_button = determine_prev_button (curr_page);
        let number_buttons = set_number_buttons (curr_page);
        let next_button = determine_next_button (curr_page,totalPages);
        liTag = prev_button + number_buttons + next_button;
    }
    else{
        let prev_button = determine_prev_button(curr_page,totalPages);
        let first_button =  set_first_button(curr_page,totalPages);
        let left_dots = determine_left_dots(curr_page);
        let middle_buttons = set_middle_buttons(curr_page,totalPages);
        let right_dots = determine_right_dots(curr_page,totalPages);
        let last_button = set_last_button(curr_page,totalPages);
        let next_button = determine_next_button(curr_page,totalPages);
        liTag = prev_button + first_button + left_dots + middle_buttons + right_dots + last_button + next_button;
    }
    
    element.innerHTML = liTag; 
    return liTag;
}
