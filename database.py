import sqlite3

class Database:
    
    def __init__(self, db="transit"):
        self.conn = sqlite3.connect('/home/yian/Downloads/us-census.db')
        self.cursor = self.conn.cursor()

    def get_fields(self):
        self.cursor.execute("PRAGMA table_info(%s);" % ("census_learn_sql"))
        return self.cursor.fetchall()

    def query_info(self, field):
        self.cursor.execute("""select distinct \"%s\", count(*), avg(age) from
        census_learn_sql group by \"%s\" order by count(*) desc limit 100"""\
            % (field, field))
        return self.cursor.fetchall()

    def field_var_count(self, field):
        self.cursor.execute("select count(distinct \"%s\") from census_learn_sql" % (field))
        return self.cursor.fetchone()