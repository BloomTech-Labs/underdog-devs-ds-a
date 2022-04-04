from typing import Dict
import altair as alt
from typing import Dict
import pandas as pd
import json

def generate_schema(data: Dict, x: str, y: str, style: str):
    """Use given data to return Vega Lite JSON schema for bar graph

    Following the given parameters, utilizes the given data alongside
    Altair functionality to return a Vega Lite JSON schema to be used
    by front end for bar graph embedding.
    Altair-compatible aggregate functions are viable for x or y string
    values, i.e. y = "count()" will count records in each category of x.
    See Altair documentation for all available aggregate functions.
    """
    table = pd.DataFrame(data)
    graph = alt.Chart(data=table)
    if style == "bar":
        graph = graph.mark_bar().encode(x=x, y=y)
    if style == "pie":
        graph = graph.mark_arc().encode(theta=x, color=y)
    return json.loads(graph.to_json())
