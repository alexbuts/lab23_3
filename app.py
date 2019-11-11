from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms.user_form import HolidayForm, PresentsForm, ClientForm, PresentsForm1, HolidayForm1, ClientForm1,CountryForm

import plotly.graph_objs as go
import plotly
import json


import plotly
import json
from flask_sqlalchemy import SQLAlchemy
import plotly.graph_objs as go
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = 'key'
ENV = 'prod'


if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vlad16tank@localhost/buts'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://niunqpaxcbscjt:ace936f17a6f1cfabd8820c906f08c41b6a2499f0f461e1a3a1c0bdc2826dbf7@ec2-107-20-168-237.compute-1.amazonaws.com:5432/d8lk089rqcbkk4'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class ormHoliday(db.Model):
    __tablename__ = 'Holiday'

    holiday_name = db.Column(db.String(20), primary_key=True)
    season_year = db.Column(db.String(20), nullable=False)
    clients_ = db.relationship('ormClient')
    a_ = db.relationship('ormHolidayCountry')


class ormClient(db.Model):
    __tablename__ = 'Client'
    passport_num = db.Column(db.Integer, primary_key=True)
    holiday_name = db.Column(db.String(20),db.ForeignKey('Holiday.holiday_name') , nullable=False)
    present_name = db.Column(db.String(20),db.ForeignKey('Presents.present_name') ,nullable=False)
    name = db.Column(db.String(40))
    family_state = db.Column(db.String(30))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(40))




class ormPresents(db.Model):
    __tablename__ = 'Presents'

    present_name = db.Column(db.String(20), primary_key=True)
    store_name = db.Column(db.String(30))
    count_items = db.Column(db.Integer)

    clients__ = db.relationship('ormClient')

class ormCountry(db.Model):
    __tablename__ = 'Country'
    country_name = db.Column(db.String(20), primary_key=True)
    population = db.Column(db.Integer)
    goverment = db.Column(db.String(20))
    coordinates = db.Column(db.Integer)
    a_ = db.relationship('ormHolidayCountry')

class ormHolidayCountry(db.Model):
    __tablename__ = 'HolidayCountry'
    country_name = db.Column(db.String(20),db.ForeignKey('Country.country_name'), primary_key=True)
    holiday_name = db.Column(db.String(20),db.ForeignKey('Holiday.holiday_name'), primary_key=True)








#db.session.query(ormClient).delete()
#db.session.query(ormHoliday).delete()

#db.session.query(ormPresents).delete()

'''
Client1 = ormClient(passport_num = 101, age =21 ,name ='alex' ,family_state = 'nmarried',gender = 'male',present_name = 'Smartphone',holiday_name ='Christmas')
Client2 = ormClient(passport_num = 102, age = 54,name = 'valera',family_state = 'married',gender = 'male',present_name = 'Smartphone',holiday_name = 'Easter')
Client3 = ormClient(passport_num = 103, age =29 ,name = 'olga',family_state = 'married',gender = 'female',present_name = 'Flowers',holiday_name = 'Christmas')

Present1 =ormPresents(present_name = 'TV', count_items=5, store_name='Comfy')
Present2 =ormPresents(present_name='Smartphone', count_items=4, store_name='Comfy')
Present3 =ormPresents(present_name='Flowers', count_items=3, store_name='Silpo')

Holiday1 = ormHoliday(holiday_name = 'Christmas', season_year = 'winter')
Holiday2 = ormHoliday(holiday_name = 'Easter', season_year ='spring' )
Holiday3 = ormHoliday(holiday_name = 'Womensday', season_year = 'spring')


Holiday1.clients_.append(Client1)
Holiday1.clients_.append(Client3)

Holiday2.clients_.append(Client2)

Present2.clients__.append(Client1)
Present2.clients__.append(Client2)
Present3.clients__.append(Client3)

db.session.add_all([Client1,Client2,Client3])
db.session.add_all([Present1,Present2,Present3])
db.session.add_all([Holiday1,Holiday2,Holiday3])

db.session.commit()
'''

#main page
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


#set
@app.route('/set', methods=['GET'])
def set():
    db.session.query(ormCountry).delete()
    C1 = ormCountry(country_name="Italy",population=30,goverment='prezident',coordinates=2)
    C2 = ormCountry(country_name="Spain",population=30,goverment='prezident',coordinates=2)
    C3 = ormCountry(country_name="Russia",population=30,goverment='prezident',coordinates=2)

    db.session.add_all([C1, C2, C3])
    db.session.commit()

    return redirect('/show')



#show
@app.route('/show', methods=['GET'])
def show():

    result = db.session.query(ormCountry).all()

    return render_template('country.html', country = result)


#insert
@app.route('/insert', methods=['GET','POST'])
def insert():

    form = CountryForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('country_form.html', form=form, form_name="New country", action="insert")
        else:
            new_user= ormCountry(
                country_name=form.country_name.data,
                population=form.population.data,
                goverment = form.goverment.data,
                coordinates = form.coordinates.data
                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('show'))

    return render_template('country_form.html', form=form, form_name="New country", action="insert")



#hilday pages
@app.route('/holiday', methods=['GET'])
def holiday():

    result = db.session.query(ormHoliday).all()

    return render_template('holidays.html', holidays = result)


@app.route('/new_holiday', methods=['GET','POST'])
def new_holiday():

    form = HolidayForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('holiday_form.html', form=form, form_name="New holiday", action="new_holiday")
        else:
            new_user= ormHoliday(
                holiday_name=form.holiday_name.data,
                season_year=form.season_year.data
                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('holiday'))

    return render_template('holiday_form.html', form=form, form_name="New holiday", action="new_holiday")

@app.route('/edit_holiday/<string:x>', methods=['GET','POST'])
def edit_holiday(x):

    form = HolidayForm1()
    user = db.session.query(ormHoliday).filter(ormHoliday.holiday_name == x).one()

    if request.method == 'GET':



        # fill form and send to user

        form.season_year.data = user.season_year
        return render_template('holiday_form1.html', form=form, form_name="Edit holiday")

    else:

        if form.validate() == False:
            return render_template('holiday_form1.html', form=form, form_name="Edit holiday")
        else:
            user.season_year = form.season_year.data

            db.session.commit()

            return redirect(url_for('holiday'))

@app.route('/delete_holiday/<string:x>', methods=['GET'])
def delete_holiday(x):
    result = db.session.query(ormHoliday).filter(ormHoliday.holiday_name ==x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('sex.html')


#client
@app.route('/clients', methods=['GET'])
def clients():

    result = db.session.query(ormClient).all()

    return render_template('clients.html', clients = result)


@app.route('/new_clients', methods=['GET','POST'])
def new_clients():

    form = ClientForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('client_form.html', form=form, form_name="New client", action="new_clients")
        else:
            new_user= ormClient(
                passport_num=form.passport_num.data,
                holiday_name=form.holiday_name.data,
                present_name=form.present_name.data,
                name=form.name.data,
                family_state=form.family_state.data,
                age=form.age.data,
                gender=form.gender.data
                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('clients'))

    return render_template('client_form.html', form=form, form_name="New client", action="new_clients")

@app.route('/edit_clients/<int:x>', methods=['GET','POST'])
def edit_clients(x):

    form = ClientForm1()

    user = db.session.query(ormClient).filter(ormClient.passport_num == x).one()

    if request.method == 'GET':

        #user_id =request.args.get('passport_num')


        # fill form and send to user
        #form.passport_num.data = user.passport_num
        form.holiday_name.data = user.holiday_name
        form.present_name.data =  user.present_name
        form.name.data = user.name
        form.family_state.data = user.family_state
        form.age.data = user.age
        form.gender.data = user.gender
        return render_template('client_form1.html', form=form, form_name="Edit client")


    else:

        if form.validate() == False:
            return render_template('client_form1.html', form=form, form_name="Edit client")
        else:

            # find user

            # update fields from form data
            user.holiday_name = form.holiday_name.data
            user.present_name = form.present_name.data
            user.name = form.name.data
            user.family_state = form.family_state.data
            user.age = form.age.data
            user.gender = form.gender.data
            db.session.commit()

            return redirect(url_for('clients'))

@app.route('/delete_clients/<int:x>', methods=['GET'])
def delete_clients(x):

    user_id = request.form['passport_num']


    result = db.session.query(ormClient).filter(ormClient.passport_num ==x).one()

    db.session.delete(result)
    db.session.commit()


    return render_template('sex.html')


#presents pages
@app.route('/presents', methods=['GET'])
def presents():

    result = db.session.query(ormPresents).all()

    return render_template('presents.html', presents = result)


@app.route('/new_presents', methods=['GET','POST'])
def new_presents():

    form = PresentsForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('presents_form.html', form=form, form_name="New user", action="new_presents")
        else:
            new_user= ormPresents(
                present_name=form.present_name.data,
                count_items=form.count_items.data,
                store_name=form.store_name.data,

                            )
            db.session.add(new_user)
            db.session.commit()


            return redirect(url_for('presents'))

    return render_template('presents_form.html', form=form, form_name="New user", action="new_presents")

@app.route('/edit_presents/<string:x>', methods=['GET','POST'])
def edit_presents(x):

    form = PresentsForm1()
    user = db.session.query(ormPresents).filter(ormPresents.present_name == x).one()

    if request.method == 'GET':

        #user_id =request.args.get('present_name')
        #db = PostgreDB()
        #user = db.sqlalchemy_session.query(ormPresents).filter(ormPresents.present_name == x).one()

        # fill form and send to user
        form.count_items.data = user.count_items
        form.store_name.data = user.store_name


        return render_template('presents_form1.html', form=form, form_name="Edit present")


    elif request.method == 'POST':

        if form.validate() == False:
            return render_template('presents_form1.html', form=form, form_name="Edit present")
        else:
            #db = PostgreDB()
            # find user
            #user = db.sqlalchemy_session.query(ormPresents).filter(ormPresents.present_name == form.present_name.data).one()

            # update fields from form data
            user.count_items = form.count_items.data
            user.store_name = form.store_name.data
            db.session.commit()

            return redirect('/presents')

@app.route('/delete_presents/<string:x>', methods=['GET'])
def delete_presents(x):

    #user_id = request.form['present_name']


    result = db.session.query(ormPresents).filter(ormPresents.present_name ==x).one()

    db.session.delete(result)
    db.session.commit()

    return render_template('sex.html')

@app.route('/plotly', methods=['GET', 'POST'])
def plotly():
    query1 = (
        db.session.query(
            ormPresents.present_name,
            func.count(ormClient.passport_num).label('salary')
    ).
            outerjoin(ormClient).
            group_by(ormPresents.present_name)
    ).all()

    query2 = (
                  db.session.query(
                      ormHoliday.holiday_name,
                      func.avg(ormClient.age).label('age')
              ).
              outerjoin(ormClient).
              group_by(ormHoliday.holiday_name)
              ).all()
    query3 = (
        db.session.query(
            ormCountry.country_name,
            ormCountry.population.label('population')
        )
    ).all()


    names, skill_counts = zip(*query3)
    bar = go.Bar(
        x=names,
        y=skill_counts
    )

    skills, user_count = zip(*query2)
    pie = go.Pie(
        labels=skills,
        values=user_count
    )




    data = {
                "bar":[bar],
                "pie":[pie]
           }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)





#     =================================================================================================

if __name__ == '__main__':
    app.run(debug=True)