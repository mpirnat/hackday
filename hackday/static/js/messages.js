
function place_message()
{
	var rand = parseInt((Math.random() * 1000));
	var tweet_count = $('.tweet_list li').length;

	var index = rand % tweet_count;

	var node = $('.tweet_list li')[index];
	if ($('#hidden-message').length > 0 && node)
	{
		$('.tweet_text', node).replaceWith($('#hidden-message'));
		$('#hidden-message').css({'display': ''});
		$('.tweet_retweet, img', node).css({'display': 'none'});
	}
}


