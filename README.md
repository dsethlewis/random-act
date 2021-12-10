# A Random Act of Something

This is a command-line Python application designed to solve a specific, yet common, problem of descision paralysis.

## Rationale

You have some spare time&mdash;maybe you have a few minutes between meetings, or maybe it's just a lazy Sunday afternoon. Nothing particularly important or urgent is demanding your attention. How do you decide what to do with your time? 

There are an infinite number of things you could do: chores, errands, phone calls, hobbies, entertainment, exercise, work, etc. Too many options, and no meaningful way to pick!

So you do the only sane thing. You pull out your phone and start swiping around aimlessly looking for a way to pass the time.

Let me suggest another choice: just pick randomly. Put everything you might do when you don't know what to do into a list, and literally pick randomly.

That's what this application does. Using PostgreSQL for a local database and SQLAlchemy for a DBAPI, it traverses a hierarchy of activities at random.

## Features

- **Simple command-line interface (CLI)**: build list, display list, pick next activity, and make modifications.
- **Random but not arbitrary**: application prompts user to adjust base rates, and uses weights for time-of-day based on a novel circular-mean based algorithm
- **Order within chaos**: create ordered routines where approprate, e.g., shower before you shave

## In Development

- **Webapp** interface using Flask
- **New weights** based on response speed and sequencing

## Pull Requests

This project is currently free and open source, and I welcome collaboration. Please feel free to submit pull requests. However, I reserve the right to develop a public, commercial application using this codebase in the future.