from django.contrib.gis.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=20)
    profile_img = models.URLField(null=True)
    uuid = models.CharField(max_length=32)
    provider = models.CharField(max_length=10)
    animals = models.ManyToManyField('Animal')
    address = models.ForeignKey('Address', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'user'


class Animal(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'animal'


class UserAnimals(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    animal_id = models.ForeignKey("Animal", on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'user_animals'


class Address(models.Model):
    address_name = models.CharField(max_length=100)
    address_type = models.CharField(max_length=11)
    address_coord = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'address'


class AddressRegion(models.Model):
    address = models.OneToOneField(
        'Address', on_delete=models.CASCADE, primary_key=True)
    address_name = models.CharField(max_length=100)
    region_1depth_name = models.CharField(max_length=20)
    region_2depth_name = models.CharField(max_length=20)
    region_3depth_name = models.CharField(max_length=20)
    region_3depth_h_name = models.CharField(max_length=20)
    h_code = models.CharField(max_length=10)
    b_code = models.CharField(max_length=10)
    mountain_yn = models.CharField(max_length=1)
    main_address_no = models.CharField(max_length=10)
    sub_address_no = models.CharField(max_length=10, blank=True)
    address_coord = models.PointField()

    class Meta:
        managed = False
        db_table = 'address_region'


class AddressRoad(models.Model):
    address = models.OneToOneField(
        'Address', on_delete=models.CASCADE, primary_key=True)
    address_name = models.CharField(max_length=100)
    region_1depth_name = models.CharField(max_length=20)
    region_2depth_name = models.CharField(max_length=20)
    region_3depth_name = models.CharField(max_length=20)
    road_name = models.CharField(max_length=20)
    underground_yn = models.CharField(max_length=1, blank=True)
    main_building_no = models.CharField(max_length=10)
    sub_building_no = models.CharField(max_length=10, blank=True)
    building_name = models.CharField(max_length=30, blank=True)
    zone_no = models.CharField(max_length=5)
    address_coord = models.PointField()

    class Meta:
        managed = False
        db_table = 'address_road'
