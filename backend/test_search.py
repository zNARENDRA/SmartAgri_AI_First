from app.services.scheme_service import scheme_service
import json

res = scheme_service.search_schemes(None, None)
print("total_schemes:", res.total_schemes)
