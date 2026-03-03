from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, PartnerMapping, MasterSKUMapping, Country, WorkOrder, \
    WorkOrderPrimarySKU, WorkOrderAdditionalSKU, WorkOrderPriceEstimate


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for User model
    """
    
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'bio', 'birth_date', 'profile_picture')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']


@admin.register(PartnerMapping)
class PartnerMappingAdmin(admin.ModelAdmin):
    list_display = (
        'partner_sku_name', 'master2_price_list', 'master3_first_call',
        'master3_breakfix_4hr', 'master3_breakfix_nbd', 'master4_deploy_per_install'
    )
    search_fields = ('partner_sku_name',)
    ordering = ('partner_sku_name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MasterSKUMapping)
class MasterSKUMappingAdmin(admin.ModelAdmin):
    list_display = ('master_sku_name','partner_sku_names')
    search_fields = (
        'master_sku_name', 
        'partner_mapping__partner_sku_name'
    )
    ordering = ('master_sku_name',)
    readonly_fields = ('created_at', 'updated_at')

    def partner_sku_names(self, obj):
        names = []
        # # ManyToMany case
        # if hasattr(obj, 'partner_mappings'):
        #     try:
        #         for pm in obj.partner_mappings.all():
        #             if pm and pm.partner_sku_name:
        #                 names.append(pm.partner_sku_name)
        #     except Exception:
        #         # if relation not available or not loaded, ignore
        #         pass
        # ForeignKey case
        pm = getattr(obj, 'partner_mapping', None)
        if pm and getattr(pm, 'partner_sku_name', None):
            names.append(pm.partner_sku_name)

        return ', '.join(names) if names else ''

    partner_sku_names.short_description = 'Partner SKU Names'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'pricing_sheet', 'wwt_region', 'show_primary_skus', 'show_additional_skus')
    search_fields = ('name', 'code')
    ordering = ('name',)
    filter_horizontal = ('primary_skus', 'additional_skus')

    def show_primary_skus(self, obj):
        names = []
        if hasattr(obj, 'primary_skus'):
            try:
                for pm in obj.primary_skus.all():
                    if pm and getattr(pm, 'master_sku_name', None):
                        names.append(pm.master_sku_name)
            except Exception:
                pass

        return ', '.join(names) if names else ''
    show_primary_skus.short_description = 'Primary SKUs'
    
    def show_additional_skus(self, obj):
        names = []
        if hasattr(obj, 'additional_skus'):
            try:
                for pm in obj.additional_skus.all():
                    if pm and getattr(pm, 'master_sku_name', None):
                        names.append(pm.master_sku_name)
            except Exception:
                pass
        # Fallback: in case a singular relation exists
        # else:
        #     pm = getattr(obj, 'additional_sku', None) or getattr(obj, 'master_sku_mappings', None)
        #     if pm and getattr(pm, 'master_sku_name', None):
        #         if getattr(pm, 'sku_type', None) == 'Additional' or True:
        #             names.append(pm.master_sku_name)

        return ', '.join(names) if names else ''
    show_additional_skus.short_description = 'Additional SKUs'


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('work_order_number', 'client', 'country', 'sector', 'term', 'support', 'primary_skus_list', 'additional_skus_list')
    readonly_fields = ('primary_skus_list', 'additional_skus_list','created_at', 'updated_at')
    search_fields = ('work_order_number', 'client', 'country__name', 'created_by__email')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        """
        Automatically set created_by to the admin user when creating a new WorkOrder
        (or if created_by is not already set).
        """
        if not getattr(obj, 'created_by', None):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
    def primary_skus_list(self, obj):
        if obj is None:
            return ''
        names = []
        try:
            if hasattr(obj, 'primary_sku_items'):
                items = obj.primary_sku_items.all()
                for it in items:
                    if hasattr(it, 'sku'):
                        sku_obj = it.sku
                        qty = getattr(it, 'quantity', None)
                        print(f"Got primary SKU item with SKU {sku_obj} and quantity {qty}")
                        names.append(f"{sku_obj} ({qty})")
                    else:
                        sku_obj = it
                        qty = None
        except Exception:
            # avoid admin crash if relation not available
            pass

        return ', '.join(names) if names else ''
    primary_skus_list.short_description = 'Primary SKUs'

    def additional_skus_list(self, obj):
        # show additional SKU names (and quantities if present) on the detail/admin form
        if obj is None:
            return ''
        names = []
        try:
            if hasattr(obj, 'additional_sku_items'):
                items = obj.additional_sku_items.all()
                for it in items:
                    if hasattr(it, 'sku'):
                        sku_obj = it.sku
                        qty = getattr(it, 'quantity', None)
                        print(f"Got additional SKU item with SKU {sku_obj} and quantity {qty}")
                        names.append(f"{sku_obj} ({qty})")
                    else:
                        sku_obj = it
                        qty = None
        except Exception:
            # avoid admin crash if relation not available
            pass

        return ', '.join(names) if names else ''
    additional_skus_list.short_description = 'Additional SKUs'


@admin.register(WorkOrderPrimarySKU)
class WorkOrderPrimarySKUAdmin(admin.ModelAdmin):
    # model field is 'workorder' (FK) on WorkOrderPrimarySKU
    list_display = ('workorder', 'sku', 'quantity')
    search_fields = ('workorder__work_order_number', 'sku__master_sku_name')
    # ordering = ('work_order',)


@admin.register(WorkOrderAdditionalSKU)
class WorkOrderAdditionalSKUAdmin(admin.ModelAdmin):
    list_display = ('workorder', 'sku', 'quantity')
    search_fields = ('workorder__work_order_number', 'sku__master_sku_name')
    # ordering = ('work_order',)

@admin.register(WorkOrderPriceEstimate)
class WorkOrderPriceEstimateAdmin(admin.ModelAdmin):
    list_display = ('workorder', 'file_name', 'generated_at', 'created_by')
    search_fields = ('workorder__work_order_number', 'file_name', 'created_by__email')
    readonly_fields = ('generated_at',)
