from setuptools import setup, find_packages


setup(
    name="web3-security-engine",
    version="1.2",
    author="Debank",
    author_email="security@debank.com",
    description="Web3 Security Engine",
    url="https://debank.com", 
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'PyYAML==6.0',
        'smmap==5.0.0',
        'requests==2.27.1'
    ]
)