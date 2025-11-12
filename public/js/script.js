
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


// search functionality 

function searchContacts(){
    var input=document.querySelector('.search-box');
    if(input){
        var searchTerm=input.value.toLowerCase();
        console.log("searching for: "+searchTerm);


    }
}


function confirmDelete(name){
    var result=confirm("Are you sure you want to delete "+name+"?");
    return result;
}


// button hover thing 
function buttonEffect(){
    var btns=document.querySelectorAll('.btn');
    for(var i=0; i<btns.length; i++){
        btns[i].addEventListener('mouseover',function(){
            console.log('button hovered');
        });
    }
}


var clickCount=0;
function countClicks(){
    clickCount++;
    console.log("total clicks: "+clickCount);
}


// everything runs when page finishes loading
window.onload=function(){
    console.log("page loaded!");
    

    var searchBox=document.querySelector('.search-box');
    if(searchBox){
        searchBox.addEventListener('keyup',searchContacts);
    }
    
    buttonEffect();
    
    
};


// Note TODO: figure out how to actually filter the contacts