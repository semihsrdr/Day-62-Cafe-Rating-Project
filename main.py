from flask import Flask, render_template,redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,URLField,SelectField
from wtforms.validators import DataRequired
import csv,pandas

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):

    cafe = StringField('Cafe name', validators=[DataRequired()])
    url = URLField('Url', validators=[DataRequired()])
    open_time = StringField('Open Time', validators=[DataRequired()])
    close_Time = StringField('Close ,Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee',choices=["☕","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi',choices=["💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"], validators=[DataRequired()])
    power_outlet = SelectField('Power Outlet',choices=["🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌️☕
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=["POST","GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        cafe_name=form.cafe.data
        url_text=form.url.data
        open_hour=form.open_time.data
        close_hour=form.close_Time.data
        coffee=form.coffee_rating.data
        wifi=form.wifi_rating.data
        power=form.power_outlet.data

        cafe = {
            "Cafe Name": [cafe_name],
            "Location": [url_text],
            "Open": [open_hour],
            "Close": [close_hour],
            "Coffee": [coffee],
            "Wifi": [wifi],
            "Power": [power]
        }

        new_cafe=pandas.DataFrame(cafe)
        new_cafe.to_csv('cafe-data.csv',mode='a',header=False,index=False)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True,host="localhost",port=8000)
