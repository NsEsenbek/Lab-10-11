import psycopg2 
import psycopg2.extras


username = "postgres"
pwd = "FuryRyosuke"
database = "demo"
port_id = "5432"
hostname = "localhost"
conn = None
end = False
try:    
    with psycopg2.connect(
        host = hostname,
        dbname = database,
        password = pwd,
        user = username,
        port = port_id
    ) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            # cur.execute('DROP TABLE employee')
            create_script = ''' CREATE TABLE IF NOT EXISTS employee (
                                    id serial PRIMARY KEY,
                                    name    varchar(40) NOT NULL,
                                    phone   varchar(40) NOT NULL) '''
            cur.execute(create_script)
            while end == False:
                print("Input:")
                now = input()
                if now == 'close':
                    end = True
                elif now == 'enter':
                    print("Enter name and phone:")
                    values = (input(), input())
                    print(values)
                    insert_script = 'INSERT INTO employee (name, phone) VALUES (%s, %s)'

                    output_script = f"SELECT phone FROM employee WHERE name = '{values[0]}'"

                    cur.execute(output_script)
                    res = cur.fetchone()
                    if res:
                        print("This name already exists")
                        print("Otvet:")
                        otvet = input()
                        closeotvet = False
                        while closeotvet == False:
                            if otvet == 'add':
                                update_script = f"UPDATE employee SET phone = '{values[1]}' WHERE name = '{values[0]}'"
                                cur.execute(update_script)
                                print(values[0], values[1])
                                closeotvet = True
                            elif otvet == 'continue':
                                print("ok")
                                closeotvet = True
                            else:
                                print("unknown command")
                    else:
                        cur.execute(insert_script, values)
                elif now == 'output':
                    print("Print name:")
                    output_script = f"SELECT id, phone FROM employee WHERE name = '{input()}'"
                    cur.execute(output_script)
                    res = cur.fetchone()
                    if res:
                        print(res)
                    else:
                        print("This name not exist")
                elif now == 'restart':
                    cur.execute('DROP TABLE employee')
                elif now == 'delete':
                    print("Input name to delete:")
                    name_to_delete = input()
                        # DELETE FROM employee
                        # WHERE name = 'Nurtas';
                    delete_script = f"""    DELETE FROM employee
                                            WHERE name = '{name_to_delete}'"""
                    cur.execute(delete_script)
                else:
                    print("Unknown command")
            conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
