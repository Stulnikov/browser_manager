from distutils.core import setup

setup(name='browser manager',
      version='0.1',
      description='Browser Manager',
      license="MIT",
      author='Aleksey Stulnikov',
      author_email='a.stulnikov@mobidev.biz',
      url='https://github.com/Stulnikov/browser_manager',
      py_modules=['browser_manager'],
      install_requires=['selenium>=3.141.0'],
      zip_safe=False)
