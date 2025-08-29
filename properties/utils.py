from django.core.cache import cache
from .models import Property


def get_all_properties():
    """
    Cache the Property queryset in Redis for 1 hour using Django's low-level cache API.
    """
    # Check Redis for cached properties
    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        return cached_properties
    
    # If not found in cache, fetch from database
    queryset = Property.objects.all()
    
    # Store the queryset in Redis with 1 hour timeout (3600 seconds)
    cache.set('all_properties', queryset, 3600)
    
    return queryset
