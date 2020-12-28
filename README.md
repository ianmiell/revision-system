# Revision System

## What Is It?

This project uses [spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition#:~:text=Spaced%20repetition%20is%20a%20method,fact%20is%20presented%20or%20said.) to help you learn discrete facts for the kinds of exams that demand them.

It's a serverless application - the entire state is stored in a sqlite db that's reconstructed and saved on each run. More on this pattern [here](https://zwischenzugs.com/2017/08/07/a-non-cloud-serverless-application-pattern-using-git-and-docker/)

## Get Started

Fork this repository, and clone it to your machine.

Run:

```
./run
```

To get going, and follow the instructions.

After a question session, it's important to save state by quitting, using the menu. This will save state back to the repository so it can be run again from anywhere else.

If you exit unexpectedly and want to save state, run:

```
./save
```

## Features

- Stores your answer history within the repo

- Orders questions, prioritising ones that you have never answered, or got wrong previously

- Allows you to categorise questions by tag

- You can 'ignore' questions for n days if you feel like you will know them in the next n days, but need reminding about them later

- If you 'miss' days of revision, you will be asked the question again until you 'catch up' with the number of times the question should have been asked up to the present time

- Does not ask the same question twice in a day


## How It Works

Questions and answers are stored in a sqlite3 database, which tracks what questions you've answered and when.

Questions are tagged with at least one 'tag'. These tags categorise the questions, so that (for example) questions on AWS can be separated from questions on GCP.

Tags can be arbitrarily set, with a 1-n relationship between question and tag.

## Pre-Loaded Questions

There are twenty questions and three tags set up to get you going as an example. If you want a completely fresh environment, go into the `db/db_export.sql` file and remove all the `INSERT` lines, then commit and push.

## Requirements

```
pip3 install -r requirements
```

Also depends on:

```
git
make
python3
sqlite3
```

