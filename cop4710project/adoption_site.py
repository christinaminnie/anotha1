import os

from forms import AddForm, DelForm, AddRatingForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask,render_template,url_for,redirect



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey';

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

class VideoGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    release_date = db.Column(db.Text)
    compatibility = db.Column(db.Text)
    price = db.Column(db.Text)

    # many video games to many genres and many platforms
    genres = db.relationship('Genre', secondary='video_game_genre', backref='video_game_g')
    platforms = db.relationship('Platform', secondary='video_game_platform', backref='video_game_p')
    # many video games to one company
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref='video_game_c')

    def __init__(self, name, description, release_date, compatibility, price, company_id):
        self.name = name
        self.description = description
        self.release_date = release_date
        self.compatibility = compatibility
        self.price = price
        self.company_id = company_id

    def __repr__(self):
        return f"GAME: {self.name}\nDescription: {self.description}\nRelease Date: {self.release_date}\nCompatible " \
               f"With: {self.compatibility}\nPrice: {self.price}\nCompany_ID: {self.company_id}\n"
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numeric_rating = db.Column(db.Integer)
    verbal_rating = db.Column(db.Text)
    # many ratings to one video game
    video_game_id = db.Column(db.Integer, db.ForeignKey('video_game.id'))
    video_game = db.relationship('VideoGame', backref='rating')

    def __init__(self, numeric_rating, verbal_rating, video_game_id):
        self.numeric_rating = numeric_rating
        self.verbal_rating = verbal_rating
        self.video_game_id = video_game_id

    def __repr__(self):
        return f"Video Game ID: {self.video_game_id}, Numeric Rating: {self.numeric_rating}, Verbal Rating: {self.verbal_rating}"


video_game_genre = db.Table('video_game_genre',
                            db.Column('video_game_id', db.Integer, db.ForeignKey('video_game.id')),
                            db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
                            )

video_game_platform = db.Table('video_game_platform',
                               db.Column('video_game_id', db.Integer, db.ForeignKey('video_game.id')),
                               db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'))
                               )



class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"GENRE ......."

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    platform_device = db.Column(db.Text)
    version = db.Column(db.Integer)
    manufacturer = db.Column(db.Text)

    def __init__(self, name, platform_device, version, manufacturer):
        self.name = name
        self.platform_device = platform_device
        self.version = version
        self.manufacturer = manufacturer

    def __repr__(self):
        return f"Platform ... "

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)
    revenue = db.Column(db.Text)

    def __init__(self, name, location, revenue):
        self.name = name
        self.location = location
        self.revenue = revenue

    def __repr__(self):
        return f"name = {self.name}, location = {self.location}, revenue = {self.revenue}"





with app.app_context():
    db.create_all()

    with open('output.txt', 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            name = lines[i].strip()
            release_date = lines[i + 1].strip()
            price = lines[i + 2].strip()

            # Check if a video game with the same name already exists in the database
            existing_game = VideoGame.query.filter_by(name=name).first()
            if not existing_game:
                # If not, add the new game to the database
                game = VideoGame(name=name, release_date=release_date, price=price,description=None,compatibility=None,company_id=None)
                db.session.add(game)

    db.session.commit()

    nickie = gam






# gta = VideoGame('GTA', 'shooting game', '3/30/2001', 'Xbox', '6000')
    #rating1 = Rating(5, 'is amazing', 500)

   # db.session.add(rating1)
   # db.session.add(gta)


    #db.session.commit()

   # print(gta)
  #  print(rating1)

##############


############################################

# VIEWS WITH FORMS

##########################################

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/add', methods=['GET', 'POST'])
def add_game():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        release_date = form.release_date.data
        compatibility = form.compatibility.data
        price = form.price.data

        # Add new videogame to database
        new_game = VideoGame(name, description, release_date, compatibility, price)
        db.session.add(new_game)
        db.session.commit()

        return redirect(url_for('list_game'))

    return render_template('add.html', form=form)


@app.route('/list')
def list_game():
    # Grab a list of games from database.
    videogames = VideoGame.query.all()
    return render_template('list.html', videogames=videogames)


@app.route('/delete', methods=['GET', 'POST'])
def del_game():
    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        game = VideoGame.query.get(id)
        db.session.delete(game)
        db.session.commit()

        return redirect(url_for('list_game'))
    return render_template('delete.html', form=form)


@app.route('/addrating', methods=['GET', 'POST'])
def add_rating():
    form = AddRatingForm()

    if form.validate_on_submit():
        numericRating = form.numericRating.data
        verbalRating = form.verbalRating.data

        # Add new rating to database
        new_rating = Rating(numericRating, verbalRating, game_id=None)
        db.session.add(new_rating)
        db.session.commit()

        return redirect(url_for('list_ratings'))

    return render_template('rating.html', form=form)


@app.route('/listratings')
def list_ratings():
    ratings = Rating.query.all()
    return render_template('ratinglist.html', ratings=ratings)



if __name__ == '__main__':
    app.run(debug=True)

