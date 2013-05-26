import flask
import os.path
from beertistics import app, auth, user_service, visuals
from beertistics.exceptions import NoSuchUserException

@app.context_processor
def inject_visuals():
    # Adding the list of visuals to the context of all templates
    return dict(visuals=visuals.visuals)

@app.route('/')
def index():
    if auth.is_logged_in():
        return flask.render_template('index.html')
    else:
        return flask.render_template('login.html')

@app.route('/show-user')
@auth.requires_auth
def show_user():
    username = flask.request.args.get('username', None)
    if not username:
        return flask.redirect(flask.url_for('friend_list'))

    try:
        user = user_service.user_info_for(username)
        flask.session['shown_user'] = user
    except NoSuchUserException:
        flask.flash("Found no user with username '%s'." % username, 'error')
    return flask.redirect(flask.url_for("friend_list"))

@app.route('/test')
def test():
    return flask.render_template('test.html')

@app.route('/visual/<string:visual_id>')
@auth.requires_auth
def visual(visual_id):
    visual = visuals.get_visual(visual_id)
    template = os.path.join('visuals', visual['template_name'])
    return flask.render_template(template, next_url=visuals.get_next_url_for(visual_id))

@app.route('/about')
@auth.requires_auth
def about():
    return flask.render_template('about.html')

@app.route('/friend-list')
@auth.requires_auth
def friend_list():
    friends = user_service.friend_list_for('valle')
    return flask.render_template('friend-list.html', friends=friends)

@app.route('/checkins')
@auth.requires_auth
def checkins():
    return flask.render_template('checkins.html')
