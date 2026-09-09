from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'my_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'action'),
            glob('action/*.action')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='rashman',
    maintainer_email='rashman@todo.todo',
    description='Basic ROS 2 nodes for a mobile robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_publisher = my_robot.publisher:main',
            'my_subscriber = my_robot.subscriber:main',
            'adder_server = my_robot.adder_server:main',
            'adder_client = my_robot.adder_client:main',
            'count_action_server = my_robot.count_action_server:main',
	    'count_action_client = my_robot.count_action_client:main',
        ],
    },
)
