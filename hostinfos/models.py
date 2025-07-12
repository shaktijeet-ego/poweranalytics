from django.db import models

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'regions'  # Match your real table name exactly (case-sensitive)

    def __str__(self):
        return self.region_name

class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.province_name
    
    class Meta:
        managed = False
        db_table = 'provinces'  # Match your real table name exactly (case-sensitive)

class Branch(models.Model):
    branch_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=255)
    region = models.ForeignKey('Region', on_delete=models.DO_NOTHING, db_column='region_id')

    class Meta:
        managed = False
        db_table = 'branches'

    def __str__(self):
        return self.branch_name

class Outlet(models.Model):
    outlet_id = models.AutoField(primary_key=True)
    outlet_name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, db_column='branch_id')
    #province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.outlet_name

    class Meta:
        managed = False
        db_table = 'outlets'  # Match your real table name exactly (case-sensitive)

class Host(models.Model):
    host_id = models.AutoField(primary_key=True)
    host_name = models.CharField(max_length=100)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE, db_column='outlet_id')
    province = models.ForeignKey(Province, on_delete=models.CASCADE, db_column='province_id')
    host_type = models.CharField(max_length=50, blank=True, null=True)
    date_of_live = models.DateField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return self.host_name
    
    class Meta:
        managed = False
        db_table = 'hosts'  # Match your real table name exactly (case-sensitive)


class PowerInfo(models.Model):
    power_id = models.AutoField(primary_key=True)
    host = models.ForeignKey('Host', on_delete=models.DO_NOTHING, db_column='host_id')
    no_of_batteries = models.IntegerField(null=True, blank=True)
    damaged_batteries = models.IntegerField(null=True, blank=True)
    last_installed = models.DateField(null=True, blank=True)
    from datetime import timedelta

    backup_duration = models.DurationField(null=True, blank=True)

    solar_available = models.BooleanField(default=False)

    GENERATOR_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('ondemand', 'On Demand')
    ]
    generator_available = models.CharField(max_length=10, choices=GENERATOR_CHOICES, default='no')

    last_maintainance_date = models.DateField(null=True, blank=True)

    UPS_STATUS_CHOICES = [
        ('good', 'Good'),
        ('fine', 'Fine'),
        ('damaged', 'Damaged')
    ]
    ups_status = models.CharField(max_length=10, choices=UPS_STATUS_CHOICES, null=True, blank=True)

    batteries_changed = models.BooleanField(default=False)
    no_of_batteries_changed = models.IntegerField(null=True, blank=True)
    changed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.host.host_name


    class Meta:
        managed = False
        db_table = 'power_systems'  # Match your real table name exactly (case-sensitive)