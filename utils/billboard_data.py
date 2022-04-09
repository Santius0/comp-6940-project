import billboard
from datetime import date, timedelta
import pandas as pd


def get_chart(chart_title='hot-100', week=date.today(), starting_id=0):
    chart = billboard.ChartData(chart_title, date=week, max_retries=10, fetch=True)
    return pd.DataFrame(data=[[
        # starting_id + idx,
        # song.title,
        song.artist,
        song.image,
        song.peakPos,
        song.lastPos,
        song.weeks,
        song.rank,
        song.isNew,
        chart.date] for idx, song in enumerate(chart)],
        columns=[
            # 'id',
            # 'title',
            'artist',
            'image',
            'peakPos',
            'lastPos',
            'weeks',
            'rank',
            'isNew',
            'date'], index=[song.title for song in chart]), starting_id + len(chart)
