from random import choice
from termcolor import colored

positivity = (
    "Nice",
    "Way to go",
    "Cool",
    "Awesome",
    "Keep it going",
    "Good going",
    "You got this",
    "Not bad",
    "That's what I'm talking about",
    "Go get 'em",
    "Atta boy",
    "Amazing",
    "מזוין",
    "Incredible",
    "Magnificent",
    "Fantastic",
    "Like a boss",
    "Wonderful",
    "Livin' the dream",
    "Inimitable",
    "Genius",
    "Stick it to the man",
    "You've got the power",
    "Ain't nobody gonna break your stride",
    "That's how we do it",
    "Killin' it",
    "You da man",
    "The man with a plan",
    "Sensational",
    "You're an inspiration",
    "Going above and beyond",
    "A+",
    "Superb",
    "Magical",
    "Phat",
    "Dope",
    "Sweet",
    "Smokin'",
    "Encroyable",
    "Magnifique",
    "Hit it",
    "High five",
    "Solid",
    "Great",
    "Good"
)

def niceJob():
    return choice(positivity) + "!"

invalid = colored("Please enter a valid command.", "red")