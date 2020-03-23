
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Address(models.Model):
    address_id = models.AutoField(db_column='Address_id', primary_key=True)  # Field name made lowercase.
    contact = models.ForeignKey('Contact', models.DO_NOTHING, db_column='Contact_id',related_name='address_contact')  # Field name made lowercase.
    address_type = models.CharField(db_column='Address_type', max_length=30, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=30, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=20, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=20, blank=True, null=True)  # Field name made lowercase.
    zip = models.IntegerField(db_column='Zip', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'address'


class Contact(models.Model):
    contact_id = models.AutoField(db_column='Contact_id', primary_key=True)  # Field name made lowercase.
    fname = models.CharField(db_column='Fname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    mname = models.CharField(db_column='Mname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lname = models.CharField(db_column='Lname', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'contact'


class Date(models.Model):
    date_id = models.AutoField(db_column='Date_id', primary_key=True)  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='Contact_id',related_name='date_contact')  # Field name made lowercase.
    date_type = models.CharField(db_column='Date_type', max_length=30, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'date'


class Phone(models.Model):
    phone_id = models.AutoField(db_column='Phone_id', primary_key=True)  # Field name made lowercase.
    contact = models.ForeignKey(Contact, models.DO_NOTHING, db_column='Contact_id',related_name='phone_contact')  # Field name made lowercase.
    phone_type = models.CharField(db_column='Phone_type', max_length=30, blank=True, null=True)  # Field name made lowercase.
    area_code = models.IntegerField(db_column='Area_code', blank=True, null=True)  # Field name made lowercase.
    number = models.IntegerField(db_column='Number', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'phone'
