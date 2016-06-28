# *-* coding: utf-8 -*- 

from flask import current_app
from gcloud import datastore


builtin_list = list


def init_app(app):
    app
    
    
def get_client():
    return datastore.Client(current_app.config["PROJECT_ID"])


def from_datastore(entity):
    """ Translates Datastore results into the format expected by the application.
    
    Datastore typically returns:
        [Entity{key: (kind, id), prop: value, ... }]
        
    This returns:
        {id: id, prop: value, ... }
    """
    if not entity:
        return None
    
    if isinstance(entity, builtin_list):
        entity = entity.pop()
        
    entity["id"] = entity.key.id
    return entity


def list(limit=10, cursor=None):
    ds = get_client()
    query = ds.query(kind="Book", order=["title"])
    it = query.fetch(limit=limit, start_cursor=cursor)
    entities, more_results, cursor = it.next_page()
    entities = builtin_list(map(from_datastore, entities))
    return entities, cursor.decode("utf-8") if len(entities) == limit else None


def read(id):
    ds = get_client()
    key = ds.key("Book", int(id))
    results = ds.get(key)
    return from_datastore(results)


def update(data, id=None):
    ds = get_client()
    if id:
        key = ds.key("Book", int(id))
    else:
        key = ds.key("Book")
        
    entity = datastore.Entity(key=key, 
                              exclude_from_indexes=["description"])
    
    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


create = update


def delete(id):
    ds = get_client()
    key = ds.key("Book", int(id))
    ds.delete(key)
