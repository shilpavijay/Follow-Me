function following() {
  var username = window.location.href;
  username = username.split('/')[4];

  var create = _.template('<p class="rcornersusr" id="<%= x %>"></p>');
  var tw = _.template('<div class="userbox"></div><a href="/main/<%= a %>/"><p class="folusertext"> <%= a %> </p></a>');

  $.get("/fing/"+username+'/',function(data){
    json = $.parseJSON(data);
    for(i=0;i<json.length;i++){
      var name=json[i].fields.following; 
      $(".flist").append(create({ 'x': i }));
      $('#'+i).append(tw({ 'a': name }));
    }
  });
  return true;
}  

function followers() {
  var username = window.location.href;
  username = username.split('/')[4];

  var create = _.template('<span><p class="rcornersusr" id="<%= x %>"></p></span>');
  var tw = _.template('<div class="userbox"></div><a href="/main/<%= a %>/"><p class="folusertext"> <%= a %> </p></a>');
  $.get("/fers/"+username+'/',function(data){
    json = $.parseJSON(data);
    for(i=0;i<json.length;i++){
      var name=json[i].fields.followers; 
      $(".flist").append(create({ 'x': i }));
      $('#'+i).append(tw({ 'a': name }));
    }
  });
  return true;
} 



function stat() {
  var username = window.location.href;
  username = username.split('/')[4];

  $.get("/stats/"+username+'/',function(data){
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
  var username = window.location.href;
  username = username.split('/')[4];
  $("#mainnm").text(username);
  $("#mainnm").attr("href","/main/"+username+"/");
  
  $(".tweetlist").attr("href","/main/"+username+"/");
  $(".finglist").attr("href","/main/"+username+"/following/");
  $(".ferslist").attr("href","/main/"+username+"/followers/");

  var link = window.location.href
  link = link.slice(-10,-1);
  if (link === 'following') {
    console.log(link);
    following();
  }
  else {
    followers();
  }
  
  stat();
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