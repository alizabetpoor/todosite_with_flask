var background=document.getElementsByClassName("dark")[0];
var loginform=document.getElementsByClassName("login-popup")[0];
var registerform=document.getElementsByClassName("register-popup")[0];
var loginerror=loginform.getElementsByClassName("error")[0];
var registererror=registerform.getElementsByClassName("error")[0];
if (loginerror != null){
        openloginpopup()
}
else if(registererror !=null){
        openregisterpopup()
}
function loadingpage()
{
    var time=new Date;
    var current_hour=time.getHours()
    var current_minute=time.getMinutes()
    
    current_hour=current_hour.toString()
    current_minute=current_minute.toString()
    if(current_hour.length!=2)
    {
        current_hour="0"+current_hour
    }
    if(current_minute.length!=2)
    {
        current_minute="0"+current_minute
    }
    var current_time=current_hour+":"+current_minute
    document.getElementById("timeinput").value=current_time;
    console.log(current_time)
}
function openregisterpopup(){
    registerform.style.display="block";
    background.style.width=window.innerWidth+"px"
    background.style.height=window.innerHeight+"px"
    background.style.display="inline"
}
function openloginpopup(){
    loginform.style.display="block"
    background.style.width=window.innerWidth+"px"
    background.style.height=window.innerHeight+"px"
    background.style.display="inline"
}
function closepopup(){
    loginform.style.display="none";
    background.style.display="none";
    registerform.style.display="none";
}
function closedark(obj){
    var loginform=document.getElementsByClassName("login-popup")[0]
    obj.style.display="none";
    loginform.style.display="none";
    registerform.style.display="none";
}