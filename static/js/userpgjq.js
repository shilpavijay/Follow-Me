function reloadpg() {

  var create = _.template('<div class="well" id="<%= x %>"></div>');
  var tw = _.template('<p class="text"> <%= a %> </p>');

  $.get("/selftweets/",function(data){
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

function fol_users() {
  $.get("/folusers/",function(data){
    json = $.parseJSON(data);
    for(i=0;i<json.length;i++){
      var names = '@' + json[i]
      var newb = _.template('<button class="btn btn-primary" type="submit" id="<%= id %>"> <%= name %> </button><br/><br/>');
      $(".followbuttons").append(newb({ 'id': i, 'name': names}));
    }
  });  
  return true;
}

function followbutton() {
  $(".followbuttons").on("click", ".btn", function(){
    name = $(this).text();
    name = name.trimLeft().trimRight().slice(1);
    $.ajax({
        type: "POST",
        url: "/users/",
        data: 
        { 
          selection : name
        },
        success: function(data){ 
          // $(".followbuttons").empty();     
              // location.reload();
              location.href = location.href;
                }
          });
  return false;
  }); 
}


$("document").ready(function(){
  reloadpg();
  stat();
  fol_users();
  setTimeout(followbutton,5);
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