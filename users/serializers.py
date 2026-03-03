from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import MasterSKUMapping, User, Country, WorkOrder


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model - used for displaying user information
    """
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'phone_number', 'bio', 'birth_date', 
            'profile_picture', 'date_joined', 'is_active'
        ]
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'email': {'required': True},
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }
    
    def validate(self, attrs):
        """
        Verify that passwords match
        """
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user with encrypted password
        """
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """
        Verify credentials and return user if valid
        """
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.',
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".',
                code='authorization'
            )
        
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        """
        Verify old password is correct
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value
    
    def validate(self, attrs):
        """
        Verify that new passwords match
        """
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        return attrs
    
    def save(self, **kwargs):
        """
        Set new password for user
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'bio', 'birth_date', 'profile_picture'
        ]


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model"""

    class Meta:
        model = Country
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']


class SKUQuantitySerializer(serializers.Serializer):
    sku = serializers.PrimaryKeyRelatedField(queryset=MasterSKUMapping.objects.all())
    qty = serializers.IntegerField(min_value=1, default=1)


class WorkOrderSerializer(serializers.ModelSerializer):
    """Serializer to validate and create WorkOrder records from dashboard."""
    # Accept SKU+qty as input, but don't let DRF try to serialize them automatically
    # (the related objects are MasterSKUMapping instances and don't match the
    # SKUQuantitySerializer shape). We'll emit read-format in to_representation.
    primary_skus = SKUQuantitySerializer(many=True, required=False, write_only=True)
    additional_skus = SKUQuantitySerializer(many=True, required=False, write_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = None
        # set model dynamically in __init__ to avoid import cycles
        fields = [
            'id', 'work_order_number', 'client', 'work_order_date',
            'google_legal_entity', 'google_bill_to_address', 'google_ship_to_address',
            'sector', 'term', 'support', 'country',
            'primary_skus', 'additional_skus', 'notes',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
        extra_kwargs = {
            'sector': {'required': True},
            'term': {'required': True},
            'support': {'required': True},
            'country': {'required': True},
        }

    def __init__(self, *args, **kwargs):
        # import here to avoid circular imports
        from .models import WorkOrder
        super().__init__(*args, **kwargs)
        self.Meta.model = WorkOrder


    def create(self, validated_data, created_by=None, country=None):
        primary_items = validated_data.pop('primary_skus', [])
        additional_items = validated_data.pop('additional_skus', [])
        # country may be passed in kwargs by the view; if not, may be in validated_data
        country_obj = country or validated_data.pop('country', None)

        # Avoid passing duplicate created_by or country if present in validated_data
        validated_data.pop('created_by', None)
        validated_data.pop('country', None)

        create_kwargs = {}
        if created_by is not None:
            create_kwargs['created_by'] = created_by
        if country_obj is not None:
            create_kwargs['country'] = country_obj

        wo = WorkOrder.objects.create(**create_kwargs, **validated_data)

        # set through-model records using helper methods on WorkOrder when available
        if primary_items:
            primary_pairs = [(item['sku'], item.get('qty', 1)) for item in primary_items]
            try:
                wo.set_primary_sku_quantities(primary_pairs)
            except AttributeError:
                # fallback: create through-model records directly
                from .models import WorkOrderPrimarySKU, MasterSKUMapping
                WorkOrderPrimarySKU.objects.filter(workorder=wo).delete()
                bulk = []
                for sku, qty in primary_pairs:
                    sku_obj = sku if hasattr(sku, 'pk') else MasterSKUMapping.objects.get(pk=sku)
                    bulk.append(WorkOrderPrimarySKU(workorder=wo, sku=sku_obj, quantity=qty or 1))
                WorkOrderPrimarySKU.objects.bulk_create(bulk)

        if additional_items:
            additional_pairs = [(item['sku'], item.get('qty', 1)) for item in additional_items]
            try:
                wo.set_additional_sku_quantities(additional_pairs)
            except AttributeError:
                # fallback: create through-model records directly
                from .models import WorkOrderAdditionalSKU, MasterSKUMapping
                WorkOrderAdditionalSKU.objects.filter(workorder=wo).delete()
                bulk = []
                for sku, qty in additional_pairs:
                    sku_obj = sku if hasattr(sku, 'pk') else MasterSKUMapping.objects.get(pk=sku)
                    bulk.append(WorkOrderAdditionalSKU(workorder=wo, sku=sku_obj, quantity=qty or 1))
                WorkOrderAdditionalSKU.objects.bulk_create(bulk)

        return wo
    
    def validate(self, attrs):
        # Ensure required fields are present and non-empty
        missing = []
        for f in ('sector', 'term', 'support', 'country'):
            val = attrs.get(f)
            if val in (None, ''):
                missing.append(f)
        if missing:
            raise serializers.ValidationError({m: 'This field is required.' for m in missing})
        return attrs

    def to_representation(self, instance):
        # represent created_by as email if present
        ret = super().to_representation(instance)
        user = getattr(instance, 'created_by', None)
        ret['created_by'] = user.email if user else None
        ret['country_name'] = instance.country.name if instance.country else ''

        # Replace primary_skus/additional_skus representation with
        # [{ 'sku': <pk>, 'qty': <quantity> }, ...] using through-model items
        try:
            primary_items = instance.get_primary_sku_items()
            ret['primary_skus'] = [
                {'sku': item.sku.id, 'qty': item.quantity, 'sku_name': item.sku.master_sku_name}
                for item in primary_items
            ]
        except Exception:
            # fall back to whatever was returned by super()
            pass

        try:
            additional_items = instance.get_additional_sku_items()
            ret['additional_skus'] = [
                {'sku': item.sku.id, 'qty': item.quantity, 'sku_name': item.sku.master_sku_name}
                for item in additional_items
            ]
        except Exception:
            pass

        return ret
    
    def update(self, instance, validated_data):
        primary_items = validated_data.pop('primary_skus', None)
        additional_items = validated_data.pop('additional_skus', None)

        # update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # replace through records if provided
        if primary_items is not None:
            primary_pairs = [(item['sku'], item.get('qty', 1)) for item in primary_items]
            try:
                instance.set_primary_sku_quantities(primary_pairs)
            except AttributeError:
                from .models import WorkOrderPrimarySKU, MasterSKUMapping
                WorkOrderPrimarySKU.objects.filter(workorder=instance).delete()
                bulk = []
                for sku, qty in primary_pairs:
                    sku_obj = sku if hasattr(sku, 'pk') else MasterSKUMapping.objects.get(pk=sku)
                    bulk.append(WorkOrderPrimarySKU(workorder=instance, sku=sku_obj, quantity=qty or 1))
                WorkOrderPrimarySKU.objects.bulk_create(bulk)
        if additional_items is not None:
            additional_pairs = [(item['sku'], item.get('qty', 1)) for item in additional_items]
            try:
                instance.set_additional_sku_quantities(additional_pairs)
            except AttributeError:
                from .models import WorkOrderAdditionalSKU, MasterSKUMapping
                WorkOrderAdditionalSKU.objects.filter(workorder=instance).delete()
                bulk = []
                for sku, qty in additional_pairs:
                    sku_obj = sku if hasattr(sku, 'pk') else MasterSKUMapping.objects.get(pk=sku)
                    bulk.append(WorkOrderAdditionalSKU(workorder=instance, sku=sku_obj, quantity=qty or 1))
                WorkOrderAdditionalSKU.objects.bulk_create(bulk)

        return instance
