$(function () {
	//var AJAX_URL = "http://13.93.107.254/webservice"
	var AJAX_URL = "/webservice"
	var g_dishes = null;
	var g_categories = null;
	var g_spinner = null;
	
	function id_from_li(li, elem, id_prefix) {
		var li_classes = li.attr(elem).split(' ');
		var ret = "";
		$.each(li_classes, function( index, value ) {
			split_str = value.split("-");
			if ((split_str.length == 2) && (split_str[0] == id_prefix)) {
				ret = split_str[1];
				return ret;
			}
		});
		return ret;
	}
	
	function spin() {
		var target = document.getElementsByTagName("body")[0];
		g_spinner = new Spinner({});
		g_spinner.spin(target);
	}
	
	function unspin() {
		if (g_spinner != null) {
			g_spinner.stop();
		}
		g_spinner = null;
	}
	
	function category_id_from_li(li) {
		return id_from_li(li, "class", "category");
	}
	
	function dish_id_from_li(li) {
		return id_from_li(li, "id", "dish");
	}
	
	function log(msg, level) {
		$('.bottom-right').notify({
			message: { text: msg },
			type: level
		}).show();
	}
	
	function warning(msg) {
		log(msg, "error");
	}
	
	function success(msg) {
		log(msg, "success");
	}
	
	function update_callbacks() {
		$(".connectedSortable").sortable({
	        connectWith: ".connectedSortable",
	        receive: function(event, ui)  {
				var category_name = $(this).parent().parent().parent().attr("id");
				var li = $(ui.item[0]);
				if (category_name == "chosen-dishes") {
					if (!set_dish_today(li, true)) {
						ui.sender.sortable("cancel");
					}
					return;
				}
				orig_category_name = "category-" + category_id_from_li(li);
				if (orig_category_name != category_name) {
					warning('לא ניתן להחזיר ארוחה מהסוג הלא נכון');
					ui.sender.sortable("cancel");
					return;
				}
				if (!set_dish_today(li, false)) {
					ui.sender.sortable("cancel");
				}
				// remove dish today
				return true;
	        }
	    });
	    
	    $("#dishes-to-choose ul.nav").on("click", "li", function() {
		    if (!set_dish_today($(this), true)) {
			    // Don't add if we failed
			    return;
		    }
		    $("#chosen-dishes ul").append($(this));
	    });
	    
	    $("#chosen-dishes ul.nav").on("click", "li", function() {
		    //orig_category_name = category_name_from_li($(this));
		    //$("#" + orig_category_name + " ul").append($(this));
		    
		    dish_id = dish_id_from_li($(this));
		    dish = null;
		    
		    $.each(g_dishes, function( index, dish_iter ) {
			    if (dish_iter.id == dish_id) {
				    dish = dish_iter;
			    }
			});
			
			if (dish == null) {
				alert("No way");
			}
		    
		    $('#editModal .modal-title').html("עריכה - " + dish.name);
		    $('#editModal #dishNameEdit').attr('value', dish.name);
		    $('#editModal #dishDescriptionEdit').attr('value', dish.short_desc);
		    $('#editModal #dishRecipeEdit').html(dish.recipe);
		    $('#editModal #dishUpdateID').attr('value', dish_id);
		    
		    $('#editModal').modal('show');
	    });
	}
	
	function get_day() {
		return $("#datetimepicker").val();
	}
	
	function set_dish_today(li, should_add) {
		spin();
		
		var dish_id = dish_id_from_li(li);
		
		url_suffix = "unset_day";
		if (should_add) {
			url_suffix = "set_day";
		}
		
		var ret = false;
		$.ajax({
			type: "POST",
			url: AJAX_URL + "/restaurants/1/dishes/" + dish_id + "/" + url_suffix,
			data: JSON.stringify({"day": get_day()}),
			dataType: 'json',
			success: function(data) { 
				if (data.result == "True") {
					success("התפריט עודכן בהצלחה");
					ret = true;
				} else {
					warning("שגיאה בעדכון התפריט. רענן ונסה שוב");
					ret = false;
				}
				unspin();
			},
			failure: function(errMsg) {
			    warning(errMsg);
			    ui.sender.sortable("cancel");
			    unspin();
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
			    warning(errorThrown);
			    ui.sender.sortable("cancel");
			    unspin();
			},
			async: false
		});
		return ret;
	}
    
    
    $( document ).ready(function() {
	    spin();
	    
	    $.ajax({
		    type: "GET",
		    url: AJAX_URL + "/restaurants/1/categories/json",
		    success: function(data) {
			    g_categories = data.categories;
		    },
		    failure: function(errMsg) {
			    warning(errMsg);
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
			    warning(errorThrown);
			}
	    }) // $.ajax
	    
	    var today_dishes = null;
	    
	    $("#editModal button#dishUpdate").click(function() {
		    dish_id = $('#editModal #dishUpdateID').attr('value');
		    $('#editModal #dishUpdateID').attr('value', '');
		    
		    if (dish_id != "") {
			    $.ajax({
					type: "POST",
					url: AJAX_URL + "/restaurants/1/dishes/" + dish_id + "/update",
					data: JSON.stringify({
						"name": $('#editModal #dishNameEdit').val(),
						"recipe": $('#editModal #dishRecipeEdit').val(),
						"short_desc": $('#editModal #dishDescriptionEdit').val(),
						"day": get_day()
					}),
					dataType: 'json',
					success: function(data) { 
						if (data.result == "True") {
							success("מתכון המנה עודכן בהצלחה");
						} else {
							warning("שגיאה בעדכון מתכון המנה. רענן ונסה שוב");
						}
						$(this).button('reset');
						$('#editModal').modal('hide');
					},
					failure: function(errMsg) {
					    warning(errMsg);
					    $(this).button('reset');
					},
					error: function(XMLHttpRequest, textStatus, errorThrown) {
					    warning(errorThrown);
					    $(this).button('reset');
					}
				});
				$(this).button('loading');
			} else {
				warning("Not possible");
			}
		}); // dishUpdate.click
	    
	    $("#editModal button#dishUpdateRecipeToday").click(function() {
		    dish_id = $('#editModal #dishUpdateID').attr('value');
		    $('#editModal #dishUpdateID').attr('value', '');
		    
		    if (dish_id != "") {
			    $.ajax({
					type: "POST",
					url: AJAX_URL + "/restaurants/1/dishes/" + dish_id + "/set_extra_recipe",
					data: JSON.stringify({
						"extra_recipe": $('#editModal #dishRecipeEdit').val(),
						"day": get_day()
					}),
					dataType: 'json',
					success: function(data) { 
						if (data.result == "True") {
							success("מתכון המנה עודכן בהצלחה");
						} else {
							warning("שגיאה בעדכון מתכון המנה. רענן ונסה שוב");
						}
						$(this).button('reset');
						$('#editModal').modal('hide');
					},
					failure: function(errMsg) {
					    warning(errMsg);
					    $(this).button('reset');
					},
					error: function(XMLHttpRequest, textStatus, errorThrown) {
					    warning(errorThrown);
					    $(this).button('reset');
					}
				});
				$(this).button('loading');
			} else {
				warning("Not possible");
			}
	    }); // dishUpdateRecipeToday.click
	    
	    $.ajax({
		    type: "GET",
		    url: AJAX_URL + "/restaurants/1/today/json",
		    success: function(data) {
			    //$.each(data.dishes, function( index, dish ) {
				//    $("#chosen-dishes ul").append($("#dish-" + dish.id));
			    //});
			    today_dishes = data.dishes;
		    },
		    failure: function(errMsg) {
			    warning(errMsg);
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
			    warning(errorThrown);
			}
	    }) // $.ajax
	    
	    $.ajax({
			type: "GET",
			url: AJAX_URL + "/restaurants/1/json",
			success: function(data) { 
				g_dishes = data.dishes;
				$.each(data.dishes, function( index, dish ) {
					var today = false;
					$.each(today_dishes, function (index, today_dish) {
						if (today_dish.id == dish.id) {
							today = true;
							dish.recipe = today_dish.recipe
							return;
						}
					});
					
					div_id = "category-" + dish.category;
					li_id = "dish-" + dish.id;
					if ( !$( "#dishes-to-choose #" + div_id ).length ) {
						$("#dishes-to-choose").append(
							'<div class="panel panel-default" id="' + div_id + '"> \
			            <div class="panel-heading"> \
			                <h4 class="panel-title"> \
			                    <a href="#">' + g_categories[dish.category] + '</a> \
			                </h4> \
			            </div> \
			            <div><div class="panel-body"><ul class="nav nav-pills connectedSortable"></ul></div></div> \
			        </div>'
						)
					}
					
					ul_to_add_to = $("#dishes-to-choose #" + div_id + " ul");
					// Div already exists
					if (today) {
						ul_to_add_to = $("#chosen-dishes ul")
					}
					ul_to_add_to.append(
						'<li class="active ' + div_id +'" id="' + li_id + '"><a href="#"><span class="glyphicon glyphicon-pencil"></span>' + dish.name + '</a></li>'
					)
				});
				
				update_callbacks();
				
			},
			failure: function(errMsg) {
			    warning(errMsg);
			},
			error: function(XMLHttpRequest, textStatus, errorThrown) {
			    warning(errorThrown);
			}
		}); // $.ajax
		
		$('#datetimepicker').datepicker({
		    format: "yyyy-mm-dd",
			todayBtn: true,
			calendarWeeks: true,
			todayHighlight: true,
			autoclose: true,
		    language: "he"
	    }).on('changeDate', function (ev) {
		    $("#print_link").attr("href", AJAX_URL + "/restaurants/1/" + get_day() + "/print.html");
		    
		    $.ajax({
			    type: "GET",
			    url: AJAX_URL + "/restaurants/1/" + get_day() + "/json",
			    success: function(data) {
				    if (data.result == "False") {
						warning("שגיאה בעדכון התאריך. רענן ונסה שוב");
						ui.sender.sortable("cancel");
					}
				    
				    $.each(g_dishes, function (index, dish) {
					    li = $("#dish-" + dish.id);
				    	original_category = category_id_from_li($("#dish-" + dish.id));
				    	current_category = li.parent().parent().parent().parent().attr("id");
					    today = false;
				    	$.each(data.dishes, function( index, today_dish ) {
					    	if (dish.id == today_dish.id) {
						    	today = true;
						    	return;
					    	}
				    	});
				    	if (current_category == "chosen-dishes" && !today) {
					    	// It's currently chosen, but it shouldn't be - take it back to where it belongs
					    	$("#dishes-to-choose #category-" + original_category + " ul").append(li);
				    	} else if (current_category != "chosen-dishes" && today) {
					    	// It's currently not chosen, but it should be - choose it
					    	$("#chosen-dishes ul").append(li);
				    	}
				    });
			    },
			    failure: function(errMsg) {
				    warning(errMsg);
				},
				error: function(XMLHttpRequest, textStatus, errorThrown) {
				    warning(errorThrown);
				}
		    })
		}); // datetimepicker.onChangeDate
		
		unspin();
	}); // $(document).ready
});