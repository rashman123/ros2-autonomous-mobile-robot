from setuptools import setup
from glob import glob
import os

package_name = 'my_robot_description'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (
            'share/' + package_name,
            ['package.xml']
        ),
        (
            'share/' + package_name + '/launch',
            glob('launch/*.py')
        ),
        (
            'share/' + package_name + '/urdf',
            glob('urdf/*')
        ),
        (
            'share/' + package_name + '/worlds',
            glob('worlds/*')
        ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rashman',
    maintainer_email='rashman@todo.todo',
    description='Robot description for Gazebo',
    license='MIT',
    tests_require=['pytest'],
    entry_points={},
)
