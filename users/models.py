from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email instead of username for authentication.
    """
    
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    # Additional custom fields
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required as USERNAME_FIELD
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name


class PartnerMapping(models.Model):
    partner_sku_name = models.CharField(max_length=255, blank=True, null=True)
    master2_price_list = models.CharField(max_length=255, blank=True, null=True)
    master3_first_call = models.CharField(max_length=255, blank=True, null=True)
    master3_breakfix_4hr = models.CharField(max_length=255, blank=True, null=True)
    master3_breakfix_nbd = models.CharField(max_length=255, blank=True, null=True)
    master4_deploy_per_install = models.CharField(max_length=255, blank=True, null=True)
    
    # add timestamps for tracking when mappings are added/updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'partner_mappings'

    def __str__(self):
        return self.partner_sku_name or f"PartnerMapping {self.id}"


class MasterSKUMapping(models.Model):
    master_sku_name = models.CharField(max_length=255, blank=True, null=True)
    partner_mapping = models.ForeignKey(PartnerMapping, on_delete=models.CASCADE, related_name='master_mappings')
    SKU_TYPE = [
        ('Primary', 'Primary'),
        ('Additional', 'Additional'),
    ]
    sku_type = models.CharField(max_length=16, choices=SKU_TYPE, default='Primary')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'master_sku_mappings'
    
    def __str__(self):
        return self.master_sku_name or f"MasterSKUMapping {self.id}"
    
    @property
    def partner_sku_name(self):
        return self.partner_mapping.partner_sku_name if self.partner_mapping else None
    
# Through model to store quantity per WorkOrder primary SKU
class WorkOrderPrimarySKU(models.Model):
    workorder = models.ForeignKey('WorkOrder', on_delete=models.CASCADE, related_name='primary_sku_items')
    sku = models.ForeignKey(MasterSKUMapping, on_delete=models.CASCADE, related_name='workorder_primary_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'workorder_primary_skus'
        unique_together = ('workorder', 'sku')
        verbose_name = 'WorkOrder Primary SKU'
        verbose_name_plural = 'WorkOrder Primary SKUs'

    def __str__(self):
        return f"{self.workorder} - {self.sku} ({self.quantity})"
    
# Through model to store quantity per WorkOrder additional SKU
class WorkOrderAdditionalSKU(models.Model):
    workorder = models.ForeignKey('WorkOrder', on_delete=models.CASCADE, related_name='additional_sku_items')
    sku = models.ForeignKey(MasterSKUMapping, on_delete=models.CASCADE, related_name='workorder_additional_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'workorder_additional_skus'
        unique_together = ('workorder', 'sku')
        verbose_name = 'WorkOrder Additional SKU'
        verbose_name_plural = 'WorkOrder Additional SKUs'

    def __str__(self):
        return f"{self.workorder} - {self.sku} ({self.quantity})"

class Country(models.Model):
    """Store country display name and its 2-letter ISO code (ISO 3166-1 alpha-2).
    Example: name='India', code='IN'
        Also store the name of the pricing sheet to use for the country, and the WWT region it belongs to.
    """
    name = models.CharField(max_length=128, unique=True)
    code = models.CharField(max_length=2, unique=True)
    pricing_sheet = models.CharField(max_length=128, blank=True, default='') 
    WWT_REGION_CHOICES = [
        ('NAIC', 'NAIC'),
        ('EIC', 'EIC'),
        ('AIC-S', 'AIC-S'),
        ('UNKNOWN', 'UNKNOWN'),
    ]
    wwt_region = models.CharField(max_length=16, choices=WWT_REGION_CHOICES, default='NAIC')
    
    primary_skus = models.ManyToManyField(
        MasterSKUMapping,
        blank=True,
        related_name='primary_skus',
        limit_choices_to={'sku_type': 'Primary'}
    )
    additional_skus = models.ManyToManyField(
        MasterSKUMapping,
        blank=True,
        related_name='additional_skus',
        limit_choices_to={'sku_type': 'Additional'}
    )

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code.upper()})"

    def save(self, *args, **kwargs):
        # Ensure code is stored uppercase and trimmed
        if self.code:
            self.code = self.code.strip().upper()
        # If pricing_sheet is blank, default to country name
        if not self.pricing_sheet:
            self.pricing_sheet = self.name
        super().save(*args, **kwargs)


class WorkOrder(models.Model):
    """Store a work order created from the dashboard form."""
    
    work_order_number = models.CharField(max_length=128, blank=True)
    client = models.CharField(max_length=255, blank=True)
    work_order_date = models.DateField(null=True, blank=True)

    # add choices for sector, term, and support fields based on typical values seen in work orders
    SECTOR_CHOICES = [
        ('Public', 'Public Sector'),
        ('Commercial', 'Commercial Sector'),
    ]
    sector = models.CharField(max_length=64, choices=SECTOR_CHOICES, default='Public Sector')

    TERM_CHOICES = [
        ('60', '60'),
        ('45', '45'),
        ('30', '30'),
    ]
    term = models.CharField(max_length=64, choices=TERM_CHOICES, default='60')
    
    SUPPORT_CHOICES = [
        ('4hr', '4hr'),
        ('NBD', 'NBD'),
    ]
    support = models.CharField(max_length=64, choices=SUPPORT_CHOICES, default='4 hrs')

    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=26)

    # primary_skus uses a through model to store quantity per SKU
    primary_skus = models.ManyToManyField(
        MasterSKUMapping,
        through='WorkOrderPrimarySKU',
        blank=True,
        related_name='workorders_primary_skus',
        limit_choices_to={'sku_type': 'Primary'}
    )
    # additional_skus now also uses a through model to store quantity per SKU
    additional_skus = models.ManyToManyField(
        MasterSKUMapping,
        through='WorkOrderAdditionalSKU',
        blank=True,
        related_name='workorders_additional_skus',
        limit_choices_to={'sku_type': 'Additional'}
    )

    google_legal_entity = models.CharField(max_length=255, blank=True)
    google_bill_to_address = models.TextField(blank=True)
    google_ship_to_address = models.TextField(blank=True)

    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='workorders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"WO {self.work_order_number or self.id} - {self.client or 'unknown'}"
    

# create a model to store generated price estimator files for each work order, with a foreign key to the WorkOrder and fields for file name and generation timestamp
class WorkOrderPriceEstimate(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='price_estimates')
    file_name = models.CharField(max_length=255)
    generated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='price_estimates')

    class Meta:
        db_table = 'workorder_price_estimates'
        verbose_name = 'Work Order Price Estimate'
        verbose_name_plural = 'Work Order Price Estimates'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.file_name}"