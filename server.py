import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


def search_club_with_email_adress(info_email):
    club = [club for club in clubs if club['email'] == info_email]
    if club:
        club = club[0]
        error_message = ""
        return club, error_message
    else:
        club = []
        error_message = "Invalid email address !!"
    return club, error_message


@app.route('/showSummary', methods=['POST'])
def showSummary():
    info_email = request.form['email']
    club, error_message = search_club_with_email_adress(info_email)
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash(error_message)
        return render_template("index.html")


def control_the_number_of_points_for_a_club(found_club):
    number_of_points = found_club['points']
    return int(number_of_points) >= 1


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    number_of_points = control_the_number_of_points_for_a_club(found_club)
    found_competition = [c for c in competitions if c['name'] == competition][0]
    if number_of_points:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("You do not have enough points to register.")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display

@app.route('/show_clubs')
def show_clubs():
    return render_template('show_clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
