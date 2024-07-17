from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class HouseListing(models.Model):
  address = models.CharField(max_length=255, null=True,
    blank=True,)
  city = models.CharField(max_length=255, null=True,
    blank=True,)
  state = models.CharField(max_length=255, null=True,
    blank=True,)
  zipcode = models.IntegerField(null=True,
    blank=True,)
  # add house details later, in the form
  created_at = models.DateTimeField(auto_now_add=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings') # one-to-many relationship

  current_year = timezone.now().year

  # Image field for the house picture
  HouseImage = models.ImageField(upload_to='house_images/', null=True, blank=True, verbose_name="House Image")

# ESSENTIAL FEATURES FOR PREDICTION
  BedroomAbvGr = models.IntegerField(
    validators=[MinValueValidator(0)],
    verbose_name="Bedrooms (above grade)",
    null=True,
    blank=True,
  )
  FullBath = models.IntegerField(
    validators=[MinValueValidator(0)],
    verbose_name="Full Bathrooms",
    null=True,
    blank=True,
  )
  HalfBath = models.IntegerField(
    validators=[MinValueValidator(0)],
    verbose_name="Half Bathrooms",
    null=True,
    blank=True,
  )
  BldgType = models.CharField(
    max_length=255,
    choices=[
      ('1Fam', 'Single-family'),
      ('2FmCon', 'Apartment building'),
      ('TwnhsE', 'Townhouse end unit'),
      ('TwnhsI', 'Townhouse inside unit')
    ],
    verbose_name="Building Type",
    null=True,
    blank=True,
  )
  GrLivArea = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Above Ground Living Area",
    help_text="Square footage of living area above grade"
  )
  GarageCars = models.IntegerField(
    validators=[MinValueValidator(0)],
    verbose_name="Garage Size (in cars)",
    null=True,
    blank=True,
  )
  YearBuilt = models.IntegerField(
    validators=[MaxValueValidator(current_year)],
    verbose_name="Year Built",
    null=True,
    blank=True,
  )
  Utilities = models.CharField(
    max_length=255,
    choices=[
      ('AllPub', 'All public utilities'),
      ('NoSewr', 'Electricity, Gas, and Water'),
      ('NoSeWa', 'Electricity and Gas/Water Only'),
      ('ELO', 'Electricity only')
    ],
    verbose_name="Utilities",
    null=True,
    blank=True,
    )
  ExterQual = models.IntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)],
    verbose_name="Exterior Quality",
    help_text="Rate the quality of the material on the exterior (1-5)",
    null=True,
    blank=True,
  )
  Foundation = models.CharField(
    max_length=255,
    choices=[
      ('BrkTil', 'Brick & Tile'),
      ('CBlock', 'Cinder Block'),
      ('PConc', 'Poured Concrete'),
      ('Slab', 'Slab'),
      ('Stone', 'Stone'),
      ('Wood', 'Wood')
    ],
    verbose_name="Foundation",
    null=True,
    blank=True,
  )
  CentralAir = models.CharField(
    max_length=255,
    choices=[
      ('N', 'No'),
      ('Y', 'Yes')
    ],
    verbose_name="Central Air Conditioning",
    null=True,
    blank=True,
  )
  YrSold = models.IntegerField(
    validators=[MaxValueValidator(current_year)],
    verbose_name="Year Last Sold",
    null=True,
    blank=True,
  )

  # OPTIONAL FEATURES
  OverallQual = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(1), MaxValueValidator(10)],
    verbose_name="Overall Quality",
    help_text="Rate the overall material and finish quality (1-10)"
  )
  PoolArea = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Pool Area in square feet"
  )
  PavedDrive = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    choices=[
      ('Y', 'Paved'),
      ('P', 'Partial Pavement'),
      ('N', 'Dirt/Gravel')
    ],
    verbose_name="Paved Driveway"
  )
  GarageArea = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Garage Area"
  )
  Fireplaces = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Number of Fireplaces"
  )
  KitchenAbvGr = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Number of kitchens (above grade)"
  )
  LotArea = models.IntegerField(
    validators=[MinValueValidator(0)],
    verbose_name="Total Property Area",
    null=True,
    blank=True,
  )
  Heating = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    choices=[
      ('Floor', 'Floor Furnace'),
      ('GasA', 'Gas forced warm air furnace'),
      ('GasW', 'Gas hot water or steam heat'),
      ('Grav', 'Gravity furnace'),
      ('OthW', 'Hot water or steam heat other than gas'),
      ('Wall', 'Wall furnace'),
    ],
    verbose_name="Heating"
  )
  TotalBsmtSF = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Total Basement Area"
  )
  BsmtUnfSF = models.IntegerField(
    null=True,
    blank=True,
    validators=[MinValueValidator(0)],
    verbose_name="Unfinished Basement Area"
  )
  Exterior1st = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    choices=[
      ('VinylSd', 'Vinyl Siding'),
      ('MetalSd', 'Metal Siding'),
      ('Wd Sdng', 'Wood Siding'),
      ('HdBoard', 'Hardboard'),
      ('BrkFace', 'Brick Face'),
      ('WdShing', 'Wood Shingles'),
      ('CemntBd', 'Cement Board'),
      ('Plywood', 'Plywood'),
      ('AsbShng', 'Asbestos Shingles'),
      ('Stucco', 'Stucco'),
      ('BrkComm', 'Brick Common'),
      ('AsphShn', 'Asphalt Shingles'),
      ('Stone', 'Stone'),
      ('ImStucc', 'Imitation Stucco'),
      ('CBlock', 'Cinder Block'),
      ('Other', 'Other'),
      ('PreCast', 'PreCast')
    ],
    verbose_name="Exterior Material"
  )
  Exterior2nd = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    choices=[
      ('VinylSd', 'Vinyl Siding'),
      ('MetalSd', 'Metal Siding'),
      ('Wd Sdng', 'Wood Siding'),
      ('HdBoard', 'Hardboard'),
      ('BrkFace', 'Brick Face'),
      ('WdShing', 'Wood Shingles'),
      ('CemntBd', 'Cement Board'),
      ('Plywood', 'Plywood'),
      ('AsbShng', 'Asbestos Shingles'),
      ('Stucco', 'Stucco'),
      ('BrkComm', 'Brick Common'),
      ('AsphShn', 'Asphalt Shingles'),
      ('Stone', 'Stone'),
      ('ImStucc', 'Imitation Stucco'),
      ('CBlock', 'Cinder Block'),
      ('Other', 'Other'),
      ('PreCast', 'PreCast')
    ],
    verbose_name="Exterior Material (2nd if more than one)"
  )
  RoofStyle = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    choices=[
      ('Gable', 'Gable'),
      ('Hip', 'Hip'),
      ('Flat', 'Flat'),
      ('Gambrel', 'Gambrel (Barn)'),
      ('Mansard', 'Mansard'),
      ('Shed', 'Shed')
    ],
    verbose_name="Roof Style"
  )
  YearRemodAdd = models.IntegerField(
    null=True,
    blank=True,
    validators=[MaxValueValidator(current_year)],
    verbose_name="Year Remodeled",
  )
  LotConfig = models.CharField(
    null=True,
    blank=True,
    max_length=255,
    choices=[
      ('Inside', 'Inside lot'),
      ('Corner', 'Corner lot'),
      ('CulDSac', 'Cul-de-Sac'),
      ('FR2', 'Frontage on 2 sides'),
    ],
    verbose_name="Lot Configuration"
  )
  

  predicted_price = models.FloatField(null=True, blank=True)
  
  def __str__(self):
     return f"{self.address}, {self.city}, {self.state} {self.zipcode}"
  
  def save(self, *args, **kwargs):
    try:
        this = HouseListing.objects.get(id=self.id)
        if this.HouseImage != self.HouseImage:
            this.HouseImage.delete(save=False)
    except:
        pass
    super(HouseListing, self).save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    self.HouseImage.delete(save=False)
    super(HouseListing, self).delete(*args, **kwargs)