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
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    #province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.outlet_name

    class Meta:
        managed = False
        db_table = 'outlets'  # Match your real table name exactly (case-sensitive)

class Host(models.Model):
    host_id = models.AutoField(primary_key=True)
    host_name = models.CharField(max_length=100)
    outlet = models.ForeignKey(Outlet, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    host_type = models.CharField(max_length=50, blank=True, null=True)
    date_of_live = models.DateField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    def __str__(self):
        return self.host_name
    
    class Meta:
        managed = False
        db_table = 'hosts'  # Match your real table name exactly (case-sensitive)