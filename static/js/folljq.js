function following() {

  var create = _.template('<span><p class="rcornersusr" id="<%= x %>"></p></span>');
  var tw = _.template('<p class="text"> <%= a %> </p>');

  $.get("/fing/",function(data){
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

  var create = _.template('<span><p class="rcornersusr" id="<%= x %>"></p></span>');
  var tw = _.template('<p class="text"> <%= a %> </p>');

  $.get("/fers/",function(data){
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