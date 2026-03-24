from setuptools import find_packages, setup

package_name = 'tracksense_robot_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'arduino_node = tracksense_robot_pkg.arduino_node:main',
            'bridge_node = tracksense_robot_pkg.bridge_node:main',
            'rear_camera_node = tracksense_robot_pkg.rear_camera_node:main',
            'front_camera_node = tracksense_robot_pkg.front_camera_node:main',
            'arduino_limited_node = tracksense_robot_pkg.arduino_limited_node:main',
        ],
    },
)
