import sqlite3

class Database:
    
    def __init__(self, db_uri, main_table, col_to_avg, limit=100):
        self.conn = sqlite3.connect(db_uri, check_same_thread = False) 
        self.main_table = main_table
        self.col_to_avg = col_to_avg
        self.limit = limit

    def get_fields(self):
        cur = self.conn.cursor()
	cur.execute("PRAGMA table_info(%s);" % (self.main_table))
        return cur.fetchall()

    def query_info(self, field):
        cur = self.conn.cursor()
	cur.execute("""select distinct \"%s\", count(*), avg(%s) from
        %s group by \"%s\" order by count(*) desc limit %d"""\
            % (field, self.col_to_avg, self.main_table, field, self.limit))
        return cur.fetchall()

    def field_var_count(self, field):
        cur = self.conn.cursor()
	cur.execute("select count(distinct \"%s\") from %s" % (field, self.main_table))
        return cur.fetchone()

    def hidden_row_count(self, field):
        cur = self.conn.cursor()
        cur.execute("select (select count(*) as total_count from %s) - (select sum(count) from (select count(*) as count from %s group by \"%s\" limit %s) as temp) as difference;" % (self.main_table, self.main_table, field, self.limit))
	return cur.fetchone()
