
// trying to validate the form before it submits
function checkForm(){
    var fname = document.querySelector('input[name="first_name"]').value;
    var lname = document.querySelector('input[name="last_name"]').value;
    var mail = document.querySelector('input[name="email"]').value;
    
    if(fname=="" || lname=="" || mail==""){
        alert("Please fill out all required fields!");
        return false;
    }
    return true;
}


// search  
// how to actually filter the contacts?
function searchContacts(){
    var input=document.querySelector('.search-box');
    if(input){
        var searchTerm=input.value.toLowerCase();
        console.log("searching for: "+searchTerm);
    }
}


// burger menu for mobile - finally figured this out!
function setupBurgerMenu(){
    var burger=document.querySelector('.burger-menu');
    var navLinks=document.querySelector('.nav-links');
    
    if(burger && navLinks){
        burger.addEventListener('click',function(){
            navLinks.classList.toggle('active');
            burger.classList.toggle('active');
            console.log('menu toggled');
        });
    }
}



// test
window.openNav = function () {
    document.getElementById("nav-links").style.display = "none";

    document.getElementById("sidebar").style.width = "25%";
    document.getElementById("main-div").style.marginRight = "25%";
    document.getElementById("translucent-background").hidden = false;
};
window.closeNav = function () {
    document.getElementById("nav-links").style.display = "flex";
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("main-div").style.marginRight = "0";
    document.getElementById("translucent-background").hidden = true;
};