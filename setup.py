from setuptools import setup, find_packages


setup(
    name="web3-security-engine",
    version="1.0",
    author="Debank",
    author_email="0xjeffer@gmail.com",
    description="Web3 Security Engine",
    url="web3 security rule engine", 
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'gitdb==4.0.9',
        'GitPython==3.1.27',
        'PyYAML==6.0',
        'smmap==5.0.0'
    ]
)