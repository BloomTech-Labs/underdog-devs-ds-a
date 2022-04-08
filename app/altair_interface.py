from typing import Dict
import altair as alt
from typing import Dict, Optional, Tuple
import pandas as pd
import json
from app.data import MongoDB

db = MongoDB("UnderdogDevs")

def prop_graphs(
    collection: str,
    key: str,
    graph_type: str = "bar"
    ):
    """create graph schema to plot value counts of a given field

    Utilizes Altair's count() aggregate function to generate and return
    a Vega Lite JSON schema that will plot a count of all documents
    containing each unique value in the given key of a given collection

    Currently only supports bar and pie charts, with bar as default.

    Args:
        x_coll: name of collection to pull x-axis data from
        x_field: field to target in collection for x-axis data
        graph_type: graph type to be generated
    
    Returns:
        JSON schema as a string
    """

    coll = db.get_collection(collection)

    # Data extraction from MongoDB database
    x = coll.distinct(key)
    y = [coll.count_documents({key: value}) for value in x]

    # Data converted to Pandas DF for variable type inferencing
    table = pd.DataFrame({"x": x}, {"y": y})
    graph = alt.Chart(data = table)

    # Decide graph type
    if graph_type == "bar":
        graph = graph.mark_bar().encode(x = "x", y = "y")
    elif graph_type == "pie":
        graph = graph.mark_arc().encode(theta = "x", color = "y")

    return json.dumps(json.loads(graph.to_json()))
