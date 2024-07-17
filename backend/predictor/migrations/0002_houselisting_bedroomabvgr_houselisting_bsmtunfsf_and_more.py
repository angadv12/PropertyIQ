# Generated by Django 5.0.6 on 2024-07-11 09:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='houselisting',
            name='BedroomAbvGr',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Bedrooms (above grade)'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='BsmtUnfSF',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Unfinished Basement Area'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='CentralAir',
            field=models.CharField(blank=True, choices=[('N', 'No'), ('Y', 'Yes')], max_length=255, null=True, verbose_name='Central Air Conditioning'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='ExterQual',
            field=models.IntegerField(blank=True, help_text='Rate the quality of the material on the exterior (1-5)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Exterior Quality'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='Exterior1st',
            field=models.CharField(blank=True, choices=[('VinylSd', 'Vinyl Siding'), ('MetalSd', 'Metal Siding'), ('Wd Sdng', 'Wood Siding'), ('HdBoard', 'Hardboard'), ('BrkFace', 'Brick Face'), ('WdShing', 'Wood Shingles'), ('CemntBd', 'Cement Board'), ('Plywood', 'Plywood'), ('AsbShng', 'Asbestos Shingles'), ('Stucco', 'Stucco'), ('BrkComm', 'Brick Common'), ('AsphShn', 'Asphalt Shingles'), ('Stone', 'Stone'), ('ImStucc', 'Imitation Stucco'), ('CBlock', 'Cinder Block'), ('Other', 'Other'), ('PreCast', 'PreCast')], max_length=255, null=True, verbose_name='Exterior Material'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='Exterior2nd',
            field=models.CharField(blank=True, choices=[('VinylSd', 'Vinyl Siding'), ('MetalSd', 'Metal Siding'), ('Wd Sdng', 'Wood Siding'), ('HdBoard', 'Hardboard'), ('BrkFace', 'Brick Face'), ('WdShing', 'Wood Shingles'), ('CemntBd', 'Cement Board'), ('Plywood', 'Plywood'), ('AsbShng', 'Asbestos Shingles'), ('Stucco', 'Stucco'), ('BrkComm', 'Brick Common'), ('AsphShn', 'Asphalt Shingles'), ('Stone', 'Stone'), ('ImStucc', 'Imitation Stucco'), ('CBlock', 'Cinder Block'), ('Other', 'Other'), ('PreCast', 'PreCast')], max_length=255, null=True, verbose_name='Exterior Material (2nd if more than one)'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='Fireplaces',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Number of Fireplaces'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='Foundation',
            field=models.CharField(blank=True, choices=[('BrkTil', 'Brick & Tile'), ('CBlock', 'Cinder Block'), ('PConc', 'Poured Concrete'), ('Slab', 'Slab'), ('Stone', 'Stone'), ('Wood', 'Wood')], max_length=255, null=True, verbose_name='Foundation'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='FullBath',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Full Bathrooms'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='GarageArea',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Garage Area'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='GarageCars',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Garage Size (in cars)'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='GrLivArea',
            field=models.IntegerField(blank=True, help_text='Square footage of living area above grade', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Above Ground Living Area'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='HalfBath',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Half Bathrooms'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='Heating',
            field=models.CharField(blank=True, choices=[('Floor', 'Floor Furnace'), ('GasA', 'Gas forced warm air furnace'), ('GasW', 'Gas hot water or steam heat'), ('Grav', 'Gravity furnace'), ('OthW', 'Hot water or steam heat other than gas'), ('Wall', 'Wall furnace')], max_length=255, null=True, verbose_name='Heating'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='KitchenAbvGr',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Number of kitchens (above grade)'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='OverallQual',
            field=models.IntegerField(blank=True, help_text='Rate the overall material and finish quality (1-10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Overall Quality'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='PavedDrive',
            field=models.CharField(blank=True, choices=[('Y', 'Paved'), ('P', 'Partial Pavement'), ('N', 'Dirt/Gravel')], max_length=255, null=True, verbose_name='Paved Driveway'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='PoolArea',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Pool Area in square feet'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='RoofStyle',
            field=models.CharField(blank=True, choices=[('Gable', 'Gable'), ('Hip', 'Hip'), ('Flat', 'Flat'), ('Gambrel', 'Gambrel (Barn)'), ('Mansard', 'Mansard'), ('Shed', 'Shed')], max_length=255, null=True, verbose_name='Roof Style'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='TotalBsmtSF',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total Basement Area'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='YearBuilt',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2024)], verbose_name='Year Built'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='YearRemodAdd',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2024)], verbose_name='Year Remodeled'),
        ),
        migrations.AddField(
            model_name='houselisting',
            name='YrSold',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(2024)], verbose_name='Year Last Sold'),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='BldgType',
            field=models.CharField(blank=True, choices=[('1Fam', 'Single-family'), ('2FmCon', 'Apartment building'), ('TwnhsE', 'Townhouse end unit'), ('TwnhsI', 'Townhouse inside unit')], max_length=255, null=True, verbose_name='Building Type'),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='LandSlope',
            field=models.CharField(blank=True, choices=[('Gtl', 'Slight slope'), ('Mod', 'Moderate slope'), ('Sev', 'Severe slope')], max_length=255, null=True, verbose_name='Land Slope'),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='LotArea',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total Property Area'),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='LotConfig',
            field=models.CharField(blank=True, choices=[('Inside', 'Inside lot'), ('Corner', 'Corner lot'), ('CulDSac', 'Cul-de-Sac'), ('FR2', 'Frontage on 2 sides')], max_length=255, null=True, verbose_name='Lot Configuration'),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='Utilities',
            field=models.CharField(blank=True, choices=[('AllPub', 'All public utilities'), ('NoSewr', 'Electricity, Gas, and Water'), ('NoSeWa', 'Electricity and Gas/Water Only'), ('ELO', 'Electricity only')], max_length=255, null=True, verbose_name='Utilities'),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='state',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='houselisting',
            name='zipcode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
