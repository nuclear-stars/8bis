function formatDate(date) {
	if (date == null) date = Date.now();
	var d = new Date(date),
		month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    return [year, month, day].join('-');
}

var storagePrefix = "menuStorage-";
function getStorageValue(key) {
	if (localStorage == undefined) return;
	return localStorage.getItem(storagePrefix + formatDate() + "-" + key);
}
function setStorageValue(key, val) {
	if (localStorage == undefined) return;
	return localStorage.setItem(storagePrefix + formatDate() + "-" + key, val);
}

function changeReactionsStatus(dishId, icons) {
	var reactionArr = {};
	icons.find('.list a').each(function() {
		reactionArr[$(this).data('reaction-id')] = $(this).hasClass('selected');
	});
	$.post({
		// FIXME formatDate() is going to be problematic after midnight
	   // Fix username to be dynamic!
	   data: JSON.stringify({'votes': reactionArr, 'dish_id': dishId, 'date': formatDate(), 'username': Username}),
	   dataType: 'json',
	   url: "/webservice/restaurants/1/dishes/" + dishId + "/",
	   success: function(msg){
		 icons.find('.list a').each(function() {
			setStorageValue(dishId + '-' + $(this).data('reaction-id'), $(this).hasClass('selected'));
		 });
	   }
	});
}

function updateReactionsCount(icons) {
	var selectedNum = icons.find('a.selected').length;
	var count = icons.find('.count > span');
	if (selectedNum == 0) {
		count.hide();
		return;
	}
	count.show().text(selectedNum);
}

$(function() {
	$('.share-icons .list a').each(function() {
		var dishId = $(this).closest('dt').data('dish-id');
		if (getStorageValue(dishId + "-" + $(this).data('reaction-id')) == "true") {
			$(this).addClass('selected');
		}
		updateReactionsCount($(this).closest('.share-icons'));
		
		$(this).click(function() {
			var isOn = !$(this).hasClass('selected');
			$(this).toggleClass('selected');
			var reaction = $(this).closest('.share-icons').siblings('.current-reactions').find('.reaction-' + $(this).data('reaction-id') + ' > em');
			newVal = isOn ? parseInt(reaction.text()) + 1 : parseInt(reaction.text()) - 1;
			reaction.text(newVal);
			if (newVal > 0) {
				reaction.parent().fadeIn(200);
			} else {
				reaction.parent().fadeOut(200);
			}
			var icons = $(this).closest('.share-icons');
			changeReactionsStatus(dishId, icons);
			updateReactionsCount(icons);
		});
	});
});

