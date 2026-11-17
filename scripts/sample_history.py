import random
import json
from datetime import date, timedelta

def generate():
    rng = random.Random(117204)
    operations = []

    def add(command, **arguments):
        operations.append([command, arguments])

    def day(offset):
        return (date(2026, 7, 1) + timedelta(days=offset)).isoformat()
    for index in range(180):
        key = f'm{index}'
        add('memberships.enroll', id=key, person=f'p{index}', household=f'h{index // 2}', venue=f'v{index % 3}', start=day(index % 20), end=day(60 + index % 100), kind='family' if index % 6 == 0 else 'individual')
        pause = index % 7 == 0
        if pause:
            add('memberships.pause', id=key, start=day(40), end=day(50))
        for offset in range(21, 60, 7):
            if rng.random() < 0.65 and (not (pause and 40 <= offset < 50)):
                add('attendance.checkin', id=f'v{index}:{offset}', membership=key, person=f'p{index}', at=day(offset), venue=f'v{index % 3}')
        if index % 8 == 0:
            add('memberships.transfer', id=key, venue=f'v{(index + 1) % 3}', effective=day(55))
        if index % 3 == 0:
            add('care.plan', id=f'c{index}', memberships=[key], at=day(55), limit=1)
            add('care.finish', id=f'c{index}', membership=key, outcome=rng.choice(['reached', 'failed', 'declined']))
    return operations

def main():
    import argparse
    parser = argparse.ArgumentParser(description='生成本地合成业务记录，不包含真实个人资料')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    from pathlib import Path
    Path(args.output).write_text(json.dumps(generate(), ensure_ascii=False, indent=2) + '\n')

if __name__=='__main__':
    main()
