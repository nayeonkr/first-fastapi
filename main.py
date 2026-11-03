from fastapi import FastAPI, Request
import random
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def home():
    return {'hello': 'hi'}

@app.get('/lunch')  
def lunch():
    menu = ['김밥', '라면', '떡볶이']
    return {
        'pick' : random.choice(menu)
    }

@app.get('/lotto')
def lotto():
    numbers = sorted(random.sample(range(1, 46), 6))
    return {'numbers': numbers}

@app.get('/lotto/html')
def lotto_html(request: Request):
    numbers = random.sample(range(1, 46), 6)
    return templates.TemplateResponse(
        request=request, 
        name='lotto.html',
        context={'numbers': numbers, 'hi': 'nayeon'}

    )

# 경로요청 옵션
@app.get('/profile/{username}')
def profile(username: str):
    return {'username': username}

@app.get('/cube/{number}')
def cube(number: int):  #문자타입을 생략할경우 str타입이 된다
    return {'number': number ** 3} #str 타입일 경우 연산에서 에러가 발생한다

@app.get('/api/lotto')
def lotto_api(count: int = 1):
    games = []
    for i in range(count):
        numbers = random.sample(range(1, 46), 6)
        games.append(numbers)

    return games

@app.get('/lotto/html2')
def lotto_html2(request: Request, count: int = 1):
    games = [random.sample(range(1, 46), 6) for _ in range(count)]
    # games = [random.sample(range(1, 46), 6) for i in range(count)]
    
    return templates.TemplateResponse(
        request=request,
        name='lotto2.html',
        context={'games': games}

    )

#라우팅부터 함 ping이라는 라우팅을 만듦
@app.get('/ping')
def ping(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='ping.html'
    )

@app.get('/pong')
def pong(count: int):
    return {'count': count * 2}

@app.get('/lotto/ping')
def lotto_ping(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='lotto_ping.html'
    )

@app.get('/lotto/pong')
def lotto_pong(request: Request, count: int):
    games = [sorted(random.sample(range(1, 46), 6)) for _ in range (count)]

    # 발행일 / 추첨일(다음 토요일) / 지급기한(추첨일 + 1년)
    now = datetime.now()
    draw_date = now + timedelta(days=(5 - now.weekday()) % 7)
    deadline = draw_date + timedelta(days=365)

    return templates.TemplateResponse(
        request=request,
        name='lotto_pong.html',
        context={
            'games': games,
            'now': now,
            'draw_date': draw_date,
            'deadline': deadline,
        }
    )