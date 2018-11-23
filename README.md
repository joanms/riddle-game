# [Riddle Game](http://joans-riddle-game.herokuapp.com/)

This is a game in which users, each with a unique user name, are presented with a series of 10 riddles. The top scores are listed in a leader board, in descending order. 
It is the milestone project for the Practical Python module of Code Institute's mentored online full-stack software development course.
 
 
## UX

Please [click here](https://drive.google.com/file/d/1NEO0yWcnmsEMqvmtsFM2Q9IrvU__8o-V/view?usp=sharing) to see a flowchart of the game logic.
 
### User Stories

As a user, I want to:
- **Play a game with clear, intuitive rules.**
Each step in the game, from login through to the end, is explained in clear and succinct on-screen messages.

- **Get clear, immediate feedback on my progress.**
Each time the user answers a question, a message appears telling them whether or not they got it right and what the next step is.

- **See how I compare to other players.**
There is a link to the leaderboard at the top of each page, and the user is encouraged to check it when they've finished the game.

### Design

I chose the cursive heading font to represent the non-linear thinking needed to answer riddles. The instructions and riddles are in a simpler font 
to avoid unnecessary confusion. The background image avoids distraction by being mostly monochrome with orange accents. The navbar links turn into 
the same orange when the user hovers over them. The green background of the header and main text box was chosen as a complementary colour to the orange.


## Features
 
### Existing Features

- **Login page** where the user can enter a username and start the game.
- **Sessions** to store data about the game and the user for each instance of gameplay.
- **Instructions** on the gameplay page explaining the rules and what the user can expect.
- **Flashed messages** to tell the user when they have got something wrong and congratulate them when they answer a riddle correctly.
- **Answer form** to input their answers to the riddles.
- **Leaderboard** ranking the users so that they can see how they compare to other players.

### Features Left to Implement

- **The option to return to the game with an existing username.** Without secure user authentication, which is out of the scope of this 
module, there's no easy way to differentiate between a returning user and a user who has chosen the same username as another user. 
Consequently, users must choose a new username each time they log in.

- **More riddles, with a random selection presented each time a user logs in.** This would enable a user to play the game multiple times 
without seeing the same riddles over and over.


## Technologies Used

- **[HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)** was used to write the content of the site.
- **[CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)** was used to style the content.
- **[Bootstrap](https://getbootstrap.com/)** was used to simplify the layout and responsiveness.
- **[Python](https://www.python.org/)** was used to write the game logic.
- **[unittest](https://docs.python.org/2/library/unittest.html)** was used for automated testing of the Python code.
- **[Flask](http://flask.pocoo.org/)** was used to create a session for each login, route through the game and render HTML templates.


## Testing

### Automated Tests

Automated testing was done with unittests, and the tests are in test.py at the root directory. Run the tests by typing "python3 test.py" in the terminal. 
Please note that test_correct_login() will fail if the username in the test is already in users.txt, because the game requires each user to have a unique username.

### Manual Tests

Manual tests of the application were conducted as follows:

1. Login:
    1. Go to the "Login" page
    2. Enter a new username and click the Login button. 
    3. Ensure that the username is added to users.txt and I am taken to the gameplay page.
    3. Return to the "Login" page.
    4. Enter a username that is already in users.txt.
    5. Ensure that a flashed message appears, telling me that the username is already taken.

2. Playing the Game
    1. Enter the correct answer to a riddle and click submit.
    2. Ensure that the score is incremented and the next riddle appears.
    3. Enter a wrong answer to a riddle.
    4. Ensure that I see a message telling me I got it wrong, and prompting me to try again.
    5. Enter the correct answer on the second attempt.
    6. Ensure that the score is incremented and the next riddle appears.
    7. Enter a wrong answer to a riddle.
    8. Ensure that I see a message telling me I got it wrong, and prompting me to try again.
    9. Enter a wrong answer on the second attempt.
    10. Ensure that the next riddle appears, the score is unchanged and I see a message telling me I got the last riddle wrong.
    11. Play the game through to the end.
    12. Ensure that I am taken to the leaderboard page, and that it includes a message giving the answer to the last riddle and the player's score along with the leaderboard.
    13. Play the game on two devices simultaneously to ensure that there were no errors caused by simultaneous play.

3. Leaderboard
    1. Play the game through to the end more than 10 times with different usernames, making different numbers of deliberate errors each time.
    3. Ensure that the top 10 usernames and scores are correctly listed in the leaderboard, in descending order of score.

4. Cross-browser and Device Compatibility
    1. Play the game on Chrome, Edge, Firefox and Opera browsers to ensure that it works on all of them.
    2. Play the game on a desktop, laptop, tablet and smartphone to ensure that it works on all devices.

5. Responsiveness
    1. Check the game in responsive mode with Chrome Developer Tools to ensure that the size and position of elements adjusts correctly.
    2. Check the game on a desktop, laptop, tablet and smartphone to ensure that it displays correctly. On large screens, the navbar appears 
    at the top right of the page. On smaller screens, it appears below the main heading, and the size of all text is reduced to avoid overflow.


## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
The riddles are from the [Riddle Solution Answer Database](https://riddle.solutions/).

### Media
The background image and favicon are free stock images from [Pixabay](https://pixabay.com/).

### Acknowledgements
My fellow student, Joke Heyndels, my tutors, Nakita McCool, Niel McEwen and Haley Schafer, and 
my mentor, Chris Zielinski provided valuable help with the project.

The syntax in test.py is based on [this YouTube video](https://www.youtube.com/watch?v=1aHNs1aEATg&list=PLLjmbh6XPGK4ISY747FUHXEl9lBxre4mM&index=8&t=0s). 
