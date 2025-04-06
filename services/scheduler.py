from apscheduler.schedulers.background import BackgroundScheduler
from services.tcu_service import consultar_todos
from datetime import datetime

def agendar_tarefas(app):
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(
        func=consultar_todos,
        trigger='cron',
        day=1,
        hour=4,
        minute=0,
        id='consulta_mensal',
        name='Consulta mensal de status no TCU',
        replace_existing=True
    )
    
    scheduler.start()