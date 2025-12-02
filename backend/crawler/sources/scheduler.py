# backend/src/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

def start_scheduler(app):
    """
    启动后台定时任务调度器：
    每天固定时间自动跑一次爬虫。
    """
    from crawler.sources.crawler_simple import run_crawler_main

    scheduler = BackgroundScheduler(timezone="Asia/Shanghai")

    def job_wrapper():
        # 确保在 Flask app 上下文中运行（可以访问 db 等）
        with app.app_context():
            app.logger.info("[Scheduler] 开始执行每日爬虫任务")
            run_crawler_main()
            app.logger.info("[Scheduler] 每日爬虫任务结束")

    # 每天凌晨 3:00 运行一次（你也可以改成 hour=2 或别的）
    trigger = CronTrigger(hour=3, minute=0)
    scheduler.add_job(job_wrapper, trigger, id="daily_crawler", replace_existing=True)

    scheduler.start()
    app.logger.info("[Scheduler] 后台定时任务已启动（每日 03:00 爬虫）")
