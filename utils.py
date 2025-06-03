def get_next_id(r, key):
    return r.incr(f"id:{key}")

def get_all_items(r, prefix):
    keys = r.keys(f"{prefix}:*")
    items = []
    for key in keys:
        item = r.hgetall(key)
        for k, v in item.items():
            if k.endswith('_id') or k == 'id' or k == 'quantity' or k == 'user_id' or k == 'brewery_id' or k == 'beer_id':
                item[k] = int(v)
            elif k == 'price':
                item[k] = float(v)
        items.append(item)
    return items