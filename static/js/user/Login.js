
function openform(){
    document.getElementById('LoginForm').style.display = 'block'
}


function openforgetpasswordform(){
    document.getElementById('ForgetPassword').style.display = 'block'
    document.getElementById('LoginForm').style.display = 'none'
}

function closeforgetpasswordform(){
    document.getElementById('ForgetPassword').style.display = 'none'
    document.getElementById('LoginForm').style.display = 'block'
}

