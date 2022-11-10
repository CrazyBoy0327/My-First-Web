from flask import Blueprint, g, redirect, render_template, request, url_for, flash
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp=Blueprint('comment', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db, c = get_db()
    c.execute(
        'SELECT c.id, c.opinion, u.username, c.created_at '
        'FROM comments c JOIN users u ON c.created_by = u.id '
        'WHERE c.created_by = %s ORDER BY created_at DESC',
        (g.user['id'],)
    )
    user_comment = c.fetchall()

    return render_template('comment/index.html', user_comments = user_comment)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        new_comment = request.form['comment']
        db, c = get_db()
        error= None

        if not new_comment:
            error = 'Comment is required'
        
        if error is not None:
            flash(error)
        else:
            c.execute(
                'INSERT INTO comments (created_by, opinion) '
                'VALUES (%s, %s)', 
                (g.user['id'], new_comment)
            )
            db.commit()
            return redirect(url_for('comment.index'))

    return render_template('comment/create.html')
    

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        update_comment = request.form['update']
        db, c = get_db()
        error = None
        
        if update_comment is None:
            error = 'Update is required'
        
        if error is not None:
            flash(error)
        else:
            c.execute(
                'UPDATE comments SET opinion=%s '
                'WHERE id=%s AND created_by=%s',
                (update_comment, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('comment.index'))
    return render_template('comment/update.html')

@bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'DELETE FROM comments '
        'WHERE id=%s AND created_by = %s',
        (id, g.user['id'])
    )
    db.commit()
    return redirect(url_for('comment.index'))