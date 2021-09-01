# Teamer Event RSVP Checker

This is a simple app that allows one to retrieve event RSVP info for the [Teamer](https://teamer.net) app.

The app takes a set of login credentials and prints out all events and corresponding tables for team members, sorting 
them into either `attending`, `not_attending` or `unconfirmed` categories.

This data can either be displayed in the console window, or output to the file rsvp.txt, in the same directory as the 
`Teamer.exe` file.

## Running

If you want to run the application, `cd` into the application directory and run `pip install -r requirements.txt`, then 
run the program with `python main.py`.

This will produce an interactive CLI.

## Building

To build the `Teamer.exe` executable, run `python setup.py py2exe` instead of `python main.py`. This will create the 
executable and supporting files in the `executable` directory.

### Notes

If you choose to save the RSVP info to file, this program only outputs to the file `rsvp.txt`, which is excluded in 
`.gitignore`. This file contains PII, and should not be shared publicly.