import binascii
import os
from datetime import datetime
import sys

import click
import requests
from tabulate import tabulate

headers = {
    'TEAMER-APP-REQUEST': 'iPhone',
    'TEAMER-APP-VERSION': '5.3.7',
    'User-Agent': 'Teamer/4 (iPhone; iOS 14.6; Scale/2.00)',
}


def get_user_info():
    username = click.prompt('Enter your Teamer email', type=str)
    password = click.prompt('Enter your Teamer password', type=str, hide_input=True)

    data = {
        'id': None,
        'has_membership': False,
        'payment_only': False,
        'phone': None,
        'status': None,
        'single_access_token': None,
        'email_campaign_opted_out': False,
        'birth_year': None,
        'sms_supported_country': None,
        'password': password,
        'first_name': None,
        'opted_in?': None,
        'has_club_membership': False,
        'city': None,
        'state_province': None,
        'last_name': None,
        'country': None,
        'email': username,
        'country_code': None
    }

    click.clear()

    try:
        r = requests.post('https://teamer.net/api/v3/auth/login', json=data, headers=headers)
        r.raise_for_status()

        response_data = r.json()

        click.echo('Logged in as: {}'.format(response_data['full_name']))
        return response_data['single_access_token'], response_data['id']

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            click.echo('Unable to login to Teamer, invalid username/password combination.')
        else:
            click.echo('Unable to login to Teamer, HTTP error {}.'.format(e.response.status_code))
        sys.exit(1)


def get_teams(user_id):
    try:
        r = requests.get(f'https://teamer.net/api/v3/users/{user_id}/teams', headers=headers)
        return r.json()
    except requests.exceptions.HTTPError as e:
        click.echo('Unable to retrieve teams, HTTP error {}.'.format(e.response.status_code))
        sys.exit(1)


def get_selected_team(teams):
    choices = []
    for t in teams:
        choices.append(t['team']['name'])

    chosen_team = click.prompt(
        'Select the team you want to retrieve events for',
        type=click.Choice(choices, case_sensitive=False)
    )

    chosen_team_id = None
    chosen_team_internal_id = None

    for t in teams:
        if t['team']['name'].lower() == chosen_team.lower():
            chosen_team_internal_id = t['id']
            chosen_team_id = t['team']['id']
            break

    if chosen_team_id is None or chosen_team_internal_id is None:
        click.echo('No team selected.')
        sys.exit(1)
    else:
        return chosen_team_id, chosen_team_internal_id


def get_events(team_id):
    try:
        r = requests.get(f'https://teamer.net/api/v3/events?page=1&team_id={team_id}&view=upcoming', headers=headers)
        events = r.json()
        return events
    except requests.exceptions.HTTPError as e:
        click.echo(f'Unable to retrieve events for team, HTTP error {e.response.status_code}')
        sys.exit(1)


def get_event_notifications(event_id, team_id):
    data = {
        'attending': [],
        'not_attending': [],
        'unconfirmed': []
    }

    try:
        r = requests.get(f'https://teamer.net/api/v3/notifications?event_id={event_id}&filter=lineup&team_id={team_id}',
                         headers=headers)
        entries = r.json()

        for e in entries:
            member = {
                'full_name': e['full_name'],
                'email': e['users'][0]['email'],
                'phone': e['users'][0]['phone'],
                'reason': e['reason']
            }

            if e['status'] == 'sent':
                data['unconfirmed'].append(member)
            elif e['status'] == 'declined':
                data['not_attending'].append(member)
            elif e['status'] == 'accepted':
                data['attending'].append(member)

        return data

    except requests.exceptions.HTTPError as e:
        click.echo(f'Unable to retrieve RSVPs for event, HTTP error {e.response.status_code}')
        sys.exit(1)


def get_rsvps(events):
    event_rsvps = {}

    with click.progressbar(events) as p_events:
        for e in p_events:
            title = '{} - {}'.format(e['title'], datetime.utcfromtimestamp(e['starts_at']).strftime('%Y-%m-%d %H:%M'))
            event_rsvps[title] = get_event_notifications(event_id=e['id'], team_id=e['team_id'])

        # This deletes any events where there are no attendees from the returned results
        for k in list(event_rsvps.keys()):
            if all(len(b) == 0 for a, b in event_rsvps[k].items()):
                del event_rsvps[k]

        return event_rsvps


def print_rsvp_tables(rsvps):
    click.clear()

    write_to_file = click.prompt('Do you want to save the RSVP info to the file rsvp.txt?', type=bool)

    output_location = None
    if write_to_file:
        output_location = open('rsvp.txt', 'w')

    for event, statuses in rsvps.items():
        click.secho(f'Event: {event}\n', fg='bright_yellow', bg='blue', bold=True, file=output_location)

        for status, members in statuses.items():
            colours = {
                'attending': 'bright_green',
                'not_attending': 'bright_red',
                'unconfirmed': 'bright_blue'
            }
            click.secho(f'Status: {status}\n', fg=colours[status], file=output_location)

            headers = ['Full Name', 'Email', 'Phone', 'Reason']
            table_data = []

            for m in members:
                table_data.append([
                    m['full_name'],
                    m['email'],
                    m['phone'],
                    m['reason']
                ])

            click.echo(tabulate(tabular_data=table_data, headers=headers, tablefmt='orgtbl') + '\n', file=output_location)

    click.secho('Press any key to close', bold=True)
    click.pause()


def main():
    click.clear()
    access_token, user_id = get_user_info()

    random_token = str(binascii.b2a_hex(os.urandom(32)))
    # This appears to be a random 32 byte token
    headers['TEAMER-APP-TOKEN'] = random_token

    headers['Authorization'] = access_token

    teams = get_teams(user_id=user_id)
    team_id, internal_team_id = get_selected_team(teams)

    headers['Logged-Member-ID'] = str(internal_team_id)

    events = get_events(team_id=team_id)
    rsvps = get_rsvps(events=events)

    print_rsvp_tables(rsvps=rsvps)


main()
