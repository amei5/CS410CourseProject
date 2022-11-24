$(function(){

    $('#submit').click(function(){
		
		var search_topic = $('#search').val();
		
				
		if (search_topic){
                chrome.runtime.sendMessage(
					{topic: search_topic},
					function(response) {
						results = response.farewell;
						str = "";
						for (let i = 0; i <results.length; i++) {
						    str += (i+1) + ". " + results[i].title + "\n";
						}
						alert(str);

						var notifOptions = {
                        type: "basic",
                        title: "WikiPedia Summary For Your Result",
                        message: result[0].title
						};
						
						chrome.notifications.create('WikiNotif', notifOptions);
						
					});
		}
			
			
		$('#search').val('');
		
    });
});