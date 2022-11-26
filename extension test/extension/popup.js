$(function(){

    $('#submit').click(function(){

		var search_topic = $('#search').val();


		if (search_topic){
                chrome.runtime.sendMessage(
					{topic: search_topic},
					function(response) {
						results = response.farewell;
						results_str = "";
						for (let i = 0; i <results.length; i++) {
						    results_str += "<p>"+(i+1) + ". " + results[i].title + " "+"<a href=\"" + results[i].link + "\">Link</a></p>";
						}
						//alert(link_str);
						var htmlCode = "<html><body>" + results_str + "</body></html>";
						var url = "data:text/html," + encodeURIComponent(htmlCode);

                        chrome.tabs.create({url: url, active: false});
					});
		}


		$('#search').val('');

    });
});