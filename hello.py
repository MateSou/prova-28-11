from wtforms import StringField, SubmitField, SelectField
import os
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask import Flask, render_template, flash,redirect,url_for
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'senhasecreta'


@app.route('/')
def index():
    return render_template('homepage.html')

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    disciplina = db.Column(db.String(64))

class CadastroProfessores(FlaskForm):
    new_teacher = StringField('Cadastre um novo professor',validators=[DataRequired()])
    choices = [('dswa5','DSWA5'),('gpsa5','GPSA5'),('ihca5','IHCA5'),('soda5','SODA5'),('pjia5','PJIA5'),('tcoa5','TCOA5')]
    disciplina = SelectField('Disciplina Associada', choices=choices)
    submit = SubmitField('Enviar')

@app.route('/professores',methods=['POST','GET'])
def teachers():
    form = CadastroProfessores()
    if form.validate_on_submit():
        user = Teacher.query.filter_by(username=form.new_teacher.data).first()
        if user is None:
            user = Teacher(username=form.new_teacher.data,disciplina=form.disciplina.data)
            db.session.add(user)
            db.session.commit()
            flash('Professor Cadastrado com sucesso!')
        else:
            flash('Este Professor já está cadastrado!')
        return redirect(url_for('teachers'))

    return render_template('professores.html',form=form, users=Teacher.query.all())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404error.html')
