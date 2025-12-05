from rest_framework.throttling import UserRateThrottle


class EventQueryThrottle(UserRateThrottle):
    scope = 'event_query'
    rate = '20/day'


class InscriptionThrottle(UserRateThrottle):
    scope = 'inscription'
    rate = '50/day'
