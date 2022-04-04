from typing import Dict
import altair as alt
from typing import Dict, Optional, Tuple
import pandas as pd
import json

def generate_schema(
    data: Dict,
    x: str,
    y: str,
    graph_type: str,
    style_x: Optional[Dict] = None,
    style_y: Optional[Dict] = None,
    size: Optional[Dict] = None
    ):
    """Use given data to return Vega Lite JSON schema for bar graph

    Following the given parameters, utilizes the given data alongside
    Altair functionality to return a Vega Lite JSON schema to be used
    by front end for bar graph embedding.

    Altair-compatible aggregate functions are viable for x or y string
    values, i.e. y = "count()" will count records in each category of x
    and populate the y axis accordingly. See Altair documentation for
    all available aggregate functions.

    Similarly, style_x and style_y offer granular styling options for
    the axes. The options are expansive, therein Altair documentation
    should be referenced for a comprehensive list. Some examples include
    title*, tick*, and label* (the * denote subsequent options, i.e.
    titleFont, titleFontSize, titleColor, etc.)

    Args:
        data (dict): Data to be received for graphing
        x (str): Key to be used for the x axis
        y (str): Key to be used for the y axis
        graph_type (str): Type of graph to generate
        style_x (dict) (optional): kwargs for styling x axis
        style_y (dict) (optional): kwargs for styling y axis
        size (dict) (optional): {"height": pixels (int), "width": pixels (int)}
    
    Returns:
        JSON schema as a string
    """

    # Data converted to Pandas DF for variable type inferencing
    table = pd.DataFrame(data)
    graph = alt.Chart(data = table)

    # Decide graph type
    if graph_type == "bar":
        graph = graph.mark_bar().encode(x = x, y = y)
    elif graph_type == "pie":
        graph = graph.mark_arc().encode(theta = x, color = y)
    
    # Styling options
    if style_x:
        graph = graph.configure_axisX(**style_x)
    if style_y:
        graph = graph.configure_axisY(**style_y)
    if size:
        graph = graph.properties(
            height = size["height"],
            width = size["width"]
            )

    return json.dumps(json.loads(graph.to_json()))
