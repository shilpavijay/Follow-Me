function reloadpg() {
  var username = window.location.href;
  username = username.split('/')[4];
  var create = _.template('<div class="well" id="<%= x %>"></div>');
  var tw = _.template('<p class="text"> <p class="twname">@<%= name %> . <span id="dt"> <%= dt %> </span></p><%= a %> </p>');

  $.get("/tweets/"+username+"/",function(data){
    json = $.parseJSON(data);

    for(i=0;i<json.length;i++){
      var name = username;
      var tweet=json[i].fields.tweet_text; 
      var date = json[i].fields.post_date;
      date = date.slice(0,19).split('T')[0] + ' '+ date.slice(0,19).split('T')[1]
      $(".encl").append(create({ 'x': i }));
      $('#'+i).append(tw({ 'name': name, 'dt':date, 'a': tweet }));
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

function fol_users() {
  var username = window.location.href;
  username = username.split('/')[4];
  $.get("/folusers/"+username+"/",function(data){
    json = $.parseJSON(data);
    for(i=0;i<json.length;i++){
      var names = json[i]
      var newb = _.template('<br/><a id ="who" href="/main/<%= name%>/">@<%= name%></a><br/><button class="btn fol btn-primary" type="submit" value="<%= name%>" id="<%= id %>">+ Follow</button><br/>');
      $(".followbuttons").append(newb({ 'id': i, 'name': names}));
    }
  });  
  return true;
}

function followbutton() {
  $(".followbuttons").on("click", ".btn", function(){
    var name = $(this).val();
    name = name.trimLeft().trimRight();
    $(this).text('Following');
    $.ajax({
        type: "POST",
        url: "/users/",
        data: 
        { 
          selection : name
        },
        error: function(data){ 
            console.log('success');        
                }
          });  
  // $(document.body).html();
  return false;
  }); 

}


$("document").ready(function(){
  var username = window.location.href;
  username = username.split('/')[4];
  $("#mainnm").text(username);
  if (pageuser != username) {
    $("#whotofollow").attr("hidden",true);
  }

  reloadpg();
  stat();
  fol_users();
  setTimeout(followbutton,1);

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