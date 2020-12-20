# revision-system

## What Is It?

This project uses spaced repetition to help you learn discrete facts for the kinds of exams that demand them.

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

## How It Works

Questions and answers are stored in a sqlite3 database, which tracks what questions you've answered and when.

Questions are tagged with at least one 'tag'. These tags categorise the questions, so that (for example) questions on AWS can be separated from questions on GCP.

Tags can be arbitrarily set, with a 1-n relationship between question and tag.


