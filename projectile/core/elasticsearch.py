MAPPINGS = {
    "core-organization": {
        # "settings": {
        #     "number_of_shards": 2,
        #     "number_of_replicas": 1
        # },
        "mappings": {
            "properties": {
                "uid": {"type": "keyword"},
                "slug": {"type": "keyword"},
                "name": {"type": "text"},
                "registration_no": {"type": "keyword"},
                "summary": {
                    "type": "text",
                },
                "status": {"type": "keyword"},
                "tags": {
                    "type": "nested",
                    "properties": {
                        "uid": {"type": "keyword"},
                        "slug": {"type": "keyword"},
                        "name": {"type": "keyword"},
                        "category": {"type": "keyword"},
                    },
                },
                "parents": {
                    "type": "nested",
                    "properties": {
                        "uid": {"type": "keyword"},
                        "slug": {"type": "keyword"},
                        "name": {"type": "keyword"},
                    },
                },
                "established_at": {"type": "date"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
            }
        }
    },
    "core-tag": {
        # "settings": {
        #     "number_of_shards": 2,
        #     "number_of_replicas": 1
        # },
        "mappings": {
            "properties": {
                "uid": {"type": "keyword"},
                "category": {"type": "keyword"},
                "slug": {"type": "keyword"},
                "name": {"type": "text"},
                "label": {
                    "type": "keyword",
                },
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
            }
        }
    },
}


def get_child_organizations_by_slug(slug):
    query = {
        "from": 0,
        "size": 40,
        "query": {
            "nested": {
                "path": "parents",
                "query": {"bool": {"must": [{"match": {"parents.slug": slug}}]}},
            }
        },
    }
    return query


def get_filter_tags():
    query = {
        "aggs": {
            "causes": {
                "nested": {"path": "tags"},
                "aggs": {
                    "tags_distinct": {
                        "terms": {
                            "field": "tags.category",
                            "size": 100,
                            "script": "doc['tags.slug'].value + '::' + doc['tags.name'].value + '::' + doc['tags.category'].value",
                        }
                    }
                },
            }
        }
    }
    return query
