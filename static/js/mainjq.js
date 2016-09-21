function reloadpg() {

  var create = _.template('<div class="well" id="<%= x %>"></div>');
  var tw = _.template('<p class="text"> <p class="twname"><a href="<%= usr %>">@<%= name %></a> . <span id="dt"> <%= dt %> </span></p><%= tw %> </p>');

  $.get("/getweets/",function(data){
    json = $.parseJSON(data);
    var i = 0
    $.each(json, function(date,field){     
      $.each(field,function(tweet,username){    
        $(".encl").append(create({ 'x': i }));
        $('#'+i).append(tw({ 'name': username, 'usr': username+'/', 'dt':date, 'tw': tweet }));
        ++i;       
     });
    });
  });
  return true;
}  



function stat() {
  $.get("/stats/",function(data){
    json = $.parseJSON(data);
    cnt=json.count;
    following=json.following;
    followers=json.followers;
    $("#count").text(cnt);
    $("#ficnt").text(following);
    $("#fecnt").text(followers);
  });  
  return true;
}



$("document").ready(function(){
  reloadpg();
  stat();
  $("#submit").click(function(event){
    if($(".form-control").val().length===0){
      event.preventDefault();
    }
    else {
    $.ajax({
        type: "POST",
        url: "/fe_tw/",
        data: 
        { 
          tweetxt : $("#tweetxt").val()
        },
        success: function(data){ 
          $(".encl").empty();     
          $("#tweetxt").val('');
          reloadpg();
          stat();
                }
          });
  }
  return false;
  });  

  $("#sublogout").click(function(event){
    $.ajax({
        type: "POST",
        url: '/logout/',
        success: function(data){ 
        window.location.href = '/';
                }
          });
  return false;
  });
});