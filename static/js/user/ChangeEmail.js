var emailField = document.getElementById("email")
var codeField = document.getElementById("code")
var button = document.getElementById("button")
var Newemailfield = document.getElementById("NewEmail")
var code
var submit = document.getElementById("submit")
emailField.disabled = true



if (existing != 'existing' || existing != 'admin'){
    submit.style.display = "none"
    Newemailfield.style.display = "none"
}

if (existing){
   codeField.disabled = true
   button.disabled = true
   Newemailfield.style.display = "block"
   submit.style.display = "block"
}




function Authenticate(){
        button.innerHTML = "Resend"
        sendcode()
        button.setAttribute("onclick" , "javascript: resendcode();")
}


function sendcode(){
    var numberlist = []
    for (let i = 0; i < 6 ; i++){
    x = Math.floor((Math.random() * 10));
    numberlist.push(x);
    }

    code = numberlist.toString().replace(/,/g, '');
    console.log(code)

    setTimeout(function(){
        alert(emailField.value + "The code is " + code)} , 1000)
}



function check(){
submit.style.display = "none"
 if(codeField.value.length == 6){
     if(codeField.value == code){
        submit.style.display = "block"
        Newemailfield.style.display = "block"
        codeField.disabled = true
        button.disabled = true
     }

     else{
     alert("Wrong Code")
     }
 }
}


function resendcode(){
    var timer = 60
    var interval = setInterval(function(){
    timer = timer - 1
    button.innerHTML = "Resend(" + timer + "s)"
    if (timer == 0){
    button.innerHTML = "Resend"
    clearInterval(interval)
    }
    } , 1000);
    sendcode()
    button.disabled = true
    setTimeout(enableresend , 60000)
    }



function enableresend(){
    button.disabled = false
}






