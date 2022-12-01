$(function(){

    $('#submit').click(function(){

		var search_topic = $('#search').val();


		if (search_topic){
                chrome.runtime.sendMessage(
					{topic: search_topic},
					function(response) {
						results = response.farewell;
						//results_str = "";
						results_str = "<p><table border='0'>";
						for (let i = 0; i <results.length; i++) {
						    results_str += "<tr><td><p>"+(i+1) + ". " + "<a href=\"" + results[i].link + "\">" + results[i].title + "</a>" + " $" + results[i].price + "</p></td></tr><tr><td><img src=\"" + results[i].image + "\" alt=\"" + results[i].title + "\"></td></tr><tr><td> </td></tr>";
						    //results_str += "<p>"+(i+1) + ". " + "<a href=\"" + results[i].link + "\">" + results[i].title + "</a>" + " $" + results[i].price + "</p>" + "<img src=\"" + results[i].image + "\" alt=\"" + results[i].title + "\">";
						}
						results_str += "</table></p>"
						var htmlCode = "<html><body>" + results_str + "</body></html>";
						var url = "data:text/html," + encodeURIComponent(htmlCode);

                        chrome.tabs.create({url: url, active: false});
					});
		}


		$('#search').val('');

    });
});
