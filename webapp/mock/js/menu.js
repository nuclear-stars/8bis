$(function() {
	$('.share-icons .list a').each(function() {
		$(this).click(function() {
			var isOn = !$(this).hasClass('selected');
			$(this).toggleClass('selected');
			var type = this.className.replace('selected', '').replace(' ', '');
			var reaction = $(this).closest('.share-icons').siblings('.current-reactions').find('.' + type + ' > em');
			newVal = isOn ? parseInt(reaction.text()) + 1 : parseInt(reaction.text()) - 1;
			reaction.text(newVal);
			if (newVal > 0) {
				reaction.parent().fadeIn(200);
			} else {
				reaction.parent().fadeOut(200);
			}
			
			var selectedNum = $(this).parent().children('a.selected').length;
			var count = $(this).closest('.share-icons').find('.count > span');
			if (selectedNum == 0) {
				count.hide();
				return;
			}
			count.show().text(selectedNum);
		});
	});
});
