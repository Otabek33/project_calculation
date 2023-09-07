from datetime import datetime

year = datetime.now().year

HOLIDAYS = """
    {}-01-02,{}-01-03,{}-03-08,{}-03-20,{}-03-21,{}-03-22,{}-04-22,{}-04-24,{}-05-09,{}-06-30,{}-07-01,{}-09-01,{}-09-02,
    {}-10-02,{}-12-08,{}-12-30,""".format(
    year, year, year, year, year, year, year, year, year, year, year, year, year, year, year, year
).split(
    ","
)
