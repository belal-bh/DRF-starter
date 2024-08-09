from django.db import models


class Address(models.Model):
    ADDRESS_TYPE_PARMANENT = 'parmanent'
    ADDRESS_TYPE_MAILING = 'mailing'
    ADDRESS_TYPE_BILLING = 'billing'
    ADDRESS_TYPE_SHIPPING = 'shipping'
    ADDRESS_TYPE_CHOICES = [
        (ADDRESS_TYPE_PARMANENT, 'Parmanent Address'),
        (ADDRESS_TYPE_MAILING, 'Mailing Address'),
        (ADDRESS_TYPE_BILLING, 'Billing Address'),
        (ADDRESS_TYPE_SHIPPING, 'Shipping Address'),
    ]

    CITY_CHOICES = [
        (None, 'Select City'),
        # Barishal Division
        ('Barishal Division', (
            ('Barguna', 'Barguna'),
            ('Barishal', 'Barishal'),
            ('Bhola', 'Bhola'),
            ('Jhalakathi', 'Jhalakathi'),
            ('Patuakhali', 'Patuakhali'),
            ('Pirojpur', 'Pirojpur'),
        )
        ),
        # Chattogram Division
        ('Chattogram Division', (
            ('Bandarban', 'Bandarban'),
            ('Brahmanbaria', 'Brahmanbaria'),
            ('Chandpur', 'Chandpur'),
            ('Chattogram', 'Chattogram'),
            ('Cumilla', 'Cumilla'),
            ("Cox's Bazar", "Cox's Bazar"),
            ('Feni', 'Feni'),
            ('Khagrachhari', 'Khagrachhari'),
            ('Lakshmipur', 'Lakshmipur'),
            ('Noakhali', 'Noakhali'),
            ('Rangamati', 'Rangamati'),
        )
        ),
        # Dhaka Division
        ('Dhaka Division', (
            ('Dhaka', 'Dhaka'),
            ('Faridpur', 'Faridpur'),
            ('Gazipur', 'Gazipur'),
            ('Gopalganj', 'Gopalganj'),
            ('Kishoreganj', 'Kishoreganj'),
            ('Madaripur', 'Madaripur'),
            ('Manikganj', 'Manikganj'),
            ('Munshiganj', 'Munshiganj'),
            ('Narayanganj', 'Narayanganj'),
            ('Narsingdi', 'Narsingdi'),
            ('Rajbari', 'Rajbari'),
            ('Shariatpur', 'Shariatpur'),
            ('Tangail', 'Tangail'),
        )
        ),
        # Khulna Division
        ('Khulna Division', (
            ('Bagerhat', 'Bagerhat'),
            ('Chuadanga', 'Chuadanga'),
            ('Jashore', 'Jashore'),
            ('Jhenaidah', 'Jhenaidah'),
            ('Khulna', 'Khulna'),
            ('Kushtia', 'Kushtia'),
            ('Magura', 'Magura'),
            ('Meherpur', 'Meherpur'),
            ('Narail', 'Narail'),
            ('Satkhira', 'Satkhira'),
        )
        ),
        # Mymensingh Division
        ('Mymensingh Division', (
            ('Jamalpur', 'Jamalpur'),
            ('Mymensingh', 'Mymensingh'),
            ('Netrokona', 'Netrokona'),
            ('Sherpur', 'Sherpur'),
        )
        ),
        # Rajshahi Division
        ('Rajshahi Division', (
            ('Bogura', 'Bogura'),
            ('Joypurhat', 'Joypurhat'),
            ('Naogaon', 'Naogaon'),
            ('Natore', 'Natore'),
            ('Nawabganj', 'Nawabganj'),
            ('Pabna', 'Pabna'),
            ('Rajshahi', 'Rajshahi'),
            ('Sirajganj', 'Sirajganj'),
        )
        ),
        # Rangpur Division
        ('Rangpur Division', (
            ('Dinajpur', 'Dinajpur'),
            ('Gaibandha', 'Gaibandha'),
            ('Kurigram', 'Kurigram'),
            ('Lalmonirhat', 'Lalmonirhat'),
            ('Nilphamari', 'Nilphamari'),
            ('Panchagarh', 'Panchagarh'),
            ('Rangpur', 'Rangpur'),
            ('Thakurgaon', 'Thakurgaon'),
        )
        ),
        # Sylhet Division
        ('Sylhet Division', (
            ('Habiganj', 'Habiganj'),
            ('Moulvibazar', 'Moulvibazar'),
            ('Sunamganj', 'Sunamganj'),
            ('Sylhet', 'Sylhet'),
        )
        ),
    ]

    STATE_CHOICES = [
        (None, 'Select State/Division'),
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Dhaka', 'Dhaka'),
        ('Khulna', 'Khulna'),
        ('Mymensingh', 'Mymensingh'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Sylhet', 'Sylhet'),
    ]

    COUNTRY_CHOICE_BANGLADESH = "Bangladesh"
    COUNTRY_CHOICES = [
        (COUNTRY_CHOICE_BANGLADESH, 'Bangladesh'),
    ]

    address_type = models.CharField(
        max_length=10, choices=ADDRESS_TYPE_CHOICES)
    line_1 = models.CharField(max_length=120)
    line_2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=20, choices=CITY_CHOICES)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(
        max_length=20, choices=COUNTRY_CHOICES, default=COUNTRY_CHOICE_BANGLADESH)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "address"
        verbose_name_plural = "addresses"

    def __str__(self):
        return f"{self.line_1},{self.city}-{self.postal_code}"
