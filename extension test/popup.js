$(function(){

    
    $('#submit').click(function(){
		
		var search_topic = $('#text').val();

		if (search_topic){
                chrome.runtime.sendMessage(
					{topic: search_topic},
					function(response) {
						result = response.farewell;
						alert(result.summary);
						
						var notifOptions = {
							type: "basic",
							//iconUrl: "icon48.png",
							title: "Search Query",
							message: result.summary
						};
						
						chrome.notifications.create('WikiNotif', notifOptions);
						
					});
		}
			
			
		$('text').val('');
		
    });
});