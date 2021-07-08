from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///fee.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Fee(db.Model):
    __searchable__ = ['title', 'fee']
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    fee = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} - {self.fee}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        fee = request.form['fee']
        fee = Fee(title=title, desc=desc, fee=fee)
        db.session.add(fee)
        db.session.commit()

    allfee = Fee.query.all()
    return render_template('index.html', allfee=allfee)

@app.route('/show')
def products():
    allfee = Fee.query.all()
    print(allfee)
    return render_template('show.html', allfee=allfee)

@app.route('/search', methods=['GET', 'POST'])
def search(fee):
        allfee = Fee.query.filter_by(fee=fee).first()
        print(allfee)
        return render_template('search.html', fee=fee)


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        feestatus = request.form['fee']
        fee = Fee.query.filter_by(sno=sno).first()
        fee.title=title
        fee.desc=desc
        fee.fee=feestatus
        db.session.add(fee)
        db.session.commit()
        return redirect("/")

    fee = Fee.query.filter_by(sno=sno).first()
    return render_template('update.html', fee=fee)

@app.route('/delete/<int:sno>')
def delete(sno):
    fee = Fee.query.filter_by(sno=sno).first()
    db.session.delete(fee)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)