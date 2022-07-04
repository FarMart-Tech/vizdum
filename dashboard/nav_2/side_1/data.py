

from pytz import timezone
from datetime import datetime, timedelta
import pandas as pd
import time
import numpy as np
import plotly as px
from extras.utils import lru_ttl_cache


@lru_ttl_cache(ttl_seconds=60)
def side_1_db():
    df = px.data.gapminder().query("year==2007")
    return df
