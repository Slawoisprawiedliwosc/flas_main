from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import joblib
import numpy as np
from math import ceil

XGboost_model = joblib.load(r"model/XGBoost.joblib")
enc = joblib.load(r"model/encoder.joblib")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    data_create = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        brand = request.form["modeln"]
        model = request.form["brandn"]
        capacity = request.form["capacity"]
        course = request.form["course"]
        year = request.form["year"]
        is_new = 0
        #enc_cat_lst = [enc for model in enc.categories_ for enc in model]
        sample = np.array([brand, model, capacity, course, year, is_new])
        cat = sample[:2]
        cat = cat.reshape(1, 2)
        sample_encoded = enc.transform(cat).toarray()
        sample_numerical = sample[2:].reshape(1, 4)
        full_sample = np.concatenate((sample_numerical, sample_encoded), axis=1)
        m_price = XGboost_model.predict(full_sample)
        price = ceil(m_price[0])
        return render_template('data.html', motorbike=pricegit)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)