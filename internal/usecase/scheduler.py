from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler({'apscheduler.timezone': 'Europe/Moscow'}, )

if not scheduler.running:
    scheduler.start()
