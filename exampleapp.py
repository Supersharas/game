#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort, redirect, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from sqlalchemy.sql import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pergale1@localhost:5432/fyyur'


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.Enum('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
      'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
      'MT','NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR',
      'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
      'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())
    genres = db.relationship('VenueGenre', backref='venue', cascade="all, delete-orphan", lazy=True)
    shows = db.relationship('Show', backref='venue', cascade="all, delete-orphan", lazy=True)
    

class VenueGenre(db.Model):
    __tablename__ = 'Venuegenre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum('Alternative', 'Blues', 'Classical', 'Country',
      'Electronic', 'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental',
      'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae', 'Rock n Roll',
      'Soul', 'Other'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.Enum('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
      'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME',
      'MT','NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR',
      'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
      'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.relationship('ArtistGenre', backref='artist', cascade="all, delete-orphan", lazy=True)
    shows = db.relationship('Show', backref='artist', cascade="all, delete-orphan", lazy=True)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String())

class ArtistGenre(db.Model):
    __tablename__ = 'Artistgenre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum('Alternative', 'Blues', 'Classical', 'Country',
      'Electronic', 'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental',
      'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae', 'Rock n Roll',
      'Soul', 'Other'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():

  data = []
  areas = db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).order_by('state').all()
  for area in areas:
    data.append({'city': area[0],
      'state': area[1],
      'venues': Venue.query.filter_by(city=area[0]).all()})

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_string = request.form.get("search_term")
  search_var = "%" + search_string + "%"
  venues = Venue.query.filter(Venue.name.ilike(search_var)).all()
  response_len = len(venues)
  response = {'data': venues,
    'count': response_len}
  return render_template('pages/search_venues.html', results=response , search_term=search_string)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data = Venue.query.get(venue_id)
  past_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time <= datetime.now()).all()
  upcoming_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time >= datetime.now()).all()

  for show in past_shows:
    show.start_time = str(show.start_time)
  data.past_shows = past_shows
  data.past_shows_count = len(past_shows)
  for show in upcoming_shows:
    show.start_time = str(show.start_time)
  data.upcoming_shows = upcoming_shows
  data.upcoming_shows_count = len(upcoming_shows)

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    v_name = request.form.get('name')
    v_address = request.form.get('address')
    v_city = request.form.get('city')
    v_state = request.form.get('state')
    v_phone = request.form.get('phone')
    v_website = request.form.get('website')
    v_facebook_link = request.form.get('facebook_link')
    v_image_link = request.form.get('image_link')
    v_genres = request.form.getlist('genres')
    v_seeking_description = request.form.get('seeking_description')
    if v_seeking_description:
      v_seeking_talent = True
    else:
      v_seeking_talent = False
    venue = Venue(name=v_name, address=v_address, city=v_city, state=v_state, phone=v_phone, website=v_website, 
      facebook_link=v_facebook_link, seeking_talent=v_seeking_talent, seeking_description = v_seeking_description,
      image_link=v_image_link)
  
    db.session.add(venue)
    db.session.commit()
    for gen in v_genres:
      genre = VenueGenre(name=gen, venue_id=venue.id)
      db.session.add(genre)

    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return redirect(url_for('index'))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue could not be deleted.')
    return jsonify({'success': False})
  else:
    flash('Venue was successfully deleted!')
    return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_string = request.form.get("search_term")
  search_var = "%" + search_string + "%"
  artists = Artist.query.filter(Artist.name.ilike(search_var)).all()
  response_len = len(artists)
  response = {'data': artists,
    'count': response_len}
  return render_template('pages/search_artists.html', results=response , search_term=search_string)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  data = Artist.query.get(artist_id)
  past_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time <= datetime.now()).all()
  upcoming_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time >= datetime.now()).all()

  for show in past_shows:
    show.start_time = str(show.start_time)
  data.past_shows = past_shows
  data.past_shows_count = len(past_shows)
  for show in upcoming_shows:
    show.start_time = str(show.start_time)
  data.upcoming_shows = upcoming_shows
  data.upcoming_shows_count = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  try:
    artist = Artist.query.get(artist_id)

    artist.name = request.form.get('name')
    artist.address = request.form.get('address')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.website = request.form.get('website')
    artist.facebook_link = request.form.get('facebook_link')
    artist.image_link = request.form.get('image_link')
    artist.seeking_description = request.form.get('seeking_description')
    if artist.seeking_description:
      artist.seeking_talent = True
    else:
      seeking_talent = False
    new_genres = []
    for gen in request.form.getlist('genres'):
      new_genres.append(ArtistGenre(name=gen, artist_id=artist_id))
    artist.genres = new_genres
    db.session.commit()


  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return redirect(url_for('index'))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)

    venue.name = request.form.get('name')
    venue.address = request.form.get('address')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.phone = request.form.get('phone')
    venue.website = request.form.get('website')
    venue.facebook_link = request.form.get('facebook_link')
    venue.image_link = request.form.get('image_link')
    venue.seeking_description = request.form.get('seeking_description')
    if venue.seeking_description:
      venue.seeking_talent = True
    else:
      seeking_talent = False

    new_genres = []
    for gen in request.form.getlist('genres'):
      new_genres.append(VenueGenre(name=gen, venue_id=venue_id))

    venue.genres = new_genres
    db.session.commit()

  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return redirect(url_for('index'))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    a_name = request.form.get('name')
    a_city = request.form.get('city')
    a_state = request.form.get('state')
    a_phone = request.form.get('phone')
    a_facebook_link = request.form.get('facebook_link')
    a_genre = request.form.getlist('genres')
    a_website = request.form.get('website')
    a_image_link = request.form.get('image_link')
    a_seeking_description = request.form.get('seeking_description')
    if a_seeking_description:
      a_seeking_venue = True
    else:
      a_seeking_venue = False
    artist = Artist(name=a_name, city=a_city, state=a_state, phone=a_phone, seeking_venue=a_seeking_venue, 
      seeking_description=a_seeking_description, facebook_link=a_facebook_link, image_link=a_image_link,
      website=a_website)
    db.session.add(artist)
    db.session.commit()
    for gen in a_genre:
      genre = ArtistGenre(name=gen, artist_id=artist.id)
      db.session.add(genre)
    
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return redirect(url_for('index'))

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  error = False
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Artist could not be deleted.')
    return jsonify({'success': False})
  else:
    flash('Artist was successfully deleted!')
    return jsonify({'success': True})


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  data = Show.query.all()

  for d in data:
    d.start_time = str(d.start_time)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    artist = request.form.get('artist_id')
    venue = request.form.get('venue_id')
    start = request.form.get('start_time')
    
    show = Show(artist_id=artist, venue_id=venue, start_time=start)
  
    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('An error occurred. Show could not be listed.')
  else:
    flash('Show was successfully listed!')
  return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
