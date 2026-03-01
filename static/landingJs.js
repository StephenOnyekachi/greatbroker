
window.addEventListener('scroll', menuChange);
function menuChange(){
    const nav = document.querySelector('.myMenu');
    if (window.scrollY > 30) {
        nav.classList.add('active');
    } else {
        nav.classList.remove('active');
    }
}

window.addEventListener('scroll', slide);
function slide(){
    var reavels = document.querySelectorAll('.slidetop');
    
    for(var i = 0; i < reavels.length; i++){

        var windowheight = window.innerHeight;
        var reaveltop = reavels[i].getBoundingClientRect().top;
        var reavelpoint = 60;

        if(reaveltop < windowheight - reavelpoint){
            reavels[i].classList.add('active');
        }
        else{
            reavels[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', leftslide);
function leftslide(){
    var reavels = document.querySelectorAll('.slideleft');
    
    for(var i = 0; i < reavels.length; i++){

        var windowheight = window.innerHeight;
        var reaveltop = reavels[i].getBoundingClientRect().top;
        var reavelpoint = 10;

        if(reaveltop < windowheight - reavelpoint){
            reavels[i].classList.add('active');
        }
        else{
            reavels[i].classList.remove('active');
        }
    }
}

window.addEventListener('scroll', zoomIn);
function zoomIn(){
    var reavels = document.querySelectorAll('.zoom-in');
    
    for(var i = 0; i < reavels.length; i++){
        var windowheight = window.innerHeight;
        var reaveltop = reavels[i].getBoundingClientRect().top;
        var reavelpoint = 0;

        if(reaveltop < windowheight - reavelpoint){
            reavels[i].classList.add('active');
        }
        else{
            reavels[i].classList.remove('active');
        }
    }
}


// for showing and hiding menu on small screens
// this 
function nav() {
    const bar = document.querySelector('.menu-bar');
    const menu = document.querySelector('.one-quater');
    const mediaMenu = document.querySelector('.media-menu');
    bar.addEventListener('click', () => { 
        mediaMenu.classList.toggle('active');
        menu.classList.toggle('active');
        console.log(menu.classList.contains('active') ? "menu opened" : "menu closed"); 
    });
}nav();

// or
// const nav = document.querySelector('.bar'); 
// const menu = document.querySelector('.one-quater'); 
// nav.addEventListener('click', () => { 
//     menu.classList.toggle('active'); 
//     console.log(menu.classList.contains('active') ? "menu opened" : "menu closed"); 
// }); 

// for showing and hidding password
function setupPasswordToggles() {
    const toggles = document.querySelectorAll('.toggle')
    toggles.forEach(toggle => {
        const passInput = toggle.previousElementSibling // the <input> before the icon

        toggle.addEventListener('click', () => {
            if (passInput.type === 'password') {
                passInput.type = 'text'
                toggle.classList.remove('fa-eye')
                toggle.classList.add('fa-eye-slash')
                console.log('password showing')
            } else {
                passInput.type = 'password'
                toggle.classList.remove('fa-eye-slash')
                toggle.classList.add('fa-eye')
                console.log('password hidden')
            }
        })
    })
}
document.addEventListener('DOMContentLoaded', setupPasswordToggles);

// for showing change profile button
function changeProfile(){
    const profileBT = document.querySelector('#profileBT')
    const viewbox = document.querySelector('.varify-cover')
    const profile = document.querySelector('#profile')
    const pin = document.querySelector('#pin')
    const password = document.querySelector('#password')
    if (profileBT && viewbox && pin && password) {
        profileBT.addEventListener('click', (e) => {
            e.preventDefault() // stops form submission
            viewbox.classList.toggle('active')
            pin.style.display = 'none'; // hide the pin section
            password.style.display = 'none'; // hide the password section
            profile.style.display = 'block'; // show the profile section
            console.log('click')
        })
    }
}changeProfile();

// for showing change pin button
function changePin(){
    const pinBT = document.querySelector('#pinBT')
    const viewbox = document.querySelector('.varify-cover')
    const profile = document.querySelector('#profile')
    const pin = document.querySelector('#pin')
    const password = document.querySelector('#password')
    if (pinBT && viewbox && profile && password) {
        pinBT.addEventListener('click', (e) => {
            e.preventDefault() // stops form submission
            viewbox.classList.toggle('active')
            profile.style.display = 'none'; // hide the profile section
            password.style.display = 'none'; // hide the password section
            pin.style.display = 'block'; // show the pin section
            console.log('click')
        })
    }
}changePin();

// for showing change password button
function changePassword(){
    const passBT = document.querySelector('#passBT')
    const viewbox = document.querySelector('.varify-cover')
    const profile = document.querySelector('#profile')
    const pin = document.querySelector('#pin')
    const password = document.querySelector('#password')
    if (passBT && viewbox && profile && pin && password) {
        passBT.addEventListener('click', (e) => {
            e.preventDefault() // stops form submission
            viewbox.classList.toggle('active')
            profile.style.display = 'none'; // hide the profile section
            pin.style.display = 'none'; // hide the pin section
            password.style.display = 'block'; // show the password section
            console.log('click')
        })
    }
}changePassword();

// for showing pop up confirm box
function verify() {
    const button = document.querySelector('#confirm'); 
    const view = document.querySelector('.varify-cover'); 
    if (button && view) {
        button.addEventListener('click', (e) => { 
            e.preventDefault();
            view.classList.toggle('active'); 
            console.log(view.classList.contains('active') ? 'showing now' : 'hidden now'); 
        }); 
    } else {
        console.warn('Confirm button or varify-cover not found in DOM');
    }
}
document.addEventListener('DOMContentLoaded', verify);

// for showing increase user balance button
function usersBalance(){
    const userBalance = document.querySelector('#userBalance')
    const viewbox = document.querySelector('.varify-cover')
    const balance = document.querySelector('#balance')
    if (userBalance && viewbox) {
        userBalance.addEventListener('click', (e) => {
            e.preventDefault() // stops form submission
            viewbox.classList.toggle('active')
            balance.style.display = 'block'; // show the user balance section
            console.log('click')
        })
    }
}usersBalance();


