$(function(){

    $('#submit').click(function(){
		
		var search_topic = $('#search').val();
		
				
		if (search_topic){
                chrome.runtime.sendMessage(
					{topic: search_topic},
					function(response) {
						result = response.farewell;
						alert(result.summary);
						
						var notifOptions = {
                        type: "basic",
                        title: "WikiPedia Summary For Your Result",
                        message: result.summary
						};
						
						chrome.notifications.create('WikiNotif', notifOptions);
						
					});
		}
			
			
		$('#search').val('');
		
    });
});