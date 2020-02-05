from django.db import models
from django.contrib.auth.models import User

# Create your models here.
c = (
    ('AGONDA_BEACH','AGONDA_BEACH'),
    ('ANJUNA_WEDNESDAY_MARKET','ANJUNA_WEDNESDAY_MARKET'),
    ('ARAMBOL_HIPPIE_FESTIVAL','ARAMBOL_HIPPIE_FESTIVAL'),
    ('ASILICA_OF_BOM_JESUS','ASILICA_OF_BOM_JESUS'),
    ('BAGA_BEACH','BAGA_BEACH'),
    ('CASINO_IN_PANJIM','CASINO_IN_PANJIM'),
    ('CHAPORA_FORT','CHAPORA_FORT'),
    ('CHURCH_OF_OUR_LADY_OF_IMMACULATE_CONCEPTION','CHURCH_OF_OUR_LADY_OF_IMMACULATE_CONCEPTION'),
    ('DUDHSAGAR_FALLS','DUDHSAGAR_FALLS'),
    ('FORT_AGUADA','FORT_AGUADA'),
    ('FORT_CABO_DE_RAMA','FORT_CABO_DE_RAMA'),
    ('GO_KART_RACING','GO_KART_RACING'),
    ('GRANDE_ISLAND','GRANDE_ISLAND'),
    ('HALASSA_RESTAURANT','HALASSA_RESTAURANT'),
    ('HILL_TOP_CLUB_IN_ANJUNA','HILL_TOP_CLUB_IN_ANJUNA'),
    ('LATIN_QUARTER','LATIN_QUARTER'),
    ('NAVAL_AVIATION_MUSEUM','NAVAL_AVIATION_MUSEUM'),
    ('PARAGLIDING_IN_ARAMBOL','PARAGLIDING_IN_ARAMBOL'),
    ('TEREKHOL_FORT','TEREKHOL_FORT'))




class details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return str(self.user)

class comments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.CharField(max_length = 256)
    # place = models.CharField(choices=c,max_length=128)
    def __str__(self):
        return str(self.user)

class check_in_data(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    place = models.CharField(max_length = 128)
    p = models.CharField(max_length = 128,blank=True,null=True)
    dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)