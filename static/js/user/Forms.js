window.addEventListener('load' , (event) => {

var resend = document.getElementById('resend')


if (submit != 'submit'){
Code.style.display = 'none';
Code.disabled = true
resend.style.display= 'none'
}
} );


var code = ""







function change(){
var checkbox = document.getElementById("checkbox")
var text = document.getElementById("switch")
if (window.location.pathname == "/SignUp"){
if (checkbox.checked == true){
window.location.replace("/SignUpPhone")
}
}

else if (window.location.pathname == "/SignUpPhone"){
if (checkbox.checked == false){
window.location.replace("/SignUp")
}
}
}

function validated(input){
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(input.value))
  {
    Authenticate()
  }
    else{
    alert("You have entered an invalid email address!")
    }
}

function Authenticate(){
        var button = document.getElementById("button")
        button.disabled = true
        button.style.display = 'none'
        sendcode()
        Code.disabled = false
        Code.style.display = 'block'
        Code.style.position = 'relative'
        box.style.position = 'relative'
        var label = document.querySelector('label[for="Code"]');
        label.textContent = ' Email Verification Code ';
        resend.disabled = false
        resend.style.display = "block"
    }

function sendcode(){
    var numberlist = []
    var info = document.getElementById("switch").value
    for (let i = 0; i < 6 ; i++){
    x = Math.floor((Math.random() * 10));
    numberlist.push(x);
    }

    code = numberlist.toString().replace(/,/g, '');
    console.log(code)

    setTimeout(function(){
        alert(info + "The code is " + code)} , 500)


}



function check(){
 submit = document.getElementById("submit")
 submit.disabled = false
 if(Code.value.length == 6){
 if(Code.value == code){
 submit.disabled = false

 return true
 }
 else{
 alert("Wrong code")
 submit.disabled = true
 }
 }
}



function resendcode(){
    var submit = document.getElementById("submit")
    var timer = 60
    var interval = setInterval(function(){
    timer = timer - 1
    resend.innerHTML = "Resend(" + timer + "s)"
    if (timer == 0){
    resend.innerHTML = "Resend"
    clearInterval(interval)
    }
    } , 1000);
    sendcode()
    resend.disabled = true
    submit.disabled= true
    setTimeout(enableresend , 60000)
    }



function enableresend(){
    resend.disabled = false
}



function openform(){
    document.getElementById('LoginForm').style.display = 'block'
}


  const togglePassword = document.querySelector('#togglePassword');
  const password = document.getElementById("password")

  togglePassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});


const toggleConfirmPassword = document.querySelector('#toggleConfirmPassword');
const confirmpassword = document.getElementById("confirmpassword")

toggleConfirmPassword.addEventListener('click', function (e) {
    // toggle the type attribute
    const type = confirmpassword.getAttribute('type') === 'password' ? 'text' : 'password';
    confirmpassword.setAttribute('type', type);
    // toggle the eye slash icon
    this.classList.toggle('fa-eye-slash');
});
