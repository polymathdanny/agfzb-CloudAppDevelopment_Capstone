from django.db import models
from django.utils.timezone import now

car_types = (
    ('Sedan', u'Sedan'),
    ('SUV', u'SUV'),
    ('Wagon', u'Wagon'),
)

# Create your models here.
class CarMake(models.Model):
    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=200, choices=car_types,  null=True)
    year = models.DateField()

    def __str__(self):
        return self.name

class CarDealer(models.Model):
    def __init__(self, address, city, full_name, dealer_id, lat, long, short_name, state, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.dealer_id = dealer_id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.state = state
        self.st = st
        self.zip = zip

    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    full_name = models.CharField(max_length=200, null=True)
    dealer_id = models.IntegerField(default=0)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)
    short_name = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    st = models.CharField(max_length=200, null=True)
    zip = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name

class DealerReview(models.Model):
    def __init__(self, dealer_id, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, review_id):
        self.dealer_id = dealer_id
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.review_id = review_id

    dealer_id = models.ForeignKey(CarDealer, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    purchase = models.BooleanField(null=True)
    review = models.CharField(max_length=1000, null=True)
    purchase_date = models.DateField(null=True)
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    car_model = models.ForeignKey(CarModel, null=True, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=200, null=True)
    review_id = models.IntegerField()

    def __str__(self):
        return "Review name: " + self.dealer_id + ": " + self.car_year + " " + self.car_make

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# <HINT> Create a plain Python class `DealerReview` to hold review data

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
