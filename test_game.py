position = 'b2'
inventory = {'key_items': list(), 'useful_items': list()}
item = {'nameDisplay': 'small key',
        'description': 'A small glowing key, it probably can be use to open a door.',
        'whenGrabbed': 'You bend down and grab it.',
        'whenUsed': 'You use the key to open the door, it works!',
        'wasUsed': False,
        'conditionUse': lambda: position == 'b3',
        'classification': 'key_item'}
inventory['key_items'].append(item)
referredItem = 'small key'

verify_item = dict()
for index in inventory['key_items']:
    if index['nameDisplay'] == referredItem:
        verify_item = index
if verify_item == dict():
    for index in inventory['useful_items']:
        if index['nameDisplay'] == referredItem:
            verify_item = index
position = 'b3'
if verify_item['classification'] == 'key_item':
    if verify_item['conditionUse']():
        print(verify_item['whenUsed'])
        print('After used, the ' + referredItem + ' was swallow by darkness.')

    else:
        print('You cannot use this item here.')
