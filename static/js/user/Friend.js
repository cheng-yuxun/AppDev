var input = document.getElementById("searchbar");
input.addEventListener("input", myFunction);

function myFunction(e) {
  var filter = e.target.value.toUpperCase();

  var list = document.getElementById("Friendlist");
  var divs = list.getElementsByTagName("div");
  for (var i = 0; i < divs.length; i++) {
    var p = divs[i].getElementsByTagName("p")[0];

    if (p) {
      if (p.innerHTML.toUpperCase().indexOf(filter) > -1) {
        divs[i].style.display = "";
      } else {
        divs[i].style.display = "none";
      }
    }
  }

}
