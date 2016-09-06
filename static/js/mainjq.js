function reloadpg() {

  var create = _.template('<div class="well" id="<%= x %>"></div>');
  var tw = _.template('<p class="text"> <%= a %> </p>');

  $.get("getweets/",function(data){
    json = $.parseJSON(data);

    for(i=0;i<json.length;i++){
      var tweet=json[i].fields.tweet_text;
      console.log(tweet);    
      $(".encl").append(create({ 'x': i }));
      $('#'+i).append(tw({ 'a': tweet }));
    }
  });
  return true;
}  



function stat() {
  $.get("stats/",function(data){
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
        url: "fe_tw/",
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
        url: 'logout/',
        success: function(data){ 
        window.location.href = '/';
                }
          });
  return false;
  });
});