from flask import Blueprint
from flask import render_template, request, url_for, redirect

from oop.car import Car

app = Blueprint('html_page', __name__)


# Flask maps HTTP requests to Python functions.
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('homePageTemplate.html')


@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        car_dict = {}
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        fuel = request.form['fuel']
        engine = request.form['engine']
        plate = request.form['plate']
        minKm = request.form['min_km']
        maxKm = request.form['max_km']
        minPrice = request.form['min_price']
        maxPrice = request.form['max_price']

        if model:
            car_dict['model'] = model
        if brand:
            car_dict['brand'] = brand
        if year:
            car_dict['year'] = int(year)
        if fuel:
            car_dict['fuel'] = fuel
        if engine:
            car_dict['engine'] = engine
        if plate:
            car_dict['plate'] = plate

        km_dict = {}
        if minKm:
            km_dict['$gte'] = int(minKm)
        if maxKm:
            km_dict['$lte'] = int(maxKm)

        if km_dict:
            car_dict['km'] = km_dict

        price_dict = {}
        if minPrice:
            price_dict['$gte'] = int(minPrice)
        if maxPrice:
            price_dict['$lte'] = int(maxPrice)

        if price_dict:
            car_dict['price'] = price_dict

        res = Car().readByDict(car_dict)

        cars = []
        for car in res:
            cars.append(car)

        car_dict['min_km'] = minKm
        car_dict['max_km'] = maxKm
        return render_template('showCarsTemplate.html', cars=cars, len=len(cars), search=car_dict)
    return render_template('showCarsTemplate.html', cars=[], len=0, search=[])


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        plate = request.form['plate']
        Car().delete(plate)

    return redirect('/register')


@app.route('/profile/<plate>', methods=['GET', 'POST'])
def profile(plate):
    car = Car().readPlate(plate)
    if car:
        return render_template('updateCarTemplate.html', car=car)
    return redirect('/register')


@app.route('/update', methods=['POST'])
def update():
    car = Car()
    car.plate = request.form['plate']
    car.brand = request.form['brand']
    car.model = request.form['model']
    car.year = request.form['year']
    car.fuel = request.form['fuel']
    car.km = request.form['km']
    car.engine = request.form['engine']
    car.sold = request.form['sold']
    car.price = request.form['price']
    car.update()
    redir = '/profile/' + str(car.plate)
    return redirect(redir)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        car = Car()
        car.plate = request.form['plate']
        car.brand = request.form['brand']
        car.model = request.form['model']
        car.year = request.form['year']
        car.fuel = request.form['fuel']
        car.km = request.form['km']
        car.engine = request.form['engine']
        car.sold = request.form['sold']
        car.price = request.form['price']
        car.create()

        redir = '/profile/' + str(car.plate)
        return redirect(redir)
    return render_template('registerCarTemplate.html')
