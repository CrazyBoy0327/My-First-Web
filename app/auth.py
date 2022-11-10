import functools
from flask import Blueprint, g, redirect, render_template, request, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
        

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM users WHERE username = %s OR email = %s', (username,email,)
        )
        selected = c.fetchone()
        if not username:
            error = 'Username is required'

        if not password:
            error = 'Password is required'

        if not email:
            error = 'Email is required'

        if email[-4:] != '.com':
            error = 'Wrong email'

        if '@' not in email:
            error = 'Wrong email'

        else:
            count = 0
            for i in email:
                if i == '@':
                    count += 1
            if count != 1:
                error = 'Wrong email'
            
        if selected is not None:
            if username == selected['username']:
                error = 'Usuername {} already exist'.format(username)
            if email == selected['email']:
                error = 'This email already exist'
        if error is None:
            c.execute(
                'INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
                (username, generate_password_hash(password), email)
            )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM users WHERE username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Username or Password wrong'
        
        elif not check_password_hash(user['password'], password):
            error = 'Username or Password wrong'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('comment.index'))
        
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT * FROM users WHERE id = %s', (user_id,)
        )
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.register'))

        return view(**kwargs)
        
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.route('/delete')
def delete_user():
    session.clear()
    db, c = get_db()
    c.execute(
        'DELETE FROM users '
        'WHERE username = %s',
        (g.user['username'],)
    )
    db.commit()
    return redirect(url_for('auth.register'))

