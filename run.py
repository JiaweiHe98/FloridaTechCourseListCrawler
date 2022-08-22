import os
import uvicorn
from absl import app, flags
from src.main import main
from src.api import api

FLAGS = flags.FLAGS
flags.DEFINE_enum('semester', None, ['fall', 'spring', 'summer', 'all'], 'Semesters')
flags.DEFINE_enum('api', 'off', ['on', 'off'], 'Api status')
flags.DEFINE_boolean('useAsync', True, 'Use async method for parsing')


def run(argv):
    if FLAGS.api == 'on':
        # os.system('uvicorn run:run_api')
        run_api()
    else:
        main(FLAGS.semester, FLAGS.useAsync)


def run_api():
    uvicorn.run(api.app)


if __name__ == '__main__':
    app.run(run)
