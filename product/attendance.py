from .store import require, money

from .memberships import Memberships

class Attendance:
    def __init__(self, store):
        self.store = store

    def checkin(self, id, membership, person, at, venue):
        record = self.store.get('membership',membership)
        status = Memberships(self.store).status(membership,at)
        require(status['active'] and status['venue']==venue,'会籍不在该馆有效服务期')
        require(record['person']==person or record['kind']=='family','会籍不可共用')
        return self.store.put('visit',id,dict(membership=membership,person=person,at=at,
            venue=venue,household=record['household']),create=True)

    def recent(self, membership):
        visits = [item for item in self.store.all('visit') if item['membership']==membership]
        return dict(count=len(visits),last=max((item['at'] for item in visits),default=None))
