$(document).ready(() => {

$("#login-form").submit((e) => {
    const email = $('#email').val().trim();
    const password = $('#password').val().trim();
    let valid = true;

    if (email == ""){
      $('#email').next().text("Login email field cannot be empty")
      valid = false
    } else{
      $('#email').next().text("")
    }
    if (password == ""){
      $('#password').next().text("You must enter a password")
      valid = false
    }else{
      $('#password').next().text("")
    }

    if (valid === false) {
      e.preventDefault();
    }
})
})





