from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=150)

    # Create a toString method for object string representation
    def __str__(self):
        return str(self.name) + ": " + str(self.description)

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    dealer_id = models.IntegerField(null=False)
    TYPE_CHOICES = [
        ('sedan', 'SEDAN'),
        ('suv', 'SUV'),
        ('wagon', 'WAGON')
    ]
    type = models.CharField(null=False, max_length=30, choices=TYPE_CHOICES, default=TYPE_CHOICES[0])
    year = models.DateField(null=False)

    # Create a toString method for object string representation
    def __str__(self):
        return str(self.make) + " " + str(self.name) + " " + str(self.dealer_id) + " " + str(self.type) + " " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
