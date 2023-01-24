import shutil
import unittest

import HtmlTestRunner

loader = unittest.TestLoader()

if __name__ == '__main__':
    try:
        shutil.rmtree('output')
    except:
        print('no output folder yet')

    start_dir = '.'
    suite = loader.discover(start_dir)

    # run
    runner = HtmlTestRunner.HTMLTestRunner(combine_reports=True, output='output', verbosity=2)
    runner.run(suite)

# open file
# chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
# file = os.listdir('output')[0]
# path = os.path.realpath(file)
# webbrowser.get(using='google-chrome').open('file://' + path)
