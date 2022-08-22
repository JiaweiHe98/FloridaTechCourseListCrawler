from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from src.api.helpers import courseListLoader
from src.main import run

course_list = {}


def load_course_list():
    global course_list
    course_list = courseListLoader.read()


load_course_list()
app = FastAPI()


@app.get('/')
def landing():
    return {'message': 'Welcome to Florida Tech Course List Parser Backend!'}


@app.get('/course')
def get_course_list(semester: str or None = None):
    if semester is None or semester not in ['fall', 'spring', 'summer', 'all']:
        raise HTTPException(status_code=400,
                            detail='Semester not specified or semester not exist! (fall, spring, summer, all)')

    if len(course_list) == 0:
        raise HTTPException(status_code=500,
                            detail='Course list is currently unavailable')

    if semester == 'fall':
        return course_list['fall']
    elif semester == 'spring':
        return course_list['spring']
    elif semester == 'summer':
        return course_list['summer']
    else:
        return course_list


@app.get('/parse')
def start_parsing(semester: str or None = None, use_async: bool = True):
    if semester is None or semester not in ['fall', 'spring', 'summer', 'all']:
        raise HTTPException(status_code=400,
                            detail='Semester not specified or semester not exist! (fall, spring, summer, all)')

    global course_list
    course_list = run(semester, use_async)
    # try:
    #     course_list = run(semester, use_async)
    # except Exception:
    #     raise HTTPException(status_code=500, detail='Parser fail')

    return {'message': 'Parse finished!'}
