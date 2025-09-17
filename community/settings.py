from interop.bs import BS
from interop.query_bo import QueryBO
from interop.embed_bo import EmbedBO

CLASSES = {"Python.BS": BS, "Python.EmbedBO": EmbedBO, "Python.QueryBO": QueryBO}

PRODUCTIONS = [
    {
        "Python.Production": {
            "@Name": "Python.Production",
            "@LogGeneralTraceEvents": "false",
            "Description": "",
            "ActorPoolSize": "1",
            "Item": [
                {
                    "@Name": "BS",
                    "@ClassName": "Python.BS",
                    "@PoolSize": "1",
                    "@Enabled": "true",
                },
                {
                    "@Name": "EmbedBO",
                    "@ClassName": "Python.EmbedBO",
                    "@PoolSize": "1",
                    "@Enabled": "true",
                },
                {
                    "@Name": "QueryBO",
                    "@ClassName": "Python.QueryBO",
                    "@PoolSize": "1",
                    "@Enabled": "true",
                },
            ],
        }
    }
]
