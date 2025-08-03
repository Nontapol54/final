from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research.db'
db = SQLAlchemy(app)

class Research(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)

@app.route('/')
def index():
    student = {'name': 'นนทพล ชมจันทร์', 'id': '67130202'}
    return render_template('index.html', student=student)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/myresearch')
def myresearch():
    researches = Research.query.all()
    return render_template('myresearch.html', researches=researches)

@app.route('/reference', methods=['GET', 'POST'])
def reference():
    if request.method == 'POST':
        form_id = request.form.get('id')
        title = request.form['title']
        link = request.form['link']

        if form_id:
            res = Research.query.get(form_id)
            if res:
                res.title = title
                res.link = link
        else:
            new_res = Research(title=title, link=link)
            db.session.add(new_res)

        db.session.commit()
        return redirect(url_for('reference'))

    edit = None
    edit_id = request.args.get('edit_id')
    if edit_id:
        edit = Research.query.get(edit_id)

    researches = Research.query.all()
    return render_template('reference.html', researches=researches, edit=edit)

@app.route('/delete/<int:id>')
def delete(id):
    res = Research.query.get_or_404(id)
    db.session.delete(res)
    db.session.commit()
    return redirect(url_for('reference'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)