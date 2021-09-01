# Teamer Event RSVP Checker

This is a simple app that allows one to retrieve event RSVP info for the [Teamer](https://teamer.net) app.

The app takes a set of login credentials and prints out all events and corresponding tables for team members, sorting 
them into either `attending`, `not_attending` or `unconfirmed` categories.

This data can either be displayed in the console window, or output to the file rsvp.txt, in the same directory as the 
`Teamer.exe` file.

## Quickstart

If you are on Windows, a prebuilt binary is available on the Releases page, 
click [here](https://github.com/sashahilton00/teamer_rsvp/releases/download/v1.0.0/teamer_rsvp_windows_x86-64.zip) to 
download.

Run the `Teamer.exe` executable to spawn a CLI instance of the app.

Mac and Linux users can run the app using the CLI as detailed below.

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