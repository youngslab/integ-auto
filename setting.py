from setuptools import setup, find_packages

setup(
    name='integ-auto',
    version='0.3',
    description='Integrated Automation Framework',
    author='Jaeyoung Park',
    author_email='jaeyoungs.park@gmail.com',
    url='https://github.com/youngslab/integ-auto',
    install_requires=['dispatch', 'autoit', 'selenium', 'pyautogui'],
    packages=find_packages(exclude=[]),
    keywords=['automation', 'selenium', 'autoit'],
    python_requires='>=3',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
