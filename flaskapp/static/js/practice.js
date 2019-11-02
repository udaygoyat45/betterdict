var answer = {};

$(document).ready(function() {
    
});

$("button").click(function() {
        var name = (this.id).split(""); 
        if (name[0] == "b")
            answer[name[1]] = 1;
        else
            answer[name[1]] = 0;

        $(("#"+name[1])).fadeOut(500);
});

$("#submit").click(function() {
    
    $.post( "/review", {
        javascript_data: 5/*answer*/ 
    });
    
    alert("done");
});