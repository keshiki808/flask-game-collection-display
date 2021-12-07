$(document).ready(() => {
  $('#collection-item-submission').submit((e) => {
    const gameName = $('#game_name').val().trim();
    const gameDeveloper = $('#game_developer').val().trim();
    const releaseYear = $('#release_year').val().trim();
    const gameDescription = $('#game_description').val().trim();
    const imageCaption = $('#image_caption').val().trim();
    const scoreRating = $('#scoreRating').val().trim();
    const imageFile = $('#image_file').val().trim();
    const consoleResponse = $('#console').val().trim();



    let valid = true;
    if (gameName === '') {
      $('#game_name').next().text('You must enter a game name');
      valid = false;
      console.log($('#game_name').next().text('You must enter a game name').length)
    } else if (gameName.length > 50){
      $('#game_name').next().text('Name must be 50 characters or less');
      valid= false;
    }
    else {
      $('#game_name').next().text('*');
    }

    if (gameDeveloper === '') {
      $('#game_developer').next().text('You must enter a game developer');
      valid = false;
    } else if (gameDeveloper.length > 50){
      $('#game_developer').next().text('Developer name must be 50 characters or less');
      valid= false;
    }else {
      $('#game_developer').next().text('*');
    }

    if (consoleResponse === '') {
      $('#console').next().text('You must enter a console or platform');
      valid = false;
    } else if (consoleResponse.length > 25){
      $('#console').next().text('Console name must be 25 characters or less');
      valid= false;
      }
    else {
      $('#console').next().text('*');
    }

    if (releaseYear === '') {
      $('#release_year').next().text('You must enter a release year');
      valid = false;
    } else if (releaseYear.length < 4 || releaseYear.length > 4 || releaseYear < 1900){
      $('#release_year').next().text('Release year be a valid 4 digit year');
      valid= false;
      }else {
      $('#release_year').next().text('*');
    }

    if (gameDescription === '') {
      $('#game_description').next().text('You must enter a game description');
      valid = false;
    } else if (gameDescription.length > 200){
      $('#game_description').next().text('Game description must be 200 characters or less');
      valid= false;
      }else {
      $('#game_description').next().text('*');
    }

    if (imageFile === '') {
      $('#image_file').next().text('You must submit an image');
      valid = false;
    } else {
      $('#image_file').next().text('*');
    }

    if (imageCaption === '') {
      $('#image_caption').next().text('You must enter an image caption');
      valid = false;
    } else if (imageCaption.length > 50){
      $('#game_description').next().text('Image caption must be 50 characters or less');
      valid= false;
      }else {
      $('#image_caption').next().text('*');
    }

    if (scoreRating === '0') {
      $('#sr-span').text('You must choose a score')
      valid = false;
    } else {
      $('#sr-span').text('*')
    }

    if (valid === false) {
      e.preventDefault();
    }
  });
});
