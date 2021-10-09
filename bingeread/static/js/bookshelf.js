
var cur_list;

$(document).ready(function(){
	// Loads the list window
	load_lists();
	
	// Toggle the list dropdown menu on button click
	$('body').on('click', '.list_svg', function(e){
		e.stopPropagation();
		$(this).siblings('.dropdown_content').toggle();
	});
	// Toggle the list entry dropdown menu on button click
	$('body').on('click', '.edit_book_button', function(e){
		e.stopPropagation();
		$(this).siblings('.dropdown_content').toggle();
	});
	// Closes the list dropdown menu on mouseleave
	$('body').on('mouseleave', '.list_dropdown', function(e) {
		e.stopPropagation();
		$(this).find('.dropdown_content').hide();
	})
	// Allow the user to create a new list
	$('.new-list').on('click', function(){
		var name = prompt('Please name your list');
		if (name == null || name == "") {
			console.log('User cancelled the prompt');
		} else {
			create_list(name);
		}
	});
	// Allow the user to filter the list entries
	$('#list_filter input').bind('keypress', function(e){
		if (e.keyCode == 13) {
			filter_list($(this).val());
		} 
	});
	$('#list_filter span').on('click', function(){
		filter_list($(this).siblings('input').val());
	});

	// List selector
	$('body').on('click', '.list_name_link', function(){
		$(this).parent().siblings('.list_name').removeClass('selected');
		$(this).parent().addClass('selected');
		
		var lid = $(this).parent().data('lid');
		cur_list=lid;
		get_entries(lid);
	});
});

// Filter book window based on text input
function filter_list(keywords){
	if (!cur_list) {
		console.log('Could not apply filter on list as no list is selected');
	} else {
		$.ajax({
			type:'GET',
			url:filter_url,
			dataType:'json',
			data:{id:cur_list, kwrd:keywords},
			success:function(response){
				displayBooks(JSON.parse(response));
			},
			error:function(xhr){
				console.log('Could not apply filter on list | ' + xhr.status + ' ' + xhr.statusText);
			}
		});
	}
}

// Dynamically loads the list window
function load_lists(){
	$.get(get_lists_url, function(response){
		var jsonData = JSON.parse(response);
		$('#bookshelf-list').empty();
		$.each(jsonData, function(i, obj){
			var html = list_html(obj);
			$('#bookshelf-list').append(html);
		});
	}, 'json');
}

// Creates and append new list to the list window
function create_list(name){
	$.ajax({
		type:'POST',
		url:create_list_url,
		dataType:'json',
		data:{
			name:name,
			csrfmiddlewaretoken:csrf_token,
		},
		success:function(response){
			var record = JSON.parse(response);
			var html = list_html(record);
			$('#bookshelf-list').append(html);
			console.log('List created successfully');
		},
		error:function(xhr){
			console.log('List was not created | ' + xhr.status + ' ' + xhr.statusText);
			if (xhr.status == 409) {
				alert('The name is already in use.')
			}
		}
	});
}

// Renames a list and refreshes the list window 
function rename_list(id){
	var name = prompt('Please enter a new name');
	if (name == null || name == '') {
		console.log('User cancelled the prompt');
	} else {
		$.ajax({
			type:'POST',
			url:rename_list_url,
			dataType:'json',
			data:{
				id:id, 
				name:name, 
				csrfmiddlewaretoken:csrf_token},
			success:function(response){
				console.log('List renamed successfully');
				load_lists();
			},
			error:function(xhr){
				console.log('List was not renamed | ' + xhr.status + ' ' + xhr.statusText);
				if (xhr.status == 400) {
					// Assumption: Status 400 is caused by a ValidationError on the 'name' field
					alert('The name is already in use.')
				}
			}
		});
	}
}

// Deletes the list and all its entries from the database
function delete_list(id){
	if (confirm('Are you sure you want to delete this list?')) {
		$.ajax({
			type:'POST',
			url:delete_list_url,
			dataType:'html',
			data:{
				id:id,
				csrfmiddlewaretoken:csrf_token,
			},
			success:function(response){
				console.log('List deleted successfully');
				load_lists(); // Refreshes the list window
			},
			error:function(xhr){
				console.log('List was not deleted | ' + xhr.status + ' ' + xhr.statusText);
			}
		});
	} else {
		console.log('User cancelled the prompt');
	}
}

// Dynamically loads the book window
function get_entries(id){
	$.ajax({
		type:'POST',
		url:get_books_url,
		dataType:'json',
		data:{
			id:id,
			csrfmiddlewaretoken:csrf_token,
		},
		success:function(response){
			var entries = JSON.parse(response);
			if (entries.length == 0) {
				$('#bookshelf-book').empty();
				$('#bookshelf-book').append(
					'<li id="empty_list">\
						<h2>Looks like this list is empty</2>\
						<h4><a href="'+home_page+'">Visit our home page to find some books to add</a></h4>\
					</li>'
				);	
			} else {
				displayBooks(entries);
			}
		},
		error:function(xhr){
			console.log('Could not load the list entires | ' + xhr.status + ' ' + xhr.statusText);
		}
	});
}

// Inserts all the entry templates
function displayBooks(List){
	$('#bookshelf-book').empty();
	$.each(List, function(i, book){
		var data = {book:JSON.stringify(book), csrfmiddlewaretoken:csrf_token};
		$.post(book_template_url, data, function(template){
			$('#bookshelf-book').append(template);
			// Fetching the rating-widget values
			var wrapper = $('#'+book.id+' .rating-container');
			updateRatingWidget(wrapper); // NOTE: Function found in 'rating-widget.js'
		}, 'html');
	});
}

// Removes book from current list 
function removeBook(id){
	if (confirm('Are you sure you want to remove this book?')) {
		$.ajax({
			type:'POST',
			url:remove_book_url,
			dataType:'html',
			data:{
				book_id:id,
				list_id:cur_list,
				csrfmiddlewaretoken:csrf_token,
			},
			success:function(response){
				console.log('List entry successfully removed');
				get_entries(cur_list);
			},
			error:function(xhr){
				console.log('List entry was not removed | ' + xhr.status + ' ' + xhr.statusText);
			}
		});
	} else {
		console.log('User cancelled the prompt');
	}
}

// The string is in its own function to keep the code clean 
function list_html(model){
	var html = '\
	<li class="list_name" data-lid="'+model.pk+'">\
		<span class="list_name_link">'+model.fields.name+'</span>\
		<div class="list_dropdown">\
			<img class="list_svg" src="'+edit_svg+'">\
			<div class="dropdown_content">\
				<span name="rename_option" onclick="rename_list('+model.pk+')">Rename</span>\
				<span name="delete_option" onclick="delete_list('+model.pk+')">Delete</span>\
			</div>\
		</div>\
	</li>';
	return html;
}
