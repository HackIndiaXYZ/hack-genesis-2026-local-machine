from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    secret = db.Column(db.String(120), nullable=False)

def init_db():
    db.create_all()
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        new_admin = User(username='admin', secret='FLAG{HACKED_BY_AGENT}')
        db.session.add(new_admin)
        db.session.commit()

@app.route('/')
def index():
    query = request.args.get('q', '')
    html = '''
        <h2>SecureApp Search</h2>
        <form method="GET">
            <input type="text" name="q" placeholder="Search users...">
            <input type="submit" value="Search">
        </form>
        <h3>Results:</h3>
        <ul>
    '''
    if query:
        results = User.query.filter(User.username.like(f'%{query}%')).all()
        for r in results:
            html += f"<li>User: {r.username}</li>"
    html += '</ul>'
    return render_template_string(html)

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=False)