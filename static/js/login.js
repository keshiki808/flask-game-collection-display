$(document).ready(() => {

$("#login-form").submit((e) => {
    const email = $('#email').val().trim();
    const password = $('#password').val().trim();
    let valid = true;

    if (email == ""){
      $('#email').next().text("Login email field cannot be empty")
      valid = false
    } else if (email.length > 100) {
      $('#email').next().text("Login field cannot be greater than 100 characters in length")
      valid = false
    }
    else{
      $('#email').next().text("")
    }
    if (password == ""){
      $('#password').next().text("You must enter a password")
      valid = false
    }else if (password.length > 100) {
      $('#password').next().text("Password field cannot be greater than 100 characters in length")
      valid = false
    }else{
      $('#password').next().text("")
    }

    if (valid === false) {
      e.preventDefault();
    }
})
})





