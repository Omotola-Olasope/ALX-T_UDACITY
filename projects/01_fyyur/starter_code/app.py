#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from email.policy import default
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
import collections
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
collections.Callable = collections.abc.Callable
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text(), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text(), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

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
  all_venues = db.session.query(venues.city,venues.state).group_by(venues.state,venues.city).all()
  data = []
  for area in all_venues:
      venue_areas = venues.query.filter_by(state=area.state).filter_by(city=area.city).all()
      venue_data = []
      for venue in venue_areas:
        venue_data.append({
        "id": venue.id,
        "name": venue.name
      })
      data.append({
      "city": area.city,
      "state": area.state, 
      "venues": venue_data
    })
  return render_template('pages/venues.html', areas=data)
    # TODO: replace with real venues data.
    #      num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    
@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  search_term = request.form.get('search_term')
  venue_search = "%{}%".format(search_term)
  searchResults = venues.query.filter(venues.name.ilike(venue_search)).all()

  venueResult={
    "count": len(searchResults),
    "data": []
  }
  for venue in searchResults:
    venueResult['data'].append({
      "id": venues.id,
      "name": venues.name,
      })

  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  return render_template('pages/search_venues.html', results=venueResult, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  givenVenue = venues.query.get(venue_id)

  data = {
    "id": givenVenue.id,
    "name": givenVenue.name,
    "genres": givenVenue.genres,
    "address": givenVenue.address,
    "city": givenVenue.city,
    "state": givenVenue.state,
    "phone": givenVenue.phone,
    "website_link": givenVenue.website,
    "facebook_link": givenVenue.facebook_link,
    "seeking_talent": givenVenue.seeking_talent,
    "seeking_description": givenVenue.seeking_description,
    "image_link": givenVenue.image_link
  }

  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  new_venue = venues()
  new_venue.name = request.form['name']
  new_venue.city = request.form['city']
  new_venue.state = request.form['state']
  new_venue.address = request.form['address']
  new_venue.phone = request.form['phone']
  new_venue.genres = request.form['genres']
  new_venue.facebook_link = request.form['facebook_link']
  new_venue.image_link = request.form['image_link']
  new_venue.website = request.form['website_link']
  new_venue.seeking_talent = request.form['seeking_talent']
  new_venue.seeking_description = request.form['seeking_description']
        
  try:
    
    db.session.add(new_venue)
    db.session.commit()
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.

  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()
  
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = venues.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    
  except:
    db.session.rollback()
    
  finally:
    db.session.close()

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  
  artist = artists.query.order_by(artists.id).all()
  

  # TODO: replace with real data returned from querying the database
  
  return render_template('pages/artists.html', artists=artist)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  search_term = request.form.get('search_term')
  artist_search = "%{}%".format(search_term)
  searchResults = artists.query.filter(artists.name.ilike(artist_search)).all()

  artistResult={
    "count": len(searchResults),
    "data": []
  }
  for artist in searchResults:
    artistResult['data'].append({
      "id": artists.id,
      "name": artists.name,
      })

  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  return render_template('pages/search_artists.html', results=artistResult, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  givenArtist = artists.query.get(artist_id)

  data = {
    "id": givenArtist.id,
    "name": givenArtist.name,
    "genres": givenArtist.genres,
    "city": givenArtist.city,
    "state": givenArtist.state,
    "phone": givenArtist.phone,
    "website_link": givenArtist.website,
    "facebook_link": givenArtist.facebook_link,
    "seeking_venue": givenArtist.seeking_venue,
    "seeking_description": givenArtist.seeking_description,
    "image_link": givenArtist.image_link
  }  



  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  artist = artists.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres.split(',')
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = artists.query.get(artist_id)
  
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  genres = request.form['genres']
  facebook_link = request.form['facebook_link']
  image_link = request.form['image_link']
  website = request.form['website_link']
  seeking_venue = request.form['seeking_venue']
  seeking_description = request.form['seeking_description']
  
  artist.name = name
  artist.city = city
  artist.state = state
  artist.phone = phone
  artist.genres = genres
  artist.facebook_link = facebook_link
  artist.image_link = image_link
  artist.website = website
  artist.seeking_venue = seeking_venue
  artist.seeking_description = seeking_description

  try:
    db.session.add
    db.session.commit()
    flash("Artist {} is updated successfully".format(artists.name))
  except:
    db.session.rollback()
    flash("Artist {} isn't updated successfully".format(artists.name))
  finally:
    db.session.close()
  
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  venue = venues.query.get(venue_id)
  
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres.split(',')
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website_link.data = venue.website
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description


  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = venues.query.get(venue_id)
  
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  genres = request.form['genres']
  facebook_link = request.form['facebook_link']
  image_link = request.form['image_link']
  website = request.form['website_link']
  seeking_talent = request.form['seeking_talent']
  seeking_description = request.form['seeking_description']
  
  venue.name = name
  venue.city = city
  venue.state = state
  venue.address = address
  venue.phone = phone
  venue.genres = genres
  venue.facebook_link = facebook_link
  venue.image_link = image_link
  venue.website = website
  venue.seeking_talent = seeking_talent
  venue.seeking_description = seeking_description

  try:
    db.session.add
    db.session.commit()
    flash("Venue {} is updated successfully".format(venues.name))
  except:
    db.session.rollback()
    flash("Venue {} isn't updated successfully".format(venues.name))
  finally:
    db.session.close()
  
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  new_artist = artists()
  new_artist.name = request.form['name']
  new_artist.city = request.form['city']
  new_artist.state = request.form['state']
  new_artist.phone = request.form['phone']
  new_artist.genres = request.form['genres']
  new_artist.facebook_link = request.form['facebook_link']
  new_artist.image_link = request.form['image_link']
  new_artist.website = request.form['website_link']
  new_artist.seeking_venue = request.form['seeking_venue']
  new_artist.seeking_description = request.form['seeking_description']
 
    

  try:
    db.session.add(new_artist)
    db.session.commit()
  
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  
  finally:
    db.session.close()
  
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  
  Joins = db.session.query(shows).join(venues).join(artists).all()
  
  data = []
  for show in Joins: 
    data.append({
      "venue_id": shows.venue_id,
      "venue_name": shows.venue.name,
      "artist_id": shows.artist_id,
      "artist_name": shows.artists.name, 
      "artist_image_link": shows.artists.image_link,
      "start_time": str(shows.start_time)
    })

  # displays list of shows at /shows
  ## TODO: replace with real venues data.
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  try:
    newShow = shows()
    newShow.artist_id = request.form['artist_id']
    newShow.venue_id = request.form['venue_id']
    newShow.start_time = request.form['start_time']
    
    db.session.add(newShow)
    db.session.commit()
  
    flash('Show was successfully listed!')
  
  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  
  finally:
    db.session.close()
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

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
