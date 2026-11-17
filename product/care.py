from .store import require, money

from .memberships import Memberships

class Care:
    def __init__(self, store):
        self.store = store

    def plan(self, id, memberships, at, limit):
        require(len(memberships)<=limit and limit>=0,'名额不足')
        require(len(memberships)==len(set(memberships)),'名单重复')
        households=[]
        for member in memberships:
            status = Memberships(self.store).status(member,at)
            require(status['active'],'暂停或到期会籍不可联系')
            households.append(status['household'])
        require(len(households)==len(set(households)),'同家庭重复联系')
        return self.store.put('care_plan',id,dict(memberships=memberships,at=at,
            limit=limit,finished={}),create=True)

    def finish(self, id, membership, outcome):
        require(outcome in ('reached','failed','declined'),'联系结果无效')
        record = self.store.get('care_plan',id)
        require(membership in record['memberships'],'不在名单内')
        if membership in record['finished']:
            require(record['finished'][membership]==outcome,'已登记其他结果')
            return record
        record['finished'][membership]=outcome
        return self.store.put('care_plan',id,record)
