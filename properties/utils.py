from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_all_properties():
    queryset = cache.get('all_properties')
    if queryset is None:
        queryset = Property.objects.all()
        cache.set('all_properties', queryset, 3600)
    return queryset




def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info()

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)

        total = hits + misses
        hit_ratio = (hits / total) if total > 0 else None

        metrics = {
            "keyspace_hits": hits,
            "keyspace_misses": misses,
            "hit_ratio": round(hit_ratio, 4) if hit_ratio is not None else None
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            "keyspace_hits": None,
            "keyspace_misses": None,
            "hit_ratio": None,
            "error": str(e)
        }
