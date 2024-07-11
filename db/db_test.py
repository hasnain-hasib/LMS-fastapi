from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import sys
import getpass
from colorama import init, Fore, Style

init(autoreset=True)

def print_header(message):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{message}{Style.RESET_ALL}")

def print_subheader(message):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def print_info(label, value, value_color=Fore.WHITE):
    print(f"{Fore.GREEN}{label}:{Style.RESET_ALL} {value_color}{value}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def print_database_list(databases):
    print_header("Available databases:")
    for i, db in enumerate(databases, 1):
        print(f"{Fore.BLUE}{i}. {db}{Style.RESET_ALL}")

def get_connection_details():
    use_default = input("Use default connection string? (y/n): ").lower() == 'y'
    if use_default:
        return "postgresql+psycopg2://hasib:2325210@localhost/fastdb"
    else:
        host = input("Enter database host (default: localhost): ") or "localhost"
        port = input("Enter database port (default: 5432): ") or "5432"
        user = input("Enter database user: ")
        password = getpass.getpass("Enter database password: ")
        database = input("Enter database name: ")
        return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

def execute_query(connection, query, fetch='one'):
    try:
        result = connection.execute(text(query))
        if fetch == 'one':
            return result.fetchone()
        elif fetch == 'all':
            return result.fetchall()
    except SQLAlchemyError as e:
        print_warning(f"Error executing query: {e}")
        return None

def list_databases(engine):
    try:
        with engine.connect() as connection:
            databases = execute_query(connection, "SELECT datname FROM pg_database WHERE datistemplate = false;", 'all')
            if databases:
                print_database_list([db[0] for db in databases])
                return [db[0] for db in databases]
            else:
                print_warning("No databases found.")
                return []
    except OperationalError as e:
        print_warning(f"Error connecting to PostgreSQL: {e}")
        sys.exit(1)

def check_database(engine):
    try:
        with engine.connect() as connection:
            print_header("Database Connection Information:")
            print_info("Connected to", engine.url.host, Fore.RED)
            print_info("Database", engine.url.database, Fore.BLUE)

            server_version = execute_query(connection, "SELECT version();")
            if server_version:
                print_info("PostgreSQL version", server_version[0])

            db_size = execute_query(connection, "SELECT pg_size_pretty(pg_database_size(current_database()));")
            if db_size:
                print_info("Database size", db_size[0])

            table_count = execute_query(connection, "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            if table_count:
                print_info("Number of tables", table_count[0])

            print_subheader("\nActive connections:")
            active_connections = execute_query(connection, """
                SELECT 
                    application_name,
                    client_addr,
                    backend_start,
                    state,
                    query
                FROM pg_stat_activity 
                WHERE datname = current_database() AND pid != pg_backend_pid();
            """, 'all')
            if active_connections:
                for conn in active_connections:
                    print_info("Application", conn[0] or 'N/A', Fore.GREEN)
                    print_info("  Client Address", conn[1] or 'N/A', Fore.RED)
                    print_info("  Connected Since", conn[2])
                    print_info("  State", conn[3])
                    print_info("  Current Query", f"{conn[4][:50]}..." if conn[4] and len(conn[4]) > 50 else conn[4] or 'N/A')
                    print()
            else:
                print("No active connections other than the current one.")

            print_subheader("\nTop 5 largest tables:")
            largest_tables = execute_query(connection, """
                SELECT relname AS table_name,
                       pg_size_pretty(pg_total_relation_size(relid)) AS total_size
                FROM pg_catalog.pg_statio_user_tables
                ORDER BY pg_total_relation_size(relid) DESC
                LIMIT 5;
            """, 'all')
            if largest_tables:
                for table in largest_tables:
                    print_info(table[0], table[1])
            else:
                print("No tables found in the database.")

            print_subheader("\nRecent database activity:")
            recent_activity = execute_query(connection, """
                SELECT datname, query, state, age(now(), query_start) AS duration
                FROM pg_stat_activity
                WHERE state != 'idle' AND datname = current_database()
                ORDER BY query_start DESC
                LIMIT 5;
            """, 'all')
            if recent_activity:
                for activity in recent_activity:
                    print_info("Database", activity[0], Fore.BLUE)
                    print_info("  Query", f"{activity[1][:50]}..." if len(activity[1]) > 50 else activity[1])
                    print_info("  State", activity[2])
                    print_info("  Duration", activity[3])
                    print()
            else:
                print("No recent activity found.")

            print_subheader("Database statistics:")
            db_stats = execute_query(connection, """
                SELECT 
                    COALESCE(sum(seq_scan), 0) AS sequential_scans,
                    COALESCE(sum(seq_tup_read), 0) AS sequential_tuples_read,
                    COALESCE(sum(idx_scan), 0) AS index_scans,
                    COALESCE(sum(idx_tup_fetch), 0) AS index_tuples_fetched,
                    COALESCE(sum(n_tup_ins), 0) AS rows_inserted,
                    COALESCE(sum(n_tup_upd), 0) AS rows_updated,
                    COALESCE(sum(n_tup_del), 0) AS rows_deleted
                FROM pg_stat_user_tables;
            """)
            if db_stats:
                for key, value in db_stats._mapping.items():
                    print_info(f"  {key}", value)
            else:
                print("No statistics available.")

    except OperationalError as e:
        print_warning(f"Error connecting to the database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    connection_string = get_connection_details()
    engine = create_engine(connection_string)

    try:
        with engine.connect() as connection:
            print_header("Connection to the database was successful!")
            check_database(engine)
    except Exception as e:
        print_warning(f"An error occurred: {e}")
        sys.exit(1)