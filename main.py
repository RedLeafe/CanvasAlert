import db as db
import canvas_api as canvas_api
import canvas_alert_bot as cab
from datetime import datetime
import asyncio
import time


async def main():
    time.sleep(1)
    table = db.getTable()
    
    for row in table:

        if (row[2] == 1):

            preferred_time = row[3]
            assignments = []
            try:
                assignments = canvas_api.get_assignments("https://csufullerton.instructure.com/", row[1])
            except Exception as e:
                print(f"Failed to get assignments for {row[0]}: {e}")
            db_assignments = db.selectAssignments(row[0])
            db_set = set()
            for assignment in db_assignments:
                db_set.add(assignment[0])
            print(db_assignments)
            print(assignments)

            for assignment in assignments:
                if not assignment[0] in db_set:
                    due_date = datetime.strptime(assignment[1], "%Y-%m-%dT%H:%M:%SZ")
                    now = datetime.utcnow()
                    diff = due_date - now
                    
                    hours = diff.total_seconds() / 3600

                    if hours <= preferred_time:
                        await cab.send_alert_message(row[0], f"Assintment due within {preferred_time}: {assignment[0]}")
                        print(assignment)
                    else:
                        print("Nothing due within time")
            
        if (row[5] == 1):
            for row in table:
                try:
                    announcements = canvas_api.get_announcements("https://csufullerton.instructure.com/", row[1])
                except Exception as e:
                    print(f"Failed to get announcements for {row[0]}: {e}")
            for announcement in announcements:

                assign_date = datetime.strptime(announcement[2], "%Y-%m-%dT%H:%M:%SZ")
                now = datetime.utcnow()
                diff = now - assign_date
                hours = diff.total_seconds() / 3600
                if hours <= 200:
                    await cab.send_alert_message(row[0], f"Announcement for {announcement[0]} at {assign_date}: {announcement[1]}")
                    print(announcement[1])
    print("done")
                

async def run_all():
    await asyncio.gather(
        asyncio.to_thread(cab.runBot),
        main()
    )

if __name__ == '__main__':
    asyncio.run(run_all())