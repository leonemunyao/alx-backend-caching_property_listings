from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging


logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Cache the Property queryset in Redis for 1 hour using Django's low-level cache API.
    """

    cached_properties = cache.get('all_properties')
    
    if cached_properties is not None:
        return cached_properties
    
    queryset = Property.objects.all()
    
    cache.set('all_properties', queryset, 3600)
    
    return queryset


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including hit ratio
    """
    try:

        redis_conn = get_redis_connection("default")
        
        info = redis_conn.info('stats')
        
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = keyspace_hits / total_requests if total_requests > 0 else 0
        
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': hit_ratio,
            'hit_ratio_percentage': hit_ratio * 100
        }
        
        logger.info(f"Redis Cache Metrics: "
                   f"Hits: {keyspace_hits}, "
                   f"Misses: {keyspace_misses}, "
                   f"Hit Ratio: {hit_ratio:.2%}")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0,
            'hit_ratio_percentage': 0,
            'error': str(e)
        }
