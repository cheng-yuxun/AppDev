var cardtype = document.getElementById("cardtype")
var cardnumber = document.getElementById("cardnumber")
var expirationdate = document.getElementById("expirationdate")
var ccv = document.getElementById("ccv")

expirationdate.addEventListener('keydown' , event => {
var inputlength = event.target.value.length;

if (event.which != 8){
if (inputlength ==2){
    event.target.value += '/'
}
}

});


cardnumber.addEventListener('input' , function(e){
   e.target.value = e.target.value.replace(/[^\dA-Z]/g, '').replace(/(.{4})/g, '$1 ').trim();
});
