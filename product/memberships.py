from .store import require, money

class Memberships:
    def __init__(self, store):
        self.store = store

    def enroll(self, id, person, household, venue, start, end, kind='individual'):
        require(start<end,'会籍区间无效')
        return self.store.put('membership',id,dict(person=person,household=household,
            venue=venue,start=start,end=end,kind=kind,pauses=[],transfers=[]),create=True)

    def pause(self, id, start, end):
        record = self.store.get('membership',id)
        require(record['start']<=start<end<=record['end'],'暂停超出会籍')
        require(not any(start<item['end'] and end>item['start'] for item in record['pauses']),'暂停重叠')
        record['pauses'].append(dict(start=start,end=end))
        return self.store.put('membership',id,record)

    def transfer(self, id, venue, effective):
        record = self.store.get('membership',id)
        require(record['start']<=effective<record['end'],'转会日期无效')
        require(not record['transfers'] or effective>record['transfers'][-1]['effective'],'转会须按生效日登记')
        record['transfers'].append(dict(venue=venue,effective=effective))
        return self.store.put('membership',id,record)

    def status(self, id, at):
        record = self.store.get('membership',id)
        venue = record['venue']
        for transfer in record['transfers']:
            if transfer['effective']<=at:
                venue=transfer['venue']
        active = record['start']<=at<record['end'] and not any(
            item['start']<=at<item['end'] for item in record['pauses'])
        return dict(active=active,venue=venue,household=record['household'])
