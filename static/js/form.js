$(document).ready(() => {
  console.log($('#game_developer').val().trim());
  console.log($('#game_developer'));
  $('#collection-item-submission').submit((e) => {
    const gameName = $('#game_name').val().trim();
    const gameDeveloper = $('#game_developer').val().trim();
    const releaseYear = $('#release_year').val().trim();
    const gameDescription = $('#game_description').val().trim();
    const imageCaption = $('#image_caption').val().trim();
    const scoreRating = $('#scoreRating').val().trim();
    const imageFile = $('#image_file').val().trim();
    const consoleResponse = $('#console').val().trim();

    console.log(gameDeveloper);
    console.log($('#game_developer'));

    let valid = true;
    if (gameName === '') {
      $('#game_name').next().text('You must enter a game name');
      valid = false;
    } else {
      $('#game_name').next().text('*');
    }

    if (gameDeveloper === '') {
      $('#game_developer').next().text('You must enter a game developer');
      valid = false;
    } else {
      $('#game_developer').next().text('*');
    }

    if (consoleResponse === '') {
      $('#console').next().text('You must enter a console or platform');
      valid = false;
    } else {
      $('#console').next().text('*');
    }

    if (releaseYear === '') {
      $('#release_year').next().text('You must enter a release year');
      valid = false;
    } else {
      $('#release_year').next().text('*');
    }

    if (gameDescription === '') {
      $('#game_description').next().text('You must enter a game description');
      valid = false;
    } else {
      $('#game_description').next().text('*');
    }

    if (imageFile === '') {
      $('#image_file').next().text('You must enter a game developer');
      valid = false;
    } else {
      $('#image_file').next().text('*');
    }

    if (imageCaption === '') {
      $('#image_caption').next().text('You must enter an image caption');
      valid = false;
    } else {
      $('#image_caption').next().text('*');
    }

    if (scoreRating === '0') {
      // $('#scoreRating').next().text('You must choose a score');
      $('#sr-span').text('You must choose a score')
      valid = false;
    } else {
      // $('#scoreRating').next().text('*');
      $('#sr-span').text('*')
    }

    if (valid === false) {
      e.preventDefault();
    }
  });
});
